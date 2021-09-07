import datetime
from hexagon.support.yaml import display_yaml_errors
import sys
from typing import Any, Dict, Optional
from pydantic import BaseSettings, ValidationError


def _local_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    from hexagon.support.storage import (
        HEXAGON_STORAGE_APP,
        HexagonStorageKeys,
        load_user_data,
    )

    return load_user_data(HexagonStorageKeys.options.value, HEXAGON_STORAGE_APP) or {}


def _save_settings_to_source(options):
    from hexagon.support.storage import (
        HEXAGON_STORAGE_APP,
        HexagonStorageKeys,
        store_user_data,
    )

    options_dict = options.dict()
    options_dict[
        "update_time_between_checks"
    ] = options.update_time_between_checks.total_seconds()
    store_user_data(
        HexagonStorageKeys.options.value, options_dict, app=HEXAGON_STORAGE_APP
    )


class Options(BaseSettings):
    update_time_between_checks: datetime.timedelta = datetime.timedelta(days=1)
    send_telemetry: Optional[bool] = None

    class Config:
        env_prefix = "HEXAGON_"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            # TODO: allow CLIs to override options from app.yaml (ie: cli.options.update_time_between_checks)
            return (
                env_settings,
                init_settings,
                _local_settings_source,
                file_secret_settings,
            )


def get_options() -> Options:
    try:
        return Options()
    except ValidationError as errors:
        display_yaml_errors(errors)
        sys.exit(1)


def update_options(opt: Options) -> Options:
    _save_settings_to_source(opt)
    return opt.copy()
