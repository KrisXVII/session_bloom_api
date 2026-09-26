from posthog import Posthog
from config.config_env import Config

posthog = Posthog(
    host=Config.POSTHOG_ENDPOINT,
    project_api_key=Config.POSTHOG_API_KEY,
    enable_exception_autocapture=False,
    capture_exception_code_variables=True,
    code_variables_mask_patterns=Config.DEFAULT_CODE_VARIABLES_MASK_PATTERNS +
                                 [r"(?i)email", r"(?i)first_name", r"(?i)last_name"]
)
