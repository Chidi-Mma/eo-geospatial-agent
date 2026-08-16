from core.schemas import (
    DatasetCandidate,
    DatasetRanking,
    DatasetSelectionRequest,

)

from core.dataset_ranker import (
    get_analysis_resolution,
    get_analysis_temporal_resolution,
    score_temporal_suitability,
    score_spatial_resolution,
    score_native_product_suitability,
    score_spectral_suitability,
    score_spatial_resolution,
    score_computational_suitability,
    rank_dataset_candidate,
    rank_dataset_candidates,
    
)

from core.dataset_ranker import (
    SPATIAL_WEIGHT,
    TEMPORAL_WEIGHT,
    NATIVE_WEIGHT,
    SPECTRAL_WEIGHT,
    COMPUTATIONAL_WEIGHT,
    rank_dataset_candidate,
)

from core.product_registry import get_product
from core.dataset_registry import get_dataset


def test_sentinel2_temporal_resolution():
    candidate = DatasetCandidate(
        dataset="Sentinel-2",
        pathway="calculated",
    )

    result = get_analysis_temporal_resolution(candidate)

    assert result.resolution_days == 5
    assert result.source == "dataset"


def test_modis_product_temporal_resolution():
    candidate = DatasetCandidate(
        dataset="MODIS",
        product="MOD13Q1.061",
        pathway="product",
    )

    result = get_analysis_temporal_resolution(candidate)

    assert result.resolution_days == 16
    assert result.source == "product"


def test_sentinel2_monthly_temporal_suitability():
    candidate = DatasetCandidate(
        dataset="Sentinel-2",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_temporal_suitability(candidate, request)

    assert score == 1.0


def test_sentinel2_daily_temporal_suitability():
    candidate = DatasetCandidate(
        dataset="Sentinel-2",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="daily",
    )

    score = score_temporal_suitability(candidate, request)

    assert score == 0.2


from core.band_mapping import (
    get_band_mapping,
    get_dataset_band_mappings,
)


def test_sentinel2_red_band_resolution():
    mapping = get_band_mapping("Sentinel-2", "RED")

    assert mapping.dataset_bands == ["B04"]
    assert mapping.resolution_m == 10


def test_sentinel2_nir_band_resolution():
    mapping = get_band_mapping("Sentinel-2", "NIR")

    assert mapping.dataset_bands == ["B08"]
    assert mapping.resolution_m == 10



def test_sentinel2_swir1_band_resolution():
    mapping = get_band_mapping("Sentinel-2", "SWIR1")

    assert mapping.dataset_bands == ["B11"]
    assert mapping.resolution_m == 20


def test_sentinel2_nir_20m_mapping_exists():
    mappings = get_dataset_band_mappings("Sentinel-2")

    nir_20m = [
        mapping
        for mapping in mappings
        if mapping.conceptual_band == "NIR"
        and mapping.resolution_m == 20
    ]

    assert len(nir_20m) == 1
    assert nir_20m[0].dataset_bands == ["B8A"]



def test_sentinel2_ndvi_analysis_resolution():
    candidate = DatasetCandidate(
        dataset="Sentinel-2",
        pathway="calculated",
    )

    result = get_analysis_resolution(
        candidate,
        "NDVI",
    )

    assert result.resolution_m == 10
    assert result.resampling_required is False



def test_sentinel2_ndmi_analysis_resolution():
    candidate = DatasetCandidate(
        dataset="Sentinel-2",
        pathway="calculated",
    )

    result = get_analysis_resolution(
        candidate,
        "NDMI",
    )

    assert result.resolution_m == 10
    assert result.resampling_required is True


##### Test for Landsat
def test_landsat8_red_band_resolution():
    mapping = get_band_mapping("Landsat-8", "RED")

    assert mapping.dataset_bands == ["B4"]
    assert mapping.resolution_m == 30


def test_landsat8_nir_band_resolution():
    mapping = get_band_mapping("Landsat-8", "NIR")

    assert mapping.dataset_bands == ["B5"]
    assert mapping.resolution_m == 30


def test_landsat8_swir1_band_resolution():
    mapping = get_band_mapping("Landsat-8", "SWIR1")

    assert mapping.dataset_bands == ["B6"]
    assert mapping.resolution_m == 30


def test_landsat9_band_mapping():
    red = get_band_mapping("Landsat-9", "RED")
    nir = get_band_mapping("Landsat-9", "NIR")
    swir1 = get_band_mapping("Landsat-9", "SWIR1")

    assert red.dataset_bands == ["B4"]
    assert red.resolution_m == 30

    assert nir.dataset_bands == ["B5"]
    assert nir.resolution_m == 30

    assert swir1.dataset_bands == ["B6"]
    assert swir1.resolution_m == 30


#### analysis test
def test_landsat8_ndvi_analysis_resolution():
    candidate = DatasetCandidate(
        dataset="Landsat-8",
        pathway="calculated",
    )

    result = get_analysis_resolution(
        candidate,
        "NDVI",
    )

    assert result.resolution_m == 30
    assert result.resampling_required is False


def test_landsat8_ndmi_analysis_resolution():
    candidate = DatasetCandidate(
        dataset="Landsat-8",
        pathway="calculated",
    )

    result = get_analysis_resolution(
        candidate,
        "NDMI",
    )

    assert result.resolution_m == 30
    assert result.resampling_required is False


def test_landsat9_ndvi_analysis_resolution():
    candidate = DatasetCandidate(
        dataset="Landsat-9",
        pathway="calculated",
    )

    result = get_analysis_resolution(
        candidate,
        "NDVI",
    )

    assert result.resolution_m == 30
    assert result.resampling_required is False


#### HLS 
def test_hls_red_band_resolution():
    mapping = get_band_mapping("HLS", "RED")

    assert mapping.dataset_bands == ["B4"]
    assert mapping.resolution_m == 30


def test_hls_nir_band_resolution():
    mapping = get_band_mapping("HLS", "NIR")

    assert mapping.dataset_bands == ["B8", "B8A"]
    assert mapping.resolution_m == 30


def test_hls_swir1_band_resolution():
    mapping = get_band_mapping("HLS", "SWIR1")

    assert mapping.dataset_bands == ["B11"]
    assert mapping.resolution_m == 30


def test_hls_ndvi_analysis_resolution():
    candidate = DatasetCandidate(
        dataset="HLS",
        pathway="calculated",
    )

    result = get_analysis_resolution(
        candidate,
        "NDVI",
    )

    assert result.resolution_m == 30
    assert result.resampling_required is False


def test_hls_ndmi_analysis_resolution():
    candidate = DatasetCandidate(
        dataset="HLS",
        pathway="calculated",
    )

    result = get_analysis_resolution(
        candidate,
        "NDMI",
    )

    assert result.resolution_m == 30
    assert result.resampling_required is False


#### MODIS
def test_mod13q1_product_resolution():
    product = get_product("MOD13Q1.061")

    assert product.spatial_resolution_m == 250
    assert product.temporal_resolution == "16-day"


def test_mod13q1_supported_indices():
    product = get_product("MOD13Q1.061")

    assert "NDVI" in product.supported_indices
    assert "EVI" in product.supported_indices


def test_mod13q1_ndvi_analysis_resolution():
    candidate = DatasetCandidate(
        dataset="MODIS",
        product="MOD13Q1.061",
        pathway="product",
    )

    result = get_analysis_resolution(
        candidate,
        "NDVI",
    )

    assert result.resolution_m == 250
    assert result.resampling_required is False


def test_mod13q1_evi_analysis_resolution():
    candidate = DatasetCandidate(
        dataset="MODIS",
        product="MOD13Q1.061",
        pathway="product",
    )

    result = get_analysis_resolution(
        candidate,
        "EVI",
    )

    assert result.resolution_m == 250
    assert result.resampling_required is False


def test_modis_weekly_temporal_suitability():
    candidate = DatasetCandidate(
        dataset="MODIS",
        product="MOD13Q1.061",
        pathway="product",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="weekly",
    )

    score = score_temporal_suitability(candidate, request)

    assert score == 0.4


###### Sentinel - 1
def test_sentinel1_vv_band_resolution():
    mapping = get_band_mapping("Sentinel-1", "VV")

    assert mapping.dataset_bands == ["VV"]
    assert mapping.resolution_m == 10


def test_sentinel1_vh_band_resolution():
    mapping = get_band_mapping("Sentinel-1", "VH")

    assert mapping.dataset_bands == ["VH"]
    assert mapping.resolution_m == 10


def test_sentinel1_hh_band_resolution():
    mapping = get_band_mapping("Sentinel-1", "HH")

    assert mapping.dataset_bands == ["HH"]
    assert mapping.resolution_m == 10


def test_sentinel1_hv_band_resolution():
    mapping = get_band_mapping("Sentinel-1", "HV")

    assert mapping.dataset_bands == ["HV"]
    assert mapping.resolution_m == 10


def test_sentinel1_dataset_spatial_resolution():
    dataset = get_dataset("Sentinel-1")

    assert dataset.spatial_resolutions_m == [5.0, 10.0, 20.0]



### CHIRPS
def test_chirps_dataset_metadata():
    dataset = get_dataset("CHIRPS")

    assert dataset.data_type == "climate"
    assert dataset.data_family == "PRECIPITATION"
    assert dataset.spatial_resolutions_m == [5560.0]


def test_chirps_temporal_resolution():
    dataset = get_dataset("CHIRPS")

    assert dataset.temporal_resolution == "daily and monthly"
    assert dataset.temporal_resolution_days is None


def test_chirps_products():
    daily = get_product("CHIRPS-DAILY")
    monthly = get_product("CHIRPS-MONTHLY")

    assert daily.dataset == "CHIRPS"
    assert daily.temporal_resolution == "daily"
    assert daily.temporal_resolution_days == 1.0

    assert monthly.dataset == "CHIRPS"
    assert monthly.temporal_resolution == "monthly"
    assert monthly.temporal_resolution_days == 30.0


def test_chirps_daily_temporal_suitability():
    candidate = DatasetCandidate(
        dataset="CHIRPS",
        product="CHIRPS-DAILY",
        pathway="product",
    )

    request = DatasetSelectionRequest(
        analysis_type="precipitation",
        data_family="PRECIPITATION",
        spatial_scale="regional",
        temporal_requirement="daily",
    )

    score = score_temporal_suitability(candidate, request)

    assert score == 1.0


def test_chirps_monthly_temporal_suitability():
    candidate = DatasetCandidate(
        dataset="CHIRPS",
        product="CHIRPS-MONTHLY",
        pathway="product",
    )

    request = DatasetSelectionRequest(
        analysis_type="precipitation",
        data_family="PRECIPITATION",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_temporal_suitability(candidate, request)

    assert score == 1.0


def test_chirps_daily_analysis_temporal_resolution():
    candidate = DatasetCandidate(
        dataset="CHIRPS",
        product="CHIRPS-DAILY",
        pathway="product",
    )

    result = get_analysis_temporal_resolution(candidate)

    assert result.resolution_days == 1.0
    assert result.source == "product"
    assert result.description == "daily"


def test_chirps_monthly_analysis_temporal_resolution():
    candidate = DatasetCandidate(
        dataset="CHIRPS",
        product="CHIRPS-MONTHLY",
        pathway="product",
    )

    result = get_analysis_temporal_resolution(candidate)

    assert result.resolution_days == 30.0
    assert result.source == "product"
    assert result.description == "monthly"


###### ERA
def test_era5_dataset_metadata():
    dataset = get_dataset("ERA5")

    assert dataset.data_type == "climate"
    assert dataset.data_family == "CLIMATE"
    assert dataset.spatial_resolutions_m == [27800.0]
    assert dataset.coverage == "Global"


def test_era5_temporal_resolution():
    dataset = get_dataset("ERA5")

    assert dataset.temporal_resolution == "hourly"
    assert dataset.temporal_resolution_days == 1 / 24



def test_era5_analysis_temporal_resolution():
    candidate = DatasetCandidate(
        dataset="ERA5",
        pathway="calculated",
    )

    result = get_analysis_temporal_resolution(candidate)

    assert result.resolution_days == 1 / 24
    assert result.source == "dataset"
    assert result.description == "hourly"


def test_era5_hourly_temporal_suitability():
    candidate = DatasetCandidate(
        dataset="ERA5",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="climate",
        data_family="CLIMATE",
        spatial_scale="regional",
        temporal_requirement="daily",
    )

    score = score_temporal_suitability(candidate, request)

    assert score == 1.0


def test_era5_monthly_temporal_suitability():
    candidate = DatasetCandidate(
        dataset="ERA5",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="climate",
        data_family="CLIMATE",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_temporal_suitability(candidate, request)

    assert score == 1.0



#### ERA5-Land
def test_era5_land_dataset_metadata():
    dataset = get_dataset("ERA5-Land")

    assert dataset.data_type == "climate"
    assert dataset.data_family == "CLIMATE"
    assert dataset.spatial_resolutions_m == [11100.0]
    assert dataset.coverage == "Global"


def test_era5_land_analysis_temporal_resolution():
    candidate = DatasetCandidate(
        dataset="ERA5-Land",
        pathway="calculated",
    )

    result = get_analysis_temporal_resolution(candidate)

    assert result.resolution_days == 1 / 24
    assert result.source == "dataset"
    assert result.description == "hourly"


def test_era5_land_monthly_temporal_suitability():
    candidate = DatasetCandidate(
        dataset="ERA5-Land",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="climate",
        data_family="CLIMATE",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_temporal_suitability(candidate, request)

    assert score == 1.0


##### Test for product suitability
#### Native product suitability

def test_modis_ndvi_native_product_suitability():
    candidate = DatasetCandidate(
        dataset="MODIS",
        product="MOD13Q1.061",
        pathway="product",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_native_product_suitability(candidate, request)

    assert score == 1.0


def test_chirps_precipitation_native_product_suitability():
    candidate = DatasetCandidate(
        dataset="CHIRPS",
        product="CHIRPS-DAILY",
        pathway="product",
    )

    request = DatasetSelectionRequest(
        analysis_type="precipitation",
        data_family="PRECIPITATION",
        spatial_scale="regional",
        temporal_requirement="daily",
    )

    score = score_native_product_suitability(candidate, request)

    assert score == 1.0



#### Spectral suitability

def test_sentinel2_ndvi_spectral_suitability():
    candidate = DatasetCandidate(
        dataset="Sentinel-2",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_spectral_suitability(candidate, request)

    assert score == 1.0


def test_sentinel2_ndre_spectral_suitability():
    candidate = DatasetCandidate(
        dataset="Sentinel-2",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDRE",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_spectral_suitability(candidate, request)

    assert score == 1.0


def test_landsat9_ndre_spectral_suitability():
    candidate = DatasetCandidate(
        dataset="Landsat-9",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDRE",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_spectral_suitability(candidate, request)

    assert score == 0.0


def test_sentinel1_soil_moisture_spectral_suitability():
    candidate = DatasetCandidate(
        dataset="Sentinel-1",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="soil_moisture",
        data_family="SAR",
        spatial_scale="regional",
        temporal_requirement="weekly",
    )

    score = score_spectral_suitability(candidate, request)

    assert score == 1.0


def test_sentinel2_ndvi_calculated_product_suitability():
    candidate = DatasetCandidate(
        dataset="Sentinel-2",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_native_product_suitability(candidate, request)

    assert score == 0.5


def test_unsupported_product_analysis_suitability():
    candidate = DatasetCandidate(
        dataset="MODIS",
        product="MOD13Q1.061",
        pathway="product",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDMI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_native_product_suitability(candidate, request)

    assert score == 0.0




#### Testing spatial resolution
def test_sentinel2_local_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="Sentinel-2",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="local",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 1.0


def test_sentinel2_city_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="Sentinel-2",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="city",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 1.0


def test_landsat8_local_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="Landsat-8",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="local",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 0.5


def test_landsat8_city_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="Landsat-8",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="city",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 1.0


def test_mod13q1_local_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="MODIS",
        product="MOD13Q1.061",
        pathway="product",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="local",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 0.5


def test_mod13q1_city_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="MODIS",
        product="MOD13Q1.061",
        pathway="product",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="city",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 0.7


def test_mod13q1_regional_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="MODIS",
        product="MOD13Q1.061",
        pathway="product",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 0.8



def test_landsat9_local_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="Landsat-9",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="local",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 0.5


def test_landsat9_city_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="Landsat-9",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="city",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 1.0


def test_hls_city_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="HLS",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="city",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 1.0

def test_sentinel1_local_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="Sentinel-1",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="soil_moisture",
        data_family="SAR",
        spatial_scale="local",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 1.0


def test_sentinel1_soil_moisture_analysis_resolution():
    candidate = DatasetCandidate(
        dataset="Sentinel-1",
        pathway="calculated",
    )

    result = get_analysis_resolution(
        candidate,
        "soil_moisture",
    )

    assert result.resolution_m == 10
    assert result.resampling_required is False
    assert len(result.band_resolutions) == 2
    assert result.band_resolutions[0].conceptual_band == "VV"
    assert result.band_resolutions[0].dataset_band == "VV"
    assert result.band_resolutions[0].resolution_m == 10
    assert result.band_resolutions[1].conceptual_band == "VH"
    assert result.band_resolutions[1].dataset_band == "VH"
    assert result.band_resolutions[1].resolution_m == 10


def test_chirps_regional_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="CHIRPS",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="precipitation",
        data_family="PRECIPITATION",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 0.8


def test_era5_regional_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="ERA5",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="climate",
        data_family="CLIMATE",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 0.8


def test_era5_land_regional_spatial_suitability():
    candidate = DatasetCandidate(
        dataset="ERA5-Land",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="climate",
        data_family="CLIMATE",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    score = score_spatial_resolution(candidate, request)

    assert score == 0.8


def test_rank_dataset_candidate_combines_scores():
    candidate = DatasetCandidate(
        dataset="Landsat-9",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    ranking = rank_dataset_candidate(candidate, request)

    expected_score = (
        ranking.spatial_score * SPATIAL_WEIGHT
        + ranking.temporal_score * TEMPORAL_WEIGHT
        + ranking.native_product_score * NATIVE_WEIGHT
        + ranking.spectral_score * SPECTRAL_WEIGHT
        + ranking.computational_score * COMPUTATIONAL_WEIGHT
    )

    assert ranking.total_score == expected_score


def test_rank_dataset_candidate_returns_dataset_ranking():
    candidate = DatasetCandidate(
        dataset="Landsat-9",
        pathway="calculated",
    )

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    ranking = rank_dataset_candidate(candidate, request)

    assert isinstance(ranking, DatasetRanking)
    assert ranking.candidate == candidate
    assert 0.0 <= ranking.total_score <= 1.0
    assert ranking.rationale


def test_rank_dataset_candidates_returns_sorted_rankings():
    candidates = [
        DatasetCandidate(
            dataset="MODIS",
            product="MOD13Q1.061",
            pathway="product",
        ),
        DatasetCandidate(
            dataset="Sentinel-2",
            pathway="calculated",
        ),
    ]

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    rankings = rank_dataset_candidates(
        candidates,
        request,
    )

    assert len(rankings) == 2
    assert rankings[0].total_score >= rankings[1].total_score



def test_inspect_ndvi_dataset_ranking():
    candidates = [
        DatasetCandidate(
            dataset="Sentinel-2",
            pathway="calculated",
        ),
        DatasetCandidate(
            dataset="MODIS",
            product="MOD13Q1.061",
            pathway="product",
        ),
        DatasetCandidate(
            dataset="Landsat-9",
            pathway="calculated",
        ),
        DatasetCandidate(
            dataset="HLS",
            pathway="calculated",
        ),
    ]

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    rankings = rank_dataset_candidates(
        candidates,
        request,
    )

    for ranking in rankings:
        print(
            f"{ranking.candidate.dataset}"
            f"{' / ' + ranking.candidate.product if ranking.candidate.product else ''}"
            f" | total={ranking.total_score:.3f}"
            f" | spatial={ranking.spatial_score:.2f}"
            f" | temporal={ranking.temporal_score:.2f}"
            f" | native={ranking.native_product_score:.2f}"
            f" | spectral={ranking.spectral_score:.2f}"
            f" | computational={ranking.computational_score:.2f}"
        )

    assert len(rankings) == 4
    assert rankings[0].total_score >= rankings[-1].total_score


def test_inspect_ndvi_local_daily_ranking():
    candidates = [
        DatasetCandidate(
            dataset="Sentinel-2",
            pathway="calculated",
        ),
        DatasetCandidate(
            dataset="MODIS",
            product="MOD13Q1.061",
            pathway="product",
        ),
        DatasetCandidate(
            dataset="Landsat-9",
            pathway="calculated",
        ),
        DatasetCandidate(
            dataset="HLS",
            pathway="calculated",
        ),
    ]

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="local",
        temporal_requirement="daily",
    )

    rankings = rank_dataset_candidates(
        candidates,
        request,
    )

    for ranking in rankings:
        print(
            f"{ranking.candidate.dataset}"
            f"{' / ' + ranking.candidate.product if ranking.candidate.product else ''}"
            f" | total={ranking.total_score:.3f}"
            f" | spatial={ranking.spatial_score:.2f}"
            f" | temporal={ranking.temporal_score:.2f}"
            f" | native={ranking.native_product_score:.2f}"
            f" | spectral={ranking.spectral_score:.2f}"
            f" | computational={ranking.computational_score:.2f}"
        )

    assert len(rankings) == 4
    assert rankings[0].total_score >= rankings[-1].total_score


def test_inspect_ndmi_regional_monthly_ranking():
    candidates = [
        DatasetCandidate(
            dataset="Sentinel-2",
            pathway="calculated",
        ),
        DatasetCandidate(
            dataset="MODIS",
            product="MOD13Q1.061",
            pathway="product",
        ),
        DatasetCandidate(
            dataset="Landsat-9",
            pathway="calculated",
        ),
        DatasetCandidate(
            dataset="HLS",
            pathway="calculated",
        ),
    ]

    request = DatasetSelectionRequest(
        analysis_type="NDMI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    rankings = rank_dataset_candidates(
        candidates,
        request,
    )

    for ranking in rankings:
        print(
            f"{ranking.candidate.dataset}"
            f"{' / ' + ranking.candidate.product if ranking.candidate.product else ''}"
            f" | total={ranking.total_score:.3f}"
            f" | spatial={ranking.spatial_score:.2f}"
            f" | temporal={ranking.temporal_score:.2f}"
            f" | native={ranking.native_product_score:.2f}"
            f" | spectral={ranking.spectral_score:.2f}"
            f" | computational={ranking.computational_score:.2f}"
        )

    assert len(rankings) == 4
    assert rankings[0].total_score >= rankings[-1].total_score



def test_rank_dataset_candidates_sorts_and_excludes_ineligible():
    candidates = [
        DatasetCandidate(
            dataset="Landsat-9",
            pathway="calculated",
        ),
        DatasetCandidate(
            dataset="Sentinel-2",
            pathway="calculated",
        ),
        DatasetCandidate(
            dataset="MODIS",
            product="MOD13Q1.061",
            pathway="product",
            eligible=False,
        ),
    ]

    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    rankings = rank_dataset_candidates(
        candidates,
        request,
    )

    assert len(rankings) == 2

    assert rankings[0].total_score >= rankings[1].total_score

    assert all(
        ranking.candidate.eligible
        for ranking in rankings
    )

    assert all(
        ranking.candidate.dataset != "MODIS"
        for ranking in rankings
    )