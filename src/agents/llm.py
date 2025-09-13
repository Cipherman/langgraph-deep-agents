from langchain.chat_models import init_chat_model
from src.config.env import setup_env

setup_env()

llm = init_chat_model(model="anthropic:claude-3-5-haiku-latest", temperature=0.0)
