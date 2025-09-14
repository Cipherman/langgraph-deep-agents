import logging
from pathlib import Path
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_env():
    project_root = Path(__file__).resolve().parent.parent.parent
    env_path = project_root / ".env"

    if env_path.exists():
        load_dotenv(env_path, override=True)
        logger.info(f"Setup environment from {env_path}")
    else:
        logger.warning(f".env file not found at {env_path}")
