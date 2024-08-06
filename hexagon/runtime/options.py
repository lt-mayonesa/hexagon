import datetime
from typing import Optional, Type

from pydantic import ValidationError
from pydantic.types import DirectoryPath
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    InitSettingsSource,
)

from hexagon.runtime.yaml import YamlValidationError


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


class UserDataSettingsSource(InitSettingsSource):
    def __init__(self, settings_cls: type[BaseSettings]):
        from hexagon.support.storage import (
            HEXAGON_STORAGE_APP,
            HexagonStorageKeys,
            load_user_data,
        )

        local_options = (
            load_user_data(HexagonStorageKeys.options.value, app=HEXAGON_STORAGE_APP)
            or {}
        )

        super().__init__(settings_cls, local_options)


class KeymapOptions(BaseSettings):
    create_dir: str = "c-p"


class Options(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HEXAGON_")

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

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ):
        return (
            init_settings,
            env_settings,
            UserDataSettingsSource(settings_cls),
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
