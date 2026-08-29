from posthog import Posthog
from config.config_env import Config

posthog = Posthog(
    host=Config.POSTHOG_ENDPOINT,
    project_api_key=Config.POSTHOG_API_KEY,
    enable_exception_autocapture=False
)
