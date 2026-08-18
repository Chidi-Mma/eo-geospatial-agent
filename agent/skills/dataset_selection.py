from pydantic_ai import RunContext
from pydantic_ai.toolsets import FunctionToolset

from core.dataset_selector import select_best_dataset
from core.schemas import DatasetRanking, DatasetSelectionRequest


dataset_selection_skill = FunctionToolset(
    id="dataset-selection",
    instructions=(
        "Use the dataset selection skill whenever a user asks which dataset "
        "or product should be used for an analysis. "
        "The skill returns the highest-ranked compatible dataset or product "
        "based on the structured analysis requirements."
    ),
)


@dataset_selection_skill.tool
def select_best_dataset_tool(
    ctx: RunContext,
    request: DatasetSelectionRequest,
) -> DatasetRanking | None:
    """Select the highest-ranked dataset or product for an analysis request."""

    return select_best_dataset(request)