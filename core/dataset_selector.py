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

    # Check required bands or polarizations
    for band in request.required_bands:
        try:
            get_band_mapping(dataset_name, band)
        except ValueError:
            return False

    return True


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

        # Pathway 1, native product
        for product in get_products_for_dataset(dataset_name):

            if product_is_suitable_for_index(
                product.product_id,
                request.analysis_type,
            ):
                candidates.append(
                    DatasetCandidate(
                        dataset=dataset_name,
                        product=product.product_id,
                        pathway="product",
                    )
                )

        # Pathway 2, calculate from bands
        if dataset_can_calculate_index(
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


def dataset_can_calculate_index(
    dataset_name: str,
    index_name: str,
) -> bool:
    """
    Determine whether an index can be calculated from
    the available band mappings for a dataset.
    """

    from core.registry import get_index

    index = get_index(index_name)

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