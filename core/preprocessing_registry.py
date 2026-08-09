from core.schemas import PreprocessingPipeline, PreprocessingStep

SENTINEL_2_PIPELINE = PreprocessingPipeline(
    dataset="Sentinel-2",
    data_family="OPTICAL",
    steps=[
        PreprocessingStep(
            operation="CLOUD_MASK",
            description="Mask cloudy pixels using the available quality information.",
            required=True,
        ),
        PreprocessingStep(
            operation="CLOUD_SHADOW_MASK",
            description="Mask pixels affected by cloud shadows.",
            required=True,
        ),
        PreprocessingStep(
            operation="BAND_SELECTION",
            description="Select the spectral bands required for the requested analysis.",
            required=True,
        ),
        PreprocessingStep(
            operation="RESAMPLE",
            description="Resample bands to a common spatial resolution when required.",
            parameters={
                "target_resolution": 10,
                "method": "bilinear",
            },
        ),
        PreprocessingStep(
            operation="CLIP",
            description="Clip the imagery to the user's area of interest.",
            required=True,
        ),
        PreprocessingStep(
            operation="NODATA_MASK",
            description="Handle pixels with missing or invalid observations.",
        ),
    ],
    rationale=(
        "Sentinel-2 preprocessing for optical remote sensing analysis. "
        "Cloud and cloud-shadow masking are applied before analysis, "
        "followed by band selection, spatial harmonization, AOI clipping, "
        "and nodata handling."
    ),
)


LANDSAT_PIPELINE = PreprocessingPipeline(
    dataset="Landsat-8/9",
    data_family="OPTICAL",
    steps=[
        PreprocessingStep(
            operation="CLOUD_MASK",
            description="Mask cloudy pixels using Landsat quality information.",
            required=True,
        ),
        PreprocessingStep(
            operation="CLOUD_SHADOW_MASK",
            description="Mask pixels affected by cloud shadows.",
            required=True,
        ),
        PreprocessingStep(
            operation="BAND_SELECTION",
            description="Select the spectral bands required for the requested analysis.",
            required=True,
        ),
        PreprocessingStep(
            operation="RESAMPLE",
            description="Resample bands to a common spatial resolution when required.",
            parameters={
                "target_resolution": 30,
                "method": "bilinear",
            },
        ),
        PreprocessingStep(
            operation="CLIP",
            description="Clip the imagery to the user's area of interest.",
            required=True,
        ),
        PreprocessingStep(
            operation="NODATA_MASK",
            description="Handle pixels with missing or invalid observations.",
        ),
    ],
    rationale=(
        "Landsat 8/9 preprocessing for optical remote sensing analysis. "
        "Cloud and cloud-shadow masking are applied before analysis, "
        "followed by band selection, spatial harmonization, AOI clipping, "
        "and nodata handling."
    ),
)


MODIS_PIPELINE = PreprocessingPipeline(
    dataset="MODIS",
    data_family="OPTICAL",
    steps=[
        PreprocessingStep(
            operation="CLOUD_MASK",
            description="Mask cloudy pixels using MODIS quality information.",
            required=True,
        ),
        PreprocessingStep(
            operation="BAND_SELECTION",
            description="Select the MODIS bands required for the requested analysis.",
            required=True,
        ),
        PreprocessingStep(
            operation="RESAMPLE",
            description="Resample MODIS data when required for the analysis.",
            parameters={
                "method": "bilinear",
            },
        ),
        PreprocessingStep(
            operation="CLIP",
            description="Clip the imagery to the user's area of interest.",
            required=True,
        ),
        PreprocessingStep(
            operation="NODATA_MASK",
            description="Handle pixels with missing or invalid observations.",
        ),
        PreprocessingStep(
            operation="TEMPORAL_COMPOSITE",
            description="Create a temporal composite when multiple observations are available.",
            parameters={
                "method": "median",
            },
        ),
    ],
    rationale=(
        "MODIS preprocessing for regional and temporal environmental "
        "monitoring. Quality-based cloud masking is followed by band "
        "selection, optional spatial resampling, AOI clipping, nodata "
        "handling, and temporal compositing when required."
    ),
)


HLS_PIPELINE = PreprocessingPipeline(
    dataset="HLS",
    data_family="OPTICAL",
    steps=[
        PreprocessingStep(
            operation="CLOUD_MASK",
            description="Mask cloudy pixels using HLS quality information.",
            required=True,
        ),
        PreprocessingStep(
            operation="CLOUD_SHADOW_MASK",
            description="Mask pixels affected by cloud shadows.",
            required=True,
        ),
        PreprocessingStep(
            operation="BAND_SELECTION",
            description="Select the harmonized spectral bands required for the analysis.",
            required=True,
        ),
        PreprocessingStep(
            operation="RESAMPLE",
            description="Use the harmonized spatial resolution provided by HLS.",
            parameters={
                "target_resolution": 30,
                "method": "bilinear",
            },
        ),
        PreprocessingStep(
            operation="CLIP",
            description="Clip the imagery to the user's area of interest.",
            required=True,
        ),
        PreprocessingStep(
            operation="NODATA_MASK",
            description="Handle pixels with missing or invalid observations.",
        ),
        PreprocessingStep(
            operation="TEMPORAL_COMPOSITE",
            description="Create a temporal composite when multiple observations are available.",
            parameters={
                "method": "median",
            },
        ),
    ],
    rationale=(
        "HLS preprocessing for harmonized Landsat and Sentinel-2 analysis. "
        "Quality masking is followed by selection of harmonized bands, "
        "spatial handling, AOI clipping, nodata handling, and optional "
        "temporal compositing."
    ),
)


SENTINEL_1_PIPELINE = PreprocessingPipeline(
    dataset="Sentinel-1",
    data_family="SAR",
    steps=[
        PreprocessingStep(
            operation="ORBIT_CORRECTION",
            description="Apply precise or restituted orbit information to improve geolocation.",
            required=True,
        ),
        PreprocessingStep(
            operation="THERMAL_NOISE_REMOVAL",
            description="Remove thermal noise from the SAR backscatter data.",
            required=True,
        ),
        PreprocessingStep(
            operation="RADIOMETRIC_CALIBRATION",
            description="Convert SAR measurements to calibrated backscatter values.",
            required=True,
        ),
        PreprocessingStep(
            operation="SPECKLE_FILTER",
            description="Reduce speckle noise when appropriate for the requested analysis.",
        ),
        PreprocessingStep(
            operation="TERRAIN_CORRECTION",
            description="Correct terrain-related geometric and radiometric distortions.",
            required=True,
        ),
        PreprocessingStep(
            operation="CLIP",
            description="Clip the SAR imagery to the user's area of interest.",
            required=True,
        ),
        PreprocessingStep(
            operation="NODATA_MASK",
            description="Handle pixels with missing or invalid observations.",
        ),
    ],
    rationale=(
        "Sentinel-1 SAR preprocessing. Orbit correction, thermal noise "
        "removal, radiometric calibration, terrain correction, and AOI "
        "clipping prepare the imagery for radar-based analysis. Speckle "
        "filtering is optional because its suitability depends on the "
        "analysis and spatial detail required."
    ),
)


PREPROCESSING_PIPELINES = {
    "Sentinel-2": SENTINEL_2_PIPELINE,
    "Landsat-8": LANDSAT_PIPELINE,
    "Landsat-9": LANDSAT_PIPELINE,
    "MODIS": MODIS_PIPELINE,
    "HLS": HLS_PIPELINE,
    "Sentinel-1": SENTINEL_1_PIPELINE,
}

def get_preprocessing_pipeline(dataset: str) -> PreprocessingPipeline:
    """Return the registered preprocessing pipeline for a dataset."""

    try:
        return PREPROCESSING_PIPELINES[dataset]
    except KeyError:
        raise ValueError(
            f"No preprocessing pipeline registered for {dataset}."
        )


def is_operation_allowed(
    dataset: str,
    operation: str,
) -> bool:
    """Check whether an operation is approved for a dataset."""

    pipeline = get_preprocessing_pipeline(dataset)

    operation = operation.upper()

    return any(
        step.operation == operation
        for step in pipeline.steps
    )