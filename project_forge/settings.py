"""Settings for project forge."""

from pathlib import Path
from typing import List

from platformdirs import user_cache_path, user_config_path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

APP_NAME = "project_forge"

DEFAULT_CACHE_DIR = user_cache_path(APP_NAME, appauthor=False)
CONFIG_DIR = user_config_path(APP_NAME, appauthor=False, roaming=True)
DEFAULT_CONFIG_FILE = CONFIG_DIR / "project_forge.toml"
DEFAULT_ALWAYS_SKIP = [
    ".DS_Store",
]


class Settings(BaseSettings):
    """The configuration for the project forge."""

    always_skip: List[str] = Field(default=DEFAULT_ALWAYS_SKIP, description="A list of glob patterns to skip always.")

    model_config = SettingsConfigDict(env_prefix=f"{APP_NAME}_", env_file=".env", extra="ignore")

    disable_cache: bool = Field(default=False, description="Disable local caching of remote git repositories.")
    cache_dir: Path = Field(
        default=DEFAULT_CACHE_DIR,
        description="The directory to store remote templates.",
    )


_APP_SETTINGS = None


def get_settings(config_file: Path = DEFAULT_CONFIG_FILE) -> Settings:
    """Return the settings."""
    # TODO[#3]: Implement settings management
    global _APP_SETTINGS  # noqa: PLW0603

    if _APP_SETTINGS is None:
        _APP_SETTINGS = Settings()

    return _APP_SETTINGS
