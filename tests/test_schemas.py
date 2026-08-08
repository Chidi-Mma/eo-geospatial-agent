from core.schemas import BandRequirement, SpectralIndex


def test_spectral_index_schema():
    ndvi = SpectralIndex(
        name="NDVI",
        description="Normalized Difference Vegetation Index",
        formula="(NIR - RED) / (NIR + RED)",
        required_bands=[
            BandRequirement(
                name="NIR",
                description="Near infrared"
            ),
            BandRequirement(
                name="RED",
                description="Red"
            )
        ],
        compatible_datasets=[
            "Sentinel-2",
            "Landsat-8",
            "Landsat-9",
            "MODIS"
        ]
    )

    assert ndvi.name == "NDVI"
    assert len(ndvi.required_bands) == 2