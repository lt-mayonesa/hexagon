import datetime
import os
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

CLI_OPTIONS_FILE_NAME = "cli_options.yml"


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


class CliOptionsFileSettingsSource(InitSettingsSource):
    """Loads options from a cli_options.yml file next to the project's app.yaml."""

    def __init__(self, settings_cls: type[BaseSettings], options_file_path: str):
        from hexagon.runtime.yaml import read_file

        content = read_file(options_file_path) or {}
        super().__init__(settings_cls, dict(content))


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
    cwd_tools_disabled: Optional[bool] = False
    agent_mode: Optional[bool] = False
    view_mode: Optional[str] = "tree"
    view_mode_direction: Optional[str] = "rtl"
    view_mode_separator: Optional[str] = " | "

    # Set by get_options() before instantiation so settings_customise_sources can read it
    _cli_options_file_path: str = None

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ):
        sources = [env_settings]
        if cls._cli_options_file_path and os.path.isfile(cls._cli_options_file_path):
            sources.append(
                CliOptionsFileSettingsSource(settings_cls, cls._cli_options_file_path)
            )
        sources += [init_settings, UserDataSettingsSource(settings_cls)]
        return tuple(sources)


def get_options(init_settings: dict, project_path: Optional[str] = None) -> Options:
    Options._cli_options_file_path = (
        os.path.join(project_path, CLI_OPTIONS_FILE_NAME) if project_path else None
    )
    try:
        return Options(**init_settings)
    except ValidationError as errors:
        raise YamlValidationError(errors)


def update_options(opt: Options) -> Options:
    _save_settings_to_source(opt)
    return opt.copy()
