import datetime
from hexagon.support.yaml import display_yaml_errors
import sys
from typing import Any, Dict
from pydantic import BaseSettings, ValidationError


def local_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    from hexagon.support.storage import (
        HEXAGON_STORAGE_APP,
        HexagonStorageKeys,
        load_user_data,
    )

    return load_user_data(HexagonStorageKeys.options.value, HEXAGON_STORAGE_APP) or {}


class Options(BaseSettings):
    update_time_between_checks: datetime.timedelta = datetime.timedelta(days=1)

    class Config:
        env_prefix = "HEXAGON_"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                env_settings,
                init_settings,
                local_settings_source,
                file_secret_settings,
            )


def get_options() -> Options:
    try:
        return Options()
    except ValidationError as errors:
        display_yaml_errors(errors)
        sys.exit(1)
