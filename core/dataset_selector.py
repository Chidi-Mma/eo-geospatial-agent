from core.product_registry import get_products_for_dataset
from core.schemas import (
    DatasetSelectionRequest,
    DatasetCandidate,
    DatasetRanking,
)
from core.dataset_registry import DATASETS
from core.band_mapping import get_band_mapping
from core.dataset_ranker import rank_dataset_candidates


def is_dataset_eligible(
    dataset_name: str,
    request: DatasetSelectionRequest,
) -> bool:
    """
    Determine whether a dataset satisfies the hard requirements
    of a dataset selection request.
    """

    if dataset_name not in DATASETS:
        return False

    dataset = DATASETS[dataset_name]

    # Check data family
    if dataset.data_family != request.data_family:
        return False

    # Check spatial scale
    if request.spatial_scale not in dataset.recommended_scales:
        return False


    # Check requested variables
    if request.required_variables:
        available_variables = {
            variable.lower()
            for variable in dataset.variables
        }

        requested_variables = {
            variable.lower()
            for variable in request.required_variables
        }

        if not requested_variables.issubset(available_variables):
            return False


     # Check required bands or polarizations
    for band in request.required_bands:
        try:
            get_band_mapping(dataset_name, band)
        except ValueError:
            return False

    # Check required variables
    for variable in request.required_variables:
        if not dataset_has_variable(
            dataset_name,
            variable,
        ):
            return False

    return True
    

def dataset_has_variable(
    dataset_name: str,
    variable_name: str,
) -> bool:
    """Return whether a dataset provides the requested variable."""

    if dataset_name not in DATASETS:
        return False

    dataset = DATASETS[dataset_name]

    return variable_name.lower() in [
        variable.lower()
        for variable in dataset.variables
    ]


def get_eligible_datasets(
    request: DatasetSelectionRequest,
) -> list[str]:
    """
    Return all datasets that satisfy the hard requirements.
    """

    return [
        dataset_name
        for dataset_name in DATASETS
        if is_dataset_eligible(dataset_name, request)
    ]



def product_is_suitable_for_request(
    product,
    request: DatasetSelectionRequest,
) -> bool:
    """
    Determine whether a product is suitable for the requested analysis.

    Spectral-index requests are matched through supported indices.
    Climate and precipitation products are matched through their
    measurements and temporal resolution.
    """

    # Spectral-index products
    if request.data_family == "OPTICAL":
        return product_is_suitable_for_index(
            product.product_id,
            request.analysis_type,
        )

    # Climate and precipitation products
    if request.data_family in {"CLIMATE", "PRECIPITATION"}:

        # Check that the requested analysis is represented
        # by the product measurements.
        if request.analysis_type.lower() not in [
            measurement.lower()
            for measurement in product.measurements
        ]:
            return False

        # Check temporal compatibility when the request specifies one.
        if request.temporal_requirement:
            requested_temporal = request.temporal_requirement.lower()

            temporal_days = {
                "daily": 1.0,
                "weekly": 7.0,
                "monthly": 30.0,
                "seasonal": 90.0,
                "annual": 365.0,
            }

            requested_days = temporal_days.get(requested_temporal)

            if (
                requested_days is not None
                and product.temporal_resolution_days is not None
            ):
                if product.temporal_resolution_days > requested_days:
                    return False

        return True

    return False


def get_eligible_products(
    request: DatasetSelectionRequest,
) -> list[DatasetCandidate]:
    """
    Return structured candidates that can satisfy the request
    through native products or band-based calculation.
    """

    candidates = []

    for dataset_name in DATASETS:

        dataset = DATASETS[dataset_name]

        # Data family must match
        if dataset.data_family != request.data_family:
            continue

        # Spatial scale must match
        if request.spatial_scale not in dataset.recommended_scales:
            continue


        # Requested variables must be available
        if request.required_variables:
            available_variables = {
                variable.lower()
                for variable in dataset.variables
            }

            requested_variables = {
                variable.lower()
                for variable in request.required_variables
            }

            if not requested_variables.issubset(available_variables):
                continue

        # Pathway 1, native product
        for product in get_products_for_dataset(dataset_name):

            if product_is_suitable_for_request(
                product,
                request,
            ):
                candidates.append(
                    DatasetCandidate(
                        dataset=dataset_name,
                        product=product.product_id,
                        pathway="product",
                    )
                )

        # Pathway 2, calculate from bands
        if dataset_can_satisfy_analysis(
            dataset_name,
            request.analysis_type,
        ):
            candidates.append(
                DatasetCandidate(
                    dataset=dataset_name,
                    product=None,
                    pathway="calculated",
                )
            )

    return candidates


def product_is_suitable_for_index(
    product_id: str,
    index_name: str,
) -> bool:
    """
    Determine whether a product can satisfy an index request,
    either by providing the index directly or through its
    available band mappings.
    """

    from core.product_registry import product_supports_index

    # First, check whether the product provides the index directly.
    if product_supports_index(product_id, index_name):
        return True

    return False


def dataset_can_satisfy_analysis(
    dataset_name: str,
    analysis_name: str,
) -> bool:
    """
    Determine whether a dataset can satisfy an analysis request.
    """

    dataset = DATASETS[dataset_name]
    analysis_name = analysis_name.lower()

    # Climate and precipitation analyses are variable based.
    if dataset.data_family in {"CLIMATE", "PRECIPITATION"}:
        return analysis_name in [
            variable.lower()
            for variable in dataset.variables
        ]

    # SAR analyses are polarization based.
    if dataset.data_family == "SAR":
        from core.registry import get_sar_analysis

        try:
            requirements = get_sar_analysis(analysis_name)
        except ValueError:
            return False

        for requirement in requirements:
            try:
                get_band_mapping(
                    dataset_name,
                    requirement.name,
                )
            except ValueError:
                return False

        return True

    # Optical spectral indices are band based.
    from core.registry import get_index

    try:
        index = get_index(analysis_name)
    except ValueError:
        return False

    for requirement in index.required_bands:
        try:
            get_band_mapping(
                dataset_name,
                requirement.name,
            )
        except ValueError:
            return False

    return True


def select_datasets(
    request: DatasetSelectionRequest,
) -> list[DatasetRanking]:
    """Return eligible dataset candidates ranked by suitability."""

    candidates = get_eligible_products(request)

    return rank_dataset_candidates(
        candidates,
        request,
    )

def select_best_dataset(
    request: DatasetSelectionRequest,
) -> DatasetRanking | None:
    """Return the highest-ranked dataset for a selection request."""

    rankings = select_datasets(request)

    if not rankings:
        return None

    return rankings[0]