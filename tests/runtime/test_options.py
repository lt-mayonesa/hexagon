import os
import shutil
from pathlib import Path

import pytest
from ruamel.yaml import YAML

from hexagon.runtime.options import get_options, CLI_OPTIONS_FILE_NAME

_TEST_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".options-test"))


@pytest.fixture(autouse=True)
def clean_test_dir():
    if os.path.exists(_TEST_DIR):
        shutil.rmtree(_TEST_DIR)
    Path(_TEST_DIR).mkdir(exist_ok=True, parents=True)
    yield
    if os.path.exists(_TEST_DIR):
        shutil.rmtree(_TEST_DIR)


def _write_cli_options_yml(content: dict) -> str:
    path = os.path.join(_TEST_DIR, CLI_OPTIONS_FILE_NAME)
    with open(path, "w") as f:
        YAML().dump(content, f)
    return _TEST_DIR


def _clear_env(monkeypatch):
    for key in list(os.environ.keys()):
        if key.startswith("HEXAGON_"):
            monkeypatch.delenv(key, raising=False)


def test_get_options_returns_defaults_when_no_sources(monkeypatch):
    """
    Given no envvars, no cli_options.yml, and no app.yml options.
    When get_options is called.
    Then default values are used.
    """
    _clear_env(monkeypatch)
    opts = get_options({})
    assert opts.theme == "default"


def test_app_yml_options_applied(monkeypatch):
    """
    Given app.yml has cli.options with theme=dark.
    And no envvars or cli_options.yml override.
    When get_options is called with those init_settings.
    Then theme=dark is applied.
    """
    _clear_env(monkeypatch)
    opts = get_options({"theme": "dark"})
    assert opts.theme == "dark"


def test_cli_options_yml_overrides_app_yml(monkeypatch):
    """
    Given app.yml has theme=dark.
    And cli_options.yml has theme=result_only.
    When get_options is called.
    Then theme=result_only wins (cli_options.yml > app.yml).
    """
    _clear_env(monkeypatch)
    project_path = _write_cli_options_yml({"theme": "result_only"})
    opts = get_options({"theme": "dark"}, project_path=project_path)
    assert opts.theme == "result_only"


def test_envvar_overrides_cli_options_yml(monkeypatch):
    """
    Given cli_options.yml has theme=result_only.
    And HEXAGON_THEME=no_border envvar is set.
    When get_options is called.
    Then theme=no_border wins (envvars > cli_options.yml).
    """
    _clear_env(monkeypatch)
    monkeypatch.setenv("HEXAGON_THEME", "no_border")
    project_path = _write_cli_options_yml({"theme": "result_only"})
    opts = get_options({"theme": "dark"}, project_path=project_path)
    assert opts.theme == "no_border"


def test_envvar_overrides_app_yml_directly(monkeypatch):
    """
    Given app.yml has theme=dark.
    And HEXAGON_THEME=no_border envvar is set.
    And no cli_options.yml exists.
    When get_options is called.
    Then theme=no_border wins (envvars > app.yml).
    """
    _clear_env(monkeypatch)
    monkeypatch.setenv("HEXAGON_THEME", "no_border")
    opts = get_options({"theme": "dark"})
    assert opts.theme == "no_border"


def test_missing_cli_options_yml_does_not_error(monkeypatch):
    """
    Given project_path is set but cli_options.yml does not exist.
    When get_options is called.
    Then it falls back to app.yml options without error.
    """
    _clear_env(monkeypatch)
    opts = get_options({"theme": "dark"}, project_path=_TEST_DIR)
    assert opts.theme == "dark"


def test_cli_options_file_name_constant():
    """
    The CLI_OPTIONS_FILE_NAME constant should be 'cli_options.yml'.
    """
    assert CLI_OPTIONS_FILE_NAME == "cli_options.yml"
