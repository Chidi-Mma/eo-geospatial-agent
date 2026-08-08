from core.schemas import Dataset


DATASETS: dict[str, Dataset] = {

    "Sentinel-2": Dataset(
        name="Sentinel-2",
        provider="Copernicus / European Space Agency",
        data_type="raster",
        spatial_resolutions_m=[10, 20, 60],
        temporal_resolution="approximately 5 days at the equator",
        coverage="Global",
        access_method="STAC",
        typical_use_cases=[
            "vegetation monitoring",
            "crop monitoring",
            "land cover mapping",
            "water monitoring",
            "vegetation stress analysis",
            "spectral index calculation",
        ],
        recommended_scales=[
            "local",
            "city",
            "regional",
        ],
        description=(
            "Multispectral optical Earth observation data with "
            "high spatial resolution and multiple red-edge and "
            "shortwave infrared bands."
        ),
    ),

    "Landsat-8/9": Dataset(
        name="Landsat-8/9",
        provider="NASA / USGS",
        data_type="raster",
        spatial_resolutions_m=[15, 30, 100],
        temporal_resolution="16 days per satellite",
        coverage="Global",
        access_method="STAC",
        typical_use_cases=[
            "long-term vegetation monitoring",
            "land cover mapping",
            "change detection",
            "agricultural monitoring",
            "spectral index calculation",
        ],
        recommended_scales=[
            "local",
            "city",
            "regional",
            "continental",
        ],
        description=(
            "Multispectral and thermal Earth observation data "
            "with a long historical record suitable for environmental "
            "monitoring and change detection."
        ),
    ),

    "MODIS": Dataset(
        name="MODIS",
        provider="NASA",
        data_type="raster",
        spatial_resolutions_m=[250, 500, 1000],
        temporal_resolution="daily to 16 days, depending on product",
        coverage="Global",
        access_method="STAC",
        typical_use_cases=[
            "large-area vegetation monitoring",
            "long-term environmental monitoring",
            "regional analysis",
            "continental analysis",
            "global analysis",
        ],
        recommended_scales=[
            "regional",
            "continental",
            "global",
        ],
        description=(
            "Moderate-resolution Earth observation data with "
            "high temporal frequency and a long historical record."
        ),
    ),

    "HLS": Dataset(
        name="HLS",
        provider="NASA",
        data_type="raster",
        spatial_resolutions_m=[30],
        temporal_resolution="approximately 2 to 3 days globally, depending on location",
        coverage="Global",
        access_method="STAC",
        typical_use_cases=[
            "dense vegetation time series",
            "agricultural monitoring",
            "land cover monitoring",
            "change detection",
            "long-term Earth observation analysis",
        ],
        recommended_scales=[
            "local",
            "city",
            "regional",
            "continental",
        ],
        description=(
            "Harmonized Landsat and Sentinel-2 surface reflectance "
            "data providing a dense 30 m time series."
        ),
    ),

    "ERA5": Dataset(
        name="ERA5",
        provider="ECMWF / Copernicus Climate Change Service",
        data_type="climate",
        spatial_resolutions_m=[],
        temporal_resolution="hourly",
        coverage="Global",
        access_method="API",
        typical_use_cases=[
            "temperature analysis",
            "precipitation analysis",
            "radiation analysis",
            "wind analysis",
            "climate trend analysis",
            "environmental modelling",
        ],
        recommended_scales=[
            "local",
            "city",
            "regional",
            "continental",
            "global",
        ],
        description=(
            "Global atmospheric reanalysis data providing "
            "historical climate and weather variables."
        ),
    ),

    "CHIRPS": Dataset(
        name="CHIRPS",
        provider="Climate Hazards Center, UC Santa Barbara",
        data_type="climate",
        spatial_resolutions_m=[],
        temporal_resolution="daily and monthly",
        coverage="50°S to 50°N",
        access_method="API",
        typical_use_cases=[
            "precipitation monitoring",
            "drought analysis",
            "agricultural monitoring",
            "hydrological analysis",
            "climate variability analysis",
        ],
        recommended_scales=[
            "local",
            "city",
            "regional",
            "continental",
        ],
        description=(
            "High-resolution rainfall data combining satellite "
            "observations with in-situ station data."
        ),
    ),
}


def get_dataset(dataset_name: str) -> Dataset:
    """Return a dataset by name."""

    if dataset_name not in DATASETS:
        raise ValueError(
            f"Unknown dataset: {dataset_name}. "
            f"Available datasets: {', '.join(DATASETS.keys())}"
        )

    return DATASETS[dataset_name]


def list_datasets() -> list[str]:
    """Return the names of all available datasets."""

    return list(DATASETS.keys())