from hexagon.runtime.execute.tool import _ensure_prompt
from hexagon.support.input.args.cli_args import CliArgs


def test_ensure_prompt_initializes_prompt_when_not_set():
    """
    Given a CliArgs instance that has not had _with_prompt called.
    When _ensure_prompt is called.
    Then cli_args.__prompt__ is initialized to a Prompt instance.
    """
    args = CliArgs(total_args=0)
    assert args.__prompt__ is None

    _ensure_prompt(args)

    assert args.__prompt__ is not None


def test_ensure_prompt_preserves_existing_prompt():
    """
    Given a CliArgs instance that already has a Prompt set via _with_prompt.
    When _ensure_prompt is called again.
    Then the original Prompt instance is not replaced.
    """
    from hexagon.support.input.prompt.prompt import Prompt

    args = CliArgs(total_args=0)
    original_prompt = Prompt()
    args._with_prompt(original_prompt)

    _ensure_prompt(args)

    assert args.__prompt__ is original_prompt


def test_ensure_prompt_makes_tool_prompt_callable_without_prior_setup():
    """
    Given a CliArgs initialized only via parse_cli_args (no _with_prompt call),
    as callers like replay.py do.
    When _ensure_prompt is called.
    Then cli_args.tool.prompt is callable without raising ValueError.
    """
    from hexagon.runtime.parse_args import parse_cli_args

    args = parse_cli_args(["some-tool"])
    assert args.__prompt__ is None

    _ensure_prompt(args)

    assert args.__prompt__ is not None
    assert args.tool.value == "some-tool"
