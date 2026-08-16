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