from core.schemas import BandRequirement, SpectralIndex


SPECTRAL_INDICES: dict[str, SpectralIndex] = {

    "NDVI": SpectralIndex(
        name="NDVI",
        description="Normalized Difference Vegetation Index, commonly used to assess vegetation greenness and vigor.",
        formula="(NIR - RED) / (NIR + RED)",
        required_bands=[
            BandRequirement(
                name="NIR",
                description="Near infrared"
            ),
            BandRequirement(
                name="RED",
                description="Red"
            ),
        ],
        compatible_datasets=[
            "Sentinel-2",
            "Landsat-8",
            "Landsat-9",
            "MODIS",
            "HLS",
        ],
    ),

    "EVI": SpectralIndex(
        name="EVI",
        description="Enhanced Vegetation Index, designed to improve vegetation sensitivity in high biomass areas and reduce some atmospheric and background effects.",
        formula="2.5 * (NIR - RED) / (NIR + 6*RED - 7.5*BLUE + 1)",
        required_bands=[
            BandRequirement(
                name="NIR",
                description="Near infrared"
            ),
            BandRequirement(
                name="RED",
                description="Red"
            ),
            BandRequirement(
                name="BLUE",
                description="Blue"
            ),
        ],
        compatible_datasets=[
            "Sentinel-2",
            "Landsat-8",
            "Landsat-9",
            "MODIS",
            "HLS",
        ],
    ),

    "NDRE": SpectralIndex(
        name="NDRE",
        description="Normalized Difference Red Edge Index, useful for assessing vegetation chlorophyll and plant stress.",
        formula="(NIR - RED_EDGE) / (NIR + RED_EDGE)",
        required_bands=[
            BandRequirement(
                name="NIR",
                description="Near infrared"
            ),
            BandRequirement(
                name="RED_EDGE",
                description="Red edge"
            ),
        ],
        compatible_datasets=[
            "Sentinel-2",
            "HLS",
        ],
    ),

    "NDMI": SpectralIndex(
        name="NDMI",
        description="Normalized Difference Moisture Index, commonly used to assess vegetation water content.",
        formula="(NIR - SWIR1) / (NIR + SWIR1)",
        required_bands=[
            BandRequirement(
                name="NIR",
                description="Near infrared"
            ),
            BandRequirement(
                name="SWIR1",
                description="Shortwave infrared"
            ),
        ],
        compatible_datasets=[
            "Sentinel-2",
            "Landsat-8",
            "Landsat-9",
            "HLS",
        ],
    ),

    "NDWI": SpectralIndex(
        name="NDWI",
        description="Normalized Difference Water Index, commonly used to identify and monitor surface water.",
        formula="(GREEN - NIR) / (GREEN + NIR)",
        required_bands=[
            BandRequirement(
                name="GREEN",
                description="Green"
            ),
            BandRequirement(
                name="NIR",
                description="Near infrared"
            ),
        ],
        compatible_datasets=[
            "Sentinel-2",
            "Landsat-8",
            "Landsat-9",
            "MODIS",
            "HLS",
        ],
    ),

    "NBR": SpectralIndex(
        name="NBR",
        description="Normalized Burn Ratio, commonly used for burn severity and fire disturbance assessment.",
        formula="(NIR - SWIR2) / (NIR + SWIR2)",
        required_bands=[
            BandRequirement(
                name="NIR",
                description="Near infrared"
            ),
            BandRequirement(
                name="SWIR2",
                description="Shortwave infrared 2"
            ),
        ],
        compatible_datasets=[
            "Sentinel-2",
            "Landsat-8",
            "Landsat-9",
            "HLS",
        ],
    ),

    "GNDVI": SpectralIndex(
        name="GNDVI",
        description="Green Normalized Difference Vegetation Index, sensitive to vegetation chlorophyll and nitrogen-related characteristics.",
        formula="(NIR - GREEN) / (NIR + GREEN)",
        required_bands=[
            BandRequirement(
                name="NIR",
                description="Near infrared"
            ),
            BandRequirement(
                name="GREEN",
                description="Green"
            ),
        ],
        compatible_datasets=[
            "Sentinel-2",
            "Landsat-8",
            "Landsat-9",
            "MODIS",
            "HLS",
        ],
    ),

    "SAVI": SpectralIndex(
        name="SAVI",
        description="Soil Adjusted Vegetation Index, designed to reduce the influence of soil brightness in areas with sparse vegetation.",
        formula="((NIR - RED) / (NIR + RED + L)) * (1 + L)",
        required_bands=[
            BandRequirement(
                name="NIR",
                description="Near infrared"
            ),
            BandRequirement(
                name="RED",
                description="Red"
            ),
        ],
        compatible_datasets=[
            "Sentinel-2",
            "Landsat-8",
            "Landsat-9",
            "MODIS",
            "HLS",
        ],
    ),

}


def get_index(index_name: str) -> SpectralIndex:
    """Return a spectral index by name."""

    index_name = index_name.upper()

    if index_name not in SPECTRAL_INDICES:
        raise ValueError(
            f"Unknown spectral index: {index_name}. "
            f"Available indices: {', '.join(SPECTRAL_INDICES.keys())}"
        )

    return SPECTRAL_INDICES[index_name]


def list_indices() -> list[str]:
    """Return the names of all available spectral indices."""

    return list(SPECTRAL_INDICES.keys())



SAR_ANALYSES = {
    "soil_moisture": [
        BandRequirement(
            name="VV",
            description="Vertical transmit, vertical receive SAR polarization",
        ),
        BandRequirement(
            name="VH",
            description="Vertical transmit, horizontal receive SAR polarization",
        ),
    ],
}


def get_sar_analysis(name: str) -> list[BandRequirement]:
    key = name.lower()

    if key not in SAR_ANALYSES:
        raise ValueError(
            f"Unknown SAR analysis: {name}. "
            f"Available analyses: {', '.join(SAR_ANALYSES)}"
        )

    return SAR_ANALYSES[key]

