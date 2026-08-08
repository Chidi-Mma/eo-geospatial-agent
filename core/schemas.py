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


class Dataset(BaseModel):
    """Describes an Earth observation or geospatial dataset."""

    name: str
    provider: str
    data_type: Literal["raster", "vector", "climate"]

    spatial_resolution_m: float | None = None
    temporal_resolution: str | None = None

    bands: list[DatasetBand] = Field(default_factory=list)

    description: str