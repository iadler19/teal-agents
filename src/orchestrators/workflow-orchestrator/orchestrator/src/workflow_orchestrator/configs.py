from typing import List

from ska_utils import Config

TA_AGW_KEY = Config(env_name="TA_AGW_KEY", is_required=True, default_value=None)
TA_AGW_HOST = Config(
    env_name="TA_AGW_HOST", is_required=True, default_value="localhost:8000"
)
TA_AGW_SECURE = Config(
    env_name="TA_AGW_SECURE", is_required=True, default_value="false"
)
TA_SERVICE_CONFIG = Config(
    env_name="TA_SERVICE_CONFIG", is_required=True, default_value="conf/config.yaml"
)
TA_WORKFLOW_MODULE = Config(
    env_name="TA_WORKFLOW_MODULE", is_required=False, default_value=None
)

configs: List[Config] = [
    TA_AGW_KEY,
    TA_AGW_HOST,
    TA_AGW_SECURE,
    TA_SERVICE_CONFIG,
    TA_WORKFLOW_MODULE,
]
