from agent.agent import select_best_dataset_tool
from core.schemas import DatasetSelectionRequest


def test_agent_dataset_selection_tool_ndvi():
    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    result = select_best_dataset_tool(request)

    assert result is not None
    assert result.candidate.dataset == "MODIS"
    assert result.candidate.product == "MOD13Q1.061"
    assert result.candidate.pathway == "product"


def test_agent_dataset_selection_tool_monthly_precipitation():
    request = DatasetSelectionRequest(
        analysis_type="precipitation",
        data_family="PRECIPITATION",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    result = select_best_dataset_tool(request)

    assert result is not None
    assert result.candidate.dataset == "CHIRPS"
    assert result.candidate.product == "CHIRPS-MONTHLY"
    assert result.candidate.pathway == "product"


def test_agent_dataset_selection_tool_daily_precipitation():
    request = DatasetSelectionRequest(
        analysis_type="precipitation",
        data_family="PRECIPITATION",
        spatial_scale="regional",
        temporal_requirement="daily",
    )

    result = select_best_dataset_tool(request)

    assert result is not None
    assert result.candidate.dataset == "CHIRPS"
    assert result.candidate.product == "CHIRPS-DAILY"
    assert result.candidate.pathway == "product"


def test_agent_dataset_selection_tool_sar_soil_moisture():
    request = DatasetSelectionRequest(
        analysis_type="soil_moisture",
        data_family="SAR",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    result = select_best_dataset_tool(request)

    assert result is not None
    assert result.candidate.dataset == "Sentinel-1"
    assert result.candidate.product is None
    assert result.candidate.pathway == "calculated"


def test_agent_dataset_selection_tool_ndmi():
    request = DatasetSelectionRequest(
        analysis_type="NDMI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    result = select_best_dataset_tool(request)

    assert result is not None
    assert result.candidate.dataset in {
        "Sentinel-2",
        "Landsat-8",
        "Landsat-9",
        "HLS",
    }
    assert result.candidate.product is None
    assert result.candidate.pathway == "calculated"