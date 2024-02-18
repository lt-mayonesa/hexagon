import datetime
from typing import Any, Dict, Optional

from pydantic import BaseSettings, ValidationError
from pydantic.types import DirectoryPath

from hexagon.runtime.yaml import YamlValidationError


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
    options_dict["update_time_between_checks"] = (
        options.update_time_between_checks.total_seconds()
    )
    store_user_data(
        HexagonStorageKeys.options.value, options_dict, app=HEXAGON_STORAGE_APP
    )


class KeymapOptions(BaseSettings):
    create_dir: str = "c-p"


class Options(BaseSettings):
    theme: Optional[str] = "default"
    update_time_between_checks: Optional[datetime.timedelta] = datetime.timedelta(
        days=1
    )
    send_telemetry: Optional[bool] = None
    disable_dependency_scan: Optional[bool] = False
    update_disabled: Optional[bool] = False
    cli_update_disabled: Optional[bool] = False
    config_storage_path: Optional[DirectoryPath] = None
    hints_disabled: Optional[bool] = False
    keymap: KeymapOptions = KeymapOptions()

    class Config:
        env_prefix = "HEXAGON_"

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return (
                init_settings,
                env_settings,
                _local_settings_source,
                file_secret_settings,
            )


def get_options(init_settings: dict) -> Options:
    try:
        return Options(**init_settings)
    except ValidationError as errors:
        raise YamlValidationError(errors)


def update_options(opt: Options) -> Options:
    _save_settings_to_source(opt)
    return opt.copy()
