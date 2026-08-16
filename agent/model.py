

import os
import asyncio
from typing import List

from pydantic_ai import Agent
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai import ModelMessage
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.toolsets import FunctionToolset
from pydantic_ai.capabilities import WebSearch


#provider = OpenAIProvider(
    #base_url="https://openrouter.ai/api/v1",
    #api_key=os.getenv("OPENROUTER_API_KEY"),
#)


#model = OpenAIChatModel(
    #model_name="google/gemini-2.5-flash",
    #provider=provider,
#)


model = OpenRouterModel(
    "openai/gpt-5.2"
)