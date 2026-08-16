from core.schemas import Dataset


DATASETS: dict[str, Dataset] = {

    "Sentinel-2": Dataset(
        name="Sentinel-2",
        data_family="OPTICAL",
        provider="Copernicus / European Space Agency",
        data_type="raster",
        spatial_resolutions_m=[10, 20, 60],
        temporal_resolution="approximately 5 days at the equator",
        temporal_resolution_days=5,
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

    "Landsat-8": Dataset(
        name="Landsat-8",
        provider="NASA / USGS",
        data_family="OPTICAL",
        data_type="raster",
        spatial_resolutions_m=[15, 30, 100],
        temporal_resolution="16 days",
        temporal_resolution_days=16,
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
            "Landsat 8 multispectral and thermal Earth observation "
            "data with a long historical record suitable for "
            "environmental monitoring and change detection."
        ),
    ),

    "Landsat-9": Dataset(
        name="Landsat-9",
        data_family="OPTICAL",
        provider="NASA / USGS",
        data_type="raster",
        spatial_resolutions_m=[15, 30, 100],
        temporal_resolution="16 days",
        temporal_resolution_days=16,
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
            "Landsat 9 multispectral and thermal Earth observation "
            "data suitable for environmental monitoring and "
            "change detection."
        ),
    ),
    "MODIS": Dataset(
        name="MODIS",
        data_family="OPTICAL",
        provider="NASA",
        data_type="raster",
        spatial_resolutions_m=[250, 500, 1000],
        temporal_resolution="daily to 16 days, depending on product",
        temporal_resolution_days=None,
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
        data_family="OPTICAL",
        provider="NASA",
        data_type="raster",
        spatial_resolutions_m=[30],
        temporal_resolution="approximately 2 to 3 days globally, depending on location",
        temporal_resolution_days=2.5,
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


    "Sentinel-1": Dataset(
        name="Sentinel-1",
        provider="Copernicus / European Space Agency",
        data_type="raster",
        data_family="SAR",
        spatial_resolutions_m=[5, 10, 20],
        temporal_resolution="approximately 6 days with the Sentinel-1 constellation, depending on location and acquisition mode",
        temporal_resolution_days=6,
        coverage="Global",
        access_method="STAC",
        typical_use_cases=[
            "flood mapping",
            "soil moisture analysis",
            "vegetation structure analysis",
            "change detection",
            "wetland monitoring",
            "cloud-independent Earth observation",
        ],
        recommended_scales=[
            "local",
            "city",
            "regional",
        ],
        description=(
            "C-band synthetic aperture radar Earth observation data "
            "that can acquire imagery regardless of cloud cover or daylight."
        ),
    ),

      
    "ERA5": Dataset(
        name="ERA5",
        data_family="CLIMATE",
        provider="ECMWF / Copernicus Climate Change Service",
        data_type="climate",
        spatial_resolutions_m=[27800.0],
        temporal_resolution="hourly",
        temporal_resolution_days=1/24,
        coverage="Global",
        access_method="API",
        variables=[
            "temperature",
            "precipitation",
            "radiation",
            "wind",
        ],
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



    "ERA5-Land": Dataset(
    name="ERA5-Land",
    provider="ECMWF / Copernicus Climate Change Service",
    data_type="climate",
    data_family="CLIMATE",
    spatial_resolutions_m=[11100.0],
    temporal_resolution="hourly",
    temporal_resolution_days=1/24,
    coverage="Global",
    access_method="API",
    variables=[
        "temperature",
        "precipitation",
        "soil_moisture",
        "evapotranspiration",
    ],
    typical_use_cases=[
        "land-surface temperature analysis",
        "soil moisture analysis",
        "evapotranspiration analysis",
        "drought analysis",
        "agricultural monitoring",
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
        "High-resolution land-surface reanalysis data providing "
        "hourly historical estimates of land and hydrological variables."
    ),
),



"CHIRPS": Dataset(
    name="CHIRPS",
    data_family="PRECIPITATION",
    provider="Climate Hazards Center, UC Santa Barbara",
    data_type="climate",
    spatial_resolutions_m=[5560.0],
    temporal_resolution="daily and monthly",
    temporal_resolution_days=None,
    coverage="50°S to 50°N",
    access_method="API",
    variables=[
        "precipitation",
    ],
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