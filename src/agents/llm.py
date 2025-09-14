from langchain.chat_models import init_chat_model
from src.config.env import setup_env

setup_env()

llm = init_chat_model(model="anthropic:claude-3-5-haiku-latest", temperature=0.0)

summarize_llm = init_chat_model(model="anthropic:claude-3-5-haiku-latest", max_tokens=8191)
compress_llm = init_chat_model(model="anthropic:claude-3-5-haiku-latest", max_tokens=8191)