from pydantic import BaseModel, Field
from typing import Literal


class BandRequirement(BaseModel):
    """Describes a spectral band required by an analysis."""

    name: str
    description: str


class SpectralIndex(BaseModel):
    """Defines a remote sensing spectral index."""

    name: str
    description: str
    formula: str
    required_bands: list[BandRequirement]
    compatible_datasets: list[str]


class DatasetBand(BaseModel):
    """Describes a spectral band available in a dataset."""

    name: str
    wavelength_nm: tuple[float, float] | None = None
    description: str


class BandMapping(BaseModel):
    """Maps a conceptual spectral band to one or more dataset-specific bands."""

    datasets: list[str]
    conceptual_band: Literal[
        "BLUE",
        "GREEN",
        "RED",
        "RED_EDGE",
        "NIR",
        "SWIR1",
        "SWIR2",
        "THERMAL",
        "VV",
        "VH",
        "HH",
        "HV",
    ]
    dataset_bands: list[str]
    description: str | None = None


class IndexBandMapping(BaseModel):
    """Defines the specific dataset bands used to calculate an index."""

    index: str
    dataset: str
    band_mapping: dict[str, str]
    rationale: str


class PreprocessingStep(BaseModel):
    """Defines one approved preprocessing operation."""

    operation: Literal[
        "SCALE",
        "CLOUD_MASK",
        "CLOUD_SHADOW_MASK",
        "BAND_SELECTION",
        "RESAMPLE",
        "REPROJECT",
        "CLIP",
        "TEMPORAL_COMPOSITE",
        "NODATA_MASK",
        "SPECKLE_FILTER",
        "ORBIT_CORRECTION",
        "THERMAL_NOISE_REMOVAL",
        "RADIOMETRIC_CALIBRATION",
        "TERRAIN_CORRECTION",
    ]

    description: str
    required: bool = False
    parameters: dict[str, str | int | float | bool] = Field(
        default_factory=dict
    )


class PreprocessingPipeline(BaseModel):
    """Defines an ordered preprocessing workflow."""

    dataset: str

    data_family: Literal[
        "OPTICAL",
        "SAR",
        "CLIMATE",
        "PRECIPITATION",
    ]

    steps: list[PreprocessingStep]

    rationale: str

class Dataset(BaseModel):
    """Describes an Earth observation or geospatial dataset."""

    name: str
    provider: str
    data_type: Literal["raster", "vector", "climate"]

    data_family: Literal[
    "OPTICAL",
    "SAR",
    "CLIMATE",
    "PRECIPITATION",
    ]

    spatial_resolutions_m: list[float] = Field(default_factory=list)
    temporal_resolution: str | None = None

    coverage: str | None = None
    access_method: str | None = None

    bands: list[DatasetBand] = Field(default_factory=list)

    typical_use_cases: list[str] = Field(default_factory=list)
    recommended_scales: list[
        Literal[
            "local",
            "city",
            "regional",
            "continental",
            "global",
        ]
    ] = Field(default_factory=list)

    description: str


class DatasetSelectionRequest(BaseModel):
    """Structured requirements for selecting an appropriate dataset."""

    analysis_type: str
    data_family: Literal[
        "OPTICAL",
        "SAR",
        "CLIMATE",
        "PRECIPITATION",
    ]

    spatial_scale: Literal[
        "local",
        "city",
        "regional",
        "continental",
        "global",
    ]

    temporal_requirement: str

    required_bands: list[str] = []

    required_variables: list[str] = []

    preferred_resolution_m: int | None = None

    description: str | None = None


class Product(BaseModel):
    """Metadata describing a specific Earth observation or climate product."""

    product_id: str
    dataset: str
    provider: str

    description: str

    spatial_resolution_m: int | None = None
    temporal_resolution: str

    measurements: list[str]

    supported_indices: list[str] = []

    access_method: str

    access_reference: str | None = None