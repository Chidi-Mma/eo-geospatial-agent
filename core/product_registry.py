from core.schemas import Product


PRODUCTS: dict[str, Product] = {

    "MOD13Q1.061": Product(
        product_id="MOD13Q1.061",
        dataset="MODIS",
        provider="NASA",
        description=(
            "MODIS/Terra Vegetation Indices 16-Day "
            "L3 Global 250 m product."
        ),
        spatial_resolution_m=250,
        temporal_resolution="16-day",
        measurements=[
            "NDVI",
            "EVI",
            "RED",
            "NIR",
            "QA",
        ],
        supported_indices=[
            "NDVI",
            "EVI",
        ],
        access_method="Earth Engine",
    ),

}


def get_product(product_id: str) -> Product:
    """Return a product by ID."""

    if product_id not in PRODUCTS:
        raise ValueError(
            f"Unknown product: {product_id}. "
            f"Available products: {', '.join(PRODUCTS.keys())}"
        )

    return PRODUCTS[product_id]


def list_products() -> list[str]:
    """Return the IDs of all available products."""

    return list(PRODUCTS.keys())


def get_products_for_dataset(dataset_name: str) -> list[Product]:
    """Return all products belonging to a dataset."""

    return [
        product
        for product in PRODUCTS.values()
        if product.dataset == dataset_name
    ]


def product_supports_index(
    product_id: str,
    index_name: str,
) -> bool:
    """Return whether a product directly provides an index."""

    product = get_product(product_id)

    return index_name.upper() in [
        index.upper()
        for index in product.supported_indices
    ]