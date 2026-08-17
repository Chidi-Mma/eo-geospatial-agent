from agent.reasoning import (
    create_thinking_capability,
    determine_reasoning_from_prompt,
    determine_reasoning_level,
    adaptive_reasoning_capability,
)
from core.schemas import DatasetSelectionRequest
from pydantic_ai.capabilities import Thinking

def test_simple_request_uses_low_reasoning():
    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
    )

    assert determine_reasoning_level(request) == "low"


def test_request_with_multiple_requirements_uses_medium_reasoning():
    request = DatasetSelectionRequest(
        analysis_type="NDMI",
        data_family="OPTICAL",
        spatial_scale="regional",
        temporal_requirement="monthly",
        required_bands=["NIR", "SWIR1"],
        required_variables=["soil_moisture"],
    )

    assert determine_reasoning_level(request) == "medium"


def test_global_annual_request_uses_medium_reasoning():
    request = DatasetSelectionRequest(
        analysis_type="NDVI",
        data_family="OPTICAL",
        spatial_scale="global",
        temporal_requirement="annual",
    )

    assert determine_reasoning_level(request) == "medium"


def test_complex_request_uses_high_reasoning():
    request = DatasetSelectionRequest(
        analysis_type="multi_index_analysis",
        data_family="OPTICAL",
        spatial_scale="global",
        temporal_requirement="annual",
        required_bands=["BLUE", "GREEN", "RED", "NIR", "SWIR1", "SWIR2"],
        required_variables=["precipitation", "temperature"],
        description=(
            "Compare multiple vegetation and moisture indices across regions "
            "and evaluate their temporal and spatial compatibility with climate data"
        ),
    )

    assert determine_reasoning_level(request) == "high"


def test_low_reasoning_creates_low_thinking_capability():
    capability = create_thinking_capability("low")

    assert isinstance(capability, Thinking)
    assert capability.effort == "low"


def test_medium_reasoning_creates_medium_thinking_capability():
    capability = create_thinking_capability("medium")

    assert isinstance(capability, Thinking)
    assert capability.effort == "medium"


def test_high_reasoning_creates_high_thinking_capability():
    capability = create_thinking_capability("high")

    assert isinstance(capability, Thinking)
    assert capability.effort == "high"



def test_simple_prompt_uses_low_reasoning():
    assert (
        determine_reasoning_from_prompt(
            "Which dataset should I use for NDVI at regional scale?"
        )
        == "low"
    )


def test_global_prompt_uses_medium_reasoning():
    assert (
        determine_reasoning_from_prompt(
            "Which dataset should I use for NDVI at global scale?"
        )
        == "medium"
    )


def test_comparison_prompt_uses_medium_reasoning():
    assert (
        determine_reasoning_from_prompt(
            "Compare datasets for NDVI and NDMI at regional scale."
        )
        == "medium"
    )


def test_complex_prompt_uses_high_reasoning():
    assert (
        determine_reasoning_from_prompt(
            "Compare multiple datasets for NDVI and NDMI at global scale "
            "using seasonal observations and evaluate their suitability "
            "for the analysis."
        )
        == "high"
    )