from core.product_registry import get_products_for_dataset
from core.schemas import DatasetSelectionRequest
from core.dataset_registry import DATASETS
from core.band_mapping import get_band_mapping


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
) -> list[str]:
    """
    Return products belonging to datasets that satisfy
    the hard requirements of a selection request.
    """

    eligible_datasets = get_eligible_datasets(request)

    products = []

    for dataset_name in eligible_datasets:
        for product in get_products_for_dataset(dataset_name):
            products.append(product.product_id)

    return products