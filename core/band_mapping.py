from core.schemas import BandMapping, IndexBandMapping


BAND_MAPPINGS: list[BandMapping] = [

    # Sentinel-2
    BandMapping(
        datasets=["Sentinel-2"],
        conceptual_band="BLUE",
        dataset_bands=["B02"],
        description="Sentinel-2 Band 2, blue, approximately 490 nm.",
    ),

    BandMapping(
        datasets=["Sentinel-2"],
        conceptual_band="GREEN",
        dataset_bands=["B03"],
        description="Sentinel-2 Band 3, green, approximately 560 nm.",
    ),

    BandMapping(
        datasets=["Sentinel-2"],
        conceptual_band="RED",
        dataset_bands=["B04"],
        description="Sentinel-2 Band 4, red, approximately 665 nm.",
    ),

    BandMapping(
        datasets=["Sentinel-2"],
        conceptual_band="RED_EDGE",
        dataset_bands=["B05", "B06", "B07", "B8A"],
        description="Sentinel-2 red-edge and narrow NIR bands.",
    ),

    BandMapping(
        datasets=["Sentinel-2"],
        conceptual_band="NIR",
        dataset_bands=["B08", "B8A"],
        description="Sentinel-2 near infrared bands.",
    ),

    BandMapping(
        datasets=["Sentinel-2"],
        conceptual_band="SWIR1",
        dataset_bands=["B11"],
        description="Sentinel-2 Band 11, shortwave infrared.",
    ),

    BandMapping(
        datasets=["Sentinel-2"],
        conceptual_band="SWIR2",
        dataset_bands=["B12"],
        description="Sentinel-2 Band 12, shortwave infrared.",
    ),

    # Landsat 8/9
    BandMapping(
        datasets=["Landsat-8", "Landsat-9"],
        conceptual_band="BLUE",
        dataset_bands=["B2"],
        description="Landsat 8/9 Band 2, blue.",
    ),

    BandMapping(
        datasets=["Landsat-8", "Landsat-9"],
        conceptual_band="GREEN",
        dataset_bands=["B3"],
        description="Landsat 8/9 Band 3, green.",
    ),

    BandMapping(
        datasets=["Landsat-8", "Landsat-9"],
        conceptual_band="RED",
        dataset_bands=["B4"],
        description="Landsat 8/9 Band 4, red.",
    ),

    BandMapping(
        datasets=["Landsat-8", "Landsat-9"],
        conceptual_band="NIR",
        dataset_bands=["B5"],
        description="Landsat 8/9 Band 5, near infrared.",
    ),

    BandMapping(
        datasets=["Landsat-8", "Landsat-9"],
        conceptual_band="SWIR1",
        dataset_bands=["B6"],
        description="Landsat 8/9 Band 6, shortwave infrared.",
    ),

    BandMapping(
        datasets=["Landsat-8", "Landsat-9"],
        conceptual_band="SWIR2",
        dataset_bands=["B7"],
        description="Landsat 8/9 Band 7, shortwave infrared.",
    ),


        # HLS
    BandMapping(
        datasets=["HLS"],
        conceptual_band="BLUE",
        dataset_bands=["B02"],
        description="HLS blue band, harmonized Sentinel-2/Landsat reflectance.",
    ),

    BandMapping(
        datasets=["HLS"],
        conceptual_band="GREEN",
        dataset_bands=["B03"],
        description="HLS green band, harmonized Sentinel-2/Landsat reflectance.",
    ),

    BandMapping(
        datasets=["HLS"],
        conceptual_band="RED",
        dataset_bands=["B04"],
        description="HLS red band, harmonized Sentinel-2/Landsat reflectance.",
    ),

    BandMapping(
        datasets=["HLS"],
        conceptual_band="NIR",
        dataset_bands=["B05"],
        description="HLS near infrared band.",
    ),

    BandMapping(
        datasets=["HLS"],
        conceptual_band="SWIR1",
        dataset_bands=["B06"],
        description="HLS shortwave infrared band 1.",
    ),

    BandMapping(
        datasets=["HLS"],
        conceptual_band="SWIR2",
        dataset_bands=["B07"],
        description="HLS shortwave infrared band 2.",
    ),


        # Sentinel-1 SAR polarizations
    BandMapping(
        datasets=["Sentinel-1"],
        conceptual_band="VV",
        dataset_bands=["VV"],
        description=(
            "Sentinel-1 C-band SAR VV polarization, "
            "vertical transmit and vertical receive."
        ),
    ),

    BandMapping(
        datasets=["Sentinel-1"],
        conceptual_band="VH",
        dataset_bands=["VH"],
        description=(
            "Sentinel-1 C-band SAR VH polarization, "
            "vertical transmit and horizontal receive."
        ),
    ),

    BandMapping(
        datasets=["Sentinel-1"],
        conceptual_band="HH",
        dataset_bands=["HH"],
        description=(
            "Sentinel-1 C-band SAR HH polarization, "
            "horizontal transmit and horizontal receive."
        ),
    ),

    BandMapping(
        datasets=["Sentinel-1"],
        conceptual_band="HV",
        dataset_bands=["HV"],
        description=(
            "Sentinel-1 C-band SAR HV polarization, "
            "horizontal transmit and vertical receive."
        ),
    ),
]


INDEX_BAND_MAPPINGS: list[IndexBandMapping] = [

    IndexBandMapping(
        index="NDVI",
        dataset="Sentinel-2",
        band_mapping={
            "NIR": "B08",
            "RED": "B04",
        },
        rationale="Standard Sentinel-2 NDVI using Band 8 NIR and Band 4 red.",
    ),

    IndexBandMapping(
        index="NDVI",
        dataset="Landsat-8",
        band_mapping={
            "NIR": "B5",
            "RED": "B4",
        },
        rationale="Landsat 8 NDVI using Band 5 NIR and Band 4 red.",
    ),

    IndexBandMapping(
        index="NDVI",
        dataset="Landsat-9",
        band_mapping={
            "NIR": "B5",
            "RED": "B4",
        },
        rationale="Landsat 9 NDVI using Band 5 NIR and Band 4 red.",
    ),

    IndexBandMapping(
        index="NDMI",
        dataset="Sentinel-2",
        band_mapping={
            "NIR": "B08",
            "SWIR1": "B11",
        },
        rationale="Sentinel-2 NDMI using Band 8 NIR and Band 11 SWIR.",
    ),

    IndexBandMapping(
        index="NDMI",
        dataset="Landsat-8",
        band_mapping={
            "NIR": "B5",
            "SWIR1": "B6",
        },
        rationale="Landsat 8 NDMI using Band 5 NIR and Band 6 SWIR1.",
    ),

    IndexBandMapping(
        index="NDMI",
        dataset="Landsat-9",
        band_mapping={
            "NIR": "B5",
            "SWIR1": "B6",
        },
        rationale="Landsat 9 NDMI using Band 5 NIR and Band 6 SWIR1.",
    ),

    IndexBandMapping(
        index="NDRE",
        dataset="Sentinel-2",
        band_mapping={
            "NIR": "B08",
            "RED_EDGE": "B05",
        },
        rationale=(
            "Sentinel-2 NDRE using Band 8 NIR and Band 5 "
            "red-edge reflectance."
        ),
    ),
]


def get_band_mapping(
    dataset: str,
    conceptual_band: str,
) -> BandMapping:
    """Return the mapping for a conceptual band and dataset."""

    conceptual_band = conceptual_band.upper()

    for mapping in BAND_MAPPINGS:
        if (
            dataset in mapping.datasets
            and mapping.conceptual_band == conceptual_band
        ):
            return mapping

    raise ValueError(
        f"No mapping found for {conceptual_band} "
        f"in {dataset}."
    )


def get_dataset_band_mappings(
    dataset: str,
) -> list[BandMapping]:
    """Return all band mappings available for a dataset."""

    return [
        mapping
        for mapping in BAND_MAPPINGS
        if dataset in mapping.datasets
    ]


def check_index_compatibility(
    index_name: str,
    dataset_name: str,
) -> dict:
    """
    Check whether a spectral index can be calculated
    using a particular dataset.
    """

    from core.registry import get_index
    

    index = get_index(index_name)

    if dataset_name not in index.compatible_datasets:
        return {
            "compatible": False,
            "index": index.name,
            "dataset": dataset_name,
            "reason": (
                f"{index.name} is not registered as compatible "
                f"with {dataset_name}."
            ),
            "bands": {},
        }

    bands = {}

    for requirement in index.required_bands:
        try:
            mapping = get_band_mapping(
                dataset_name,
                requirement.name,
            )

            bands[requirement.name] = mapping.dataset_bands

        except ValueError:
            return {
                "compatible": False,
                "index": index.name,
                "dataset": dataset_name,
                "reason": (
                    f"The dataset does not provide a mapping "
                    f"for required band: {requirement.name}."
                ),
                "bands": bands,
            }

    return {
        "compatible": True,
        "index": index.name,
        "dataset": dataset_name,
        "reason": "All required bands are available.",
        "bands": bands,
    }


def get_index_band_mapping(
    index: str,
    dataset: str,
) -> IndexBandMapping:
    """Return the specific bands used to calculate an index."""

    index = index.upper()

    for mapping in INDEX_BAND_MAPPINGS:
        if (
            mapping.index == index
            and mapping.dataset == dataset
        ):
            return mapping

    raise ValueError(
        f"No index-specific band mapping found for "
        f"{index} and {dataset}."
    )