import os
from dotenv import load_dotenv,find_dotenv
from agents import AsyncOpenAI, OpenAIResponsesModel, RunConfig

_=load_dotenv(find_dotenv())

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

client=AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.openai.com/v1"
)

model=OpenAIResponsesModel(
    model="gpt-4.1-mini",
    openai_client=client
)

config=RunConfig(
    model=model,
    model_provider=client
)