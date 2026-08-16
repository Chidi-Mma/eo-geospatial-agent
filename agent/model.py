from dotenv import load_dotenv
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.capabilities import WebSearch

load_dotenv(override=True)

model = OpenRouterModel(
    "deepseek/deepseek-v4-flash"
)

