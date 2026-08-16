import pytest

from core.schemas import DatasetSelectionRequest
from core.dataset_selector import (
    get_eligible_products,
    select_datasets,
    select_best_dataset,

)


def test_ndvi_regional_candidates():
    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    candidates = get_eligible_products(request)

    assert len(candidates) > 0

    assert all(
        candidate.eligible
        for candidate in candidates
    )

    candidate_names = {
        candidate.dataset
        for candidate in candidates
    }

    assert "Sentinel-2" in candidate_names
    assert "Landsat-9" in candidate_names
    assert "HLS" in candidate_names



def test_ndvi_regional_candidate_pathways():
    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    candidates = get_eligible_products(request)

    modis_candidates = [
        candidate
        for candidate in candidates
        if candidate.dataset == "MODIS"
    ]

    sentinel2_candidates = [
        candidate
        for candidate in candidates
        if candidate.dataset == "Sentinel-2"
    ]

    assert any(
        candidate.pathway == "product"
        and candidate.product == "MOD13Q1.061"
        for candidate in modis_candidates
    )

    assert any(
        candidate.pathway == "calculated"
        and candidate.product is None
        for candidate in sentinel2_candidates
    )



from core.dataset_selector import select_datasets


def test_ndvi_regional_selection_ranking():
    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    rankings = select_datasets(request)

    assert len(rankings) > 0

    assert all(
        ranking.total_score >= 0
        for ranking in rankings
    )

    scores = [
        ranking.total_score
        for ranking in rankings
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )


def test_ndmi_regional_candidates():
    request = DatasetSelectionRequest(
        analysis_type="NDMI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    candidates = get_eligible_products(request)

    assert len(candidates) > 0

    candidate_names = {
        candidate.dataset
        for candidate in candidates
    }

    assert "Sentinel-2" in candidate_names
    assert "Landsat-9" in candidate_names
    assert "HLS" in candidate_names


def test_ndmi_regional_candidate_pathways():
    request = DatasetSelectionRequest(
        analysis_type="NDMI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    candidates = get_eligible_products(request)

    sentinel2_candidates = [
        candidate
        for candidate in candidates
        if candidate.dataset == "Sentinel-2"
    ]

    landsat9_candidates = [
        candidate
        for candidate in candidates
        if candidate.dataset == "Landsat-9"
    ]

    assert any(
        candidate.pathway == "calculated"
        and candidate.product is None
        for candidate in sentinel2_candidates
    )

    assert any(
        candidate.pathway == "calculated"
        and candidate.product is None
        for candidate in landsat9_candidates
    )


def test_ndmi_regional_selection_ranking():
    request = DatasetSelectionRequest(
        analysis_type="NDMI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    rankings = select_datasets(request)

    assert len(rankings) > 0

    assert all(
        ranking.total_score >= 0
        for ranking in rankings
    )

    scores = [
        ranking.total_score
        for ranking in rankings
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )


def test_select_best_ndvi_regional_dataset():
    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    best = select_best_dataset(request)

    assert best is not None
    assert best.total_score == pytest.approx(0.94)
    assert best.candidate.dataset == "MODIS"
    assert best.candidate.product == "MOD13Q1.061"
    assert best.candidate.pathway == "product"