from core.schemas import (
    DatasetCandidate,
    DatasetRanking,
    DatasetSelectionRequest,
    BandResolution,
    AnalysisResolution,
    AnalysisTemporalResolution,
)

from core.band_mapping import get_band_mapping
from core.registry import (
    get_index,
    get_sar_analysis,
)
from core.dataset_registry import get_dataset
from core.product_registry import get_product


SPATIAL_WEIGHT = 0.30
TEMPORAL_WEIGHT = 0.25
NATIVE_WEIGHT = 0.15
SPECTRAL_WEIGHT = 0.15
COMPUTATIONAL_WEIGHT = 0.15


def get_analysis_resolution(
    candidate: DatasetCandidate,
    index_name: str,
) -> AnalysisResolution:
    """
    Determine the analysis resolution for an index.

    Product pathways use the product's native spatial resolution.
    Calculated pathways derive the resolution from the required bands.
    """

    # Product pathway
    if candidate.pathway == "product":
        if candidate.product is None:
            raise ValueError(
                "Product pathway requires a product."
            )

        product = get_product(candidate.product)

        if product.spatial_resolution_m is None:
            raise ValueError(
                f"Product {candidate.product} does not define "
                "a spatial resolution."
            )

        return AnalysisResolution(
            resolution_m=product.spatial_resolution_m,
            band_resolutions=[],
            resampling_required=False,
        )


    # Calculated pathway
    dataset = get_dataset(candidate.dataset)

    if dataset.data_family == "SAR":
        requirements = get_sar_analysis(index_name)
    else:
        index = get_index(index_name)
        requirements = index.required_bands

    band_resolutions = []

    for requirement in requirements:
        mapping = get_band_mapping(
            candidate.dataset,
            requirement.name,
        )

        band_resolutions.append(
            BandResolution(
                conceptual_band=requirement.name,
                dataset_band=mapping.dataset_bands[0],
                resolution_m=mapping.resolution_m,
            )
        )

    native_resolutions = {
        band.resolution_m
        for band in band_resolutions
    }

    analysis_resolution = min(native_resolutions)

    resampling_required = len(native_resolutions) > 1

    return AnalysisResolution(
        resolution_m=analysis_resolution,
        band_resolutions=band_resolutions,
        resampling_required=resampling_required,
    )



def score_spatial_resolution(
    candidate: DatasetCandidate,
    request: DatasetSelectionRequest,
) -> float:
    """Score how well the analysis resolution matches the requested scale."""


    dataset = get_dataset(candidate.dataset)

    if dataset.data_family in {"PRECIPITATION", "CLIMATE"}:
        resolution = min(dataset.spatial_resolutions_m)
    else:
        analysis = get_analysis_resolution(
            candidate,
            request.analysis_type,
        )

        resolution = analysis.resolution_m


    if request.spatial_scale == "local":
        return 1.0 if resolution <= 10 else 0.5

    if request.spatial_scale == "city":
        return 1.0 if resolution <= 30 else 0.7

    if request.spatial_scale == "regional":
        return 1.0 if resolution <= 30 else 0.8

    if request.spatial_scale == "continental":
        return 1.0 if resolution <= 250 else 0.8

    if request.spatial_scale == "global":
        return 1.0

    return 0.5


TEMPORAL_REQUIREMENT_DAYS = {
    "daily": 1,
    "weekly": 7,
    "monthly": 30,
    "seasonal": 90,
    "annual": 365,
}


def get_analysis_temporal_resolution(
    candidate: DatasetCandidate,
) -> AnalysisTemporalResolution:
    """
    Determine the temporal resolution for a candidate.

    Use product-level temporal information when a specific
    product is selected, otherwise use dataset-level information.
    """

    if candidate.product is not None:
        from core.product_registry import get_product

        product = get_product(candidate.product)

        if product.temporal_resolution_days is None:
            raise ValueError(
                f"No normalized temporal resolution available "
                f"for product {candidate.product}."
            )

        candidate.analysis_temporal_resolution = AnalysisTemporalResolution(
            resolution_days=product.temporal_resolution_days,
            source="product",
            description=product.temporal_resolution,
        )

        return candidate.analysis_temporal_resolution

    dataset = get_dataset(candidate.dataset)

    if (
        dataset.temporal_resolution_days is None
        or dataset.temporal_resolution is None
    ):
        raise ValueError(
            f"No temporal resolution information available "
            f"for dataset {candidate.dataset}."
        )

    candidate.analysis_temporal_resolution = AnalysisTemporalResolution(
        resolution_days=dataset.temporal_resolution_days,
        source="dataset",
        description=dataset.temporal_resolution,
    )

    return candidate.analysis_temporal_resolution


def score_temporal_suitability(
    candidate: DatasetCandidate,
    request: DatasetSelectionRequest,
) -> float:
    """Score how well a candidate's temporal resolution matches the request."""

    target_days = TEMPORAL_REQUIREMENT_DAYS.get(
        request.temporal_requirement.lower()
    )

    if target_days is None:
        return 0.5

    temporal = get_analysis_temporal_resolution(candidate)

    temporal_days = temporal.resolution_days

    if temporal_days <= target_days:
        return 1.0

    ratio = target_days / temporal_days

    if ratio >= 0.5:
        return 0.7

    if ratio >= 0.25:
        return 0.4

    return 0.2



def score_native_product_suitability(
    candidate: DatasetCandidate,
    request: DatasetSelectionRequest,
) -> float:
    """Score whether the candidate provides the requested analysis natively."""

    if candidate.pathway != "product":
        return 0.5

    if candidate.product is None:
        return 0.0

    product = get_product(candidate.product)

    analysis_type = request.analysis_type.lower()

    supported_indices = [
        index.lower()
        for index in product.supported_indices
    ]

    measurements = [
        measurement.lower()
        for measurement in product.measurements
    ]

    if (
        analysis_type in supported_indices
        or analysis_type in measurements
    ):
        return 1.0

    return 0.0


def score_spectral_suitability(
    candidate: DatasetCandidate,
    request: DatasetSelectionRequest,
) -> float:
    """Score how well the candidate provides the required analysis bands."""

    if candidate.pathway == "product":
        return 1.0

    dataset = get_dataset(candidate.dataset)

    if dataset.data_family == "SAR":
        requirements = get_sar_analysis(request.analysis_type)
    else:
        index = get_index(request.analysis_type)
        requirements = index.required_bands

    available_bands = 0

    for requirement in requirements:
        try:
            get_band_mapping(
                candidate.dataset,
                requirement.name,
            )
            available_bands += 1
        except ValueError:
            continue

    if not requirements:
        return 0.0

    coverage = available_bands / len(requirements)

    if coverage == 1.0:
        return 1.0

    return 0.0


def score_computational_suitability(
    candidate: DatasetCandidate,
    request: DatasetSelectionRequest,
) -> float:
    """Score the expected computational simplicity of a candidate."""

    # Existing derived product, minimal processing required
    if candidate.pathway == "product":
        return 1.0

    dataset = get_dataset(candidate.dataset)

    # Climate and precipitation datasets are generally simpler
    # to process than multispectral or SAR band calculations.
    if dataset.data_family in {"CLIMATE", "PRECIPITATION"}:
        return 1.0

    # Calculated optical or SAR analysis requires band processing.
    analysis = get_analysis_resolution(
        candidate,
        request.analysis_type,
    )

    # Resampling multiple native resolutions adds computational work.
    if analysis.resampling_required:
        return 0.5

    return 0.7



def rank_dataset_candidate(
    candidate: DatasetCandidate,
    request: DatasetSelectionRequest,
) -> DatasetRanking:
    """Calculate the overall suitability score for a dataset candidate."""

    spatial_score = score_spatial_resolution(
        candidate,
        request,
    )

    temporal_score = score_temporal_suitability(
        candidate,
        request,
    )

    native_product_score = score_native_product_suitability(
        candidate,
        request,
    )

    spectral_score = score_spectral_suitability(
        candidate,
        request,
    )

    computational_score = score_computational_suitability(
        candidate,
        request,
    )

    total_score = (
        spatial_score * SPATIAL_WEIGHT
        + temporal_score * TEMPORAL_WEIGHT
        + native_product_score * NATIVE_WEIGHT
        + spectral_score * SPECTRAL_WEIGHT
        + computational_score * COMPUTATIONAL_WEIGHT
    )

    rationale = (
        f"Spatial suitability: {spatial_score:.2f}, "
        f"temporal suitability: {temporal_score:.2f}, "
        f"native product suitability: {native_product_score:.2f}, "
        f"spectral suitability: {spectral_score:.2f}, "
        f"computational suitability: {computational_score:.2f}."
    )

    return DatasetRanking(
        candidate=candidate,
        spatial_score=spatial_score,
        temporal_score=temporal_score,
        native_product_score=native_product_score,
        spectral_score=spectral_score,
        computational_score=computational_score,
        total_score=total_score,
        rationale=rationale,
    )


def rank_dataset_candidates(
    candidates: list[DatasetCandidate],
    request: DatasetSelectionRequest,
) -> list[DatasetRanking]:
    """Rank multiple dataset candidates from highest to lowest suitability."""

    rankings = [
        rank_dataset_candidate(candidate, request)
        for candidate in candidates
        if candidate.eligible
    ]

    rankings.sort(
        key=lambda ranking: ranking.total_score,
        reverse=True,
    )

    return rankings

