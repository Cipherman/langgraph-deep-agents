import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnvConfig(BaseModel):
    llm_api_key: str
    llm_base_url: Optional[str] = None
    llm_model: str = Field(default="anthropic:claude-3-5-haiku-latest")


def setup_env():
    # os.environ[""]
    project_root = Path(__file__).resolve().parent.parent.parent
    env_path = project_root / ".env"

    if env_path.exists():
        load_dotenv(env_path, override=True)
        logger.info(f"Setup environment from {env_path}")
    else:
        logger.warning(f".env file not found at {env_path}")
