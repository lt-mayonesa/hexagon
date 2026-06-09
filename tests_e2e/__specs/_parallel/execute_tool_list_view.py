import os

from tests_e2e.framework.hexagon_spec import as_a_user


def _alias_file_path(spec):
    return os.path.join(spec.test_dir, "home-aliases.txt")


def _write_alias_file(spec):
    with open(_alias_file_path(spec), "w") as f:
        f.write("previous line\n")


def test_list_view_shows_all_tools_in_single_prompt():
    """
    Given view_mode: list.
    When hexagon is run interactively with no arguments.
    Then a single flat fuzzy prompt is shown that contains root tools and nested
    tools (from all groups) — no secondary group prompt is ever shown.
    """
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        # The prompt renders all leaf tools in one flat list.
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "A Root Tool",
                "A Root Tool Without Alias",
                "Child Tool | A Group",
            ],
            discard_until_first_match=True,
        )
        # Select the first tool (A Root Tool) and verify execution.
        .enter()
        .then_output_should_be(["root tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_executes_root_level_tool():
    """
    Given view_mode: list.
    When the user selects a root-level tool from the flat prompt.
    Then the tool executes and produces the correct output.
    """
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        .then_output_should_be(
            [["Hi, which tool would you like to use today?"]],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["root tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_executes_tool_inside_group():
    """
    Given view_mode: list.
    When the user selects a tool that lives inside a group using args.
    Then the tool executes correctly — no secondary group prompt appears.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["group", "child-tool"])
        .then_output_should_be(["child tool output"])
        .exit()
    )


def test_list_view_executes_deeply_nested_tool():
    """
    Given view_mode: list.
    When the user selects a tool nested under group > sub-group using args.
    Then the tool executes correctly.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["group", "sub-group", "nested-tool"])
        .then_output_should_be(["nested tool output"])
        .exit()
    )


def test_list_view_builtin_tools_appear_in_flat_list():
    """
    Given view_mode: list.
    When the flat prompt is shown.
    Then the built-in tools are visible alongside user tools.
    After verifying their presence, selecting the first tool still works.
    """
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "Save Last Command",
                "Replay Last Command",
            ],
            discard_until_first_match=True,
        )
        # Select the first tool (A Root Tool) to exit cleanly.
        .enter()
        .then_output_should_be(["root tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_breadcrumb_rtl_is_default():
    """
    Given view_mode: list with no explicit view_mode_direction.
    When the flat prompt is shown.
    Then nested tools display as 'tool-name | group-name' (rtl, deepest first).
    After verification, select a tool to exit cleanly.
    """
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        .then_output_should_be(
            [["Child Tool | A Group"]],
            discard_until_first_match=True,
        )
        # Select the first tool to exit cleanly.
        .enter()
        .then_output_should_be(["root tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_breadcrumb_ltr_via_option():
    """
    Given view_mode_direction: ltr (via env var).
    When the flat prompt is shown.
    Then nested tools display as 'group-name | tool-name' (ltr, root first).
    """
    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                "HEXAGON_THEME": "no_border",
                "HEXAGON_VIEW_MODE_DIRECTION": "ltr",
            }
        )
        .then_output_should_be(
            [["A Group | Child Tool"]],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["root tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_custom_separator_via_option():
    """
    Given view_mode_separator: ' > ' (via env var).
    When the flat prompt is shown.
    Then '>' is used as separator instead of '|'.
    """
    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                "HEXAGON_THEME": "no_border",
                "HEXAGON_VIEW_MODE_SEPARATOR": " > ",
            }
        )
        .then_output_should_be(
            [["Child Tool > A Group"]],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["root tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_root_tool_has_no_breadcrumb():
    """
    Given a root-level tool (no group ancestor).
    When the flat prompt is shown.
    Then that tool's entry shows only its name, without a separator.
    Verified by checking the display and executing the root tool.
    """
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        .then_output_should_be(
            [["A Root Tool"]],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["root tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_args_resolve_root_tool():
    """
    Given view_mode: list and a root-level tool name as an argument.
    When hexagon is run with that argument.
    Then the tool executes without any interactive prompt.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["root-tool"])
        .then_output_should_be(["root tool output"])
        .exit()
    )


def test_list_view_args_resolve_group_tool_tree_style():
    """
    Given view_mode: list and positional args 'group child-tool'.
    When hexagon is run with those arguments.
    Then the tool executes without any interactive prompt.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["group", "child-tool"])
        .then_output_should_be(["child tool output"])
        .exit()
    )


def test_list_view_args_resolve_nested_group_tree_style():
    """
    Given view_mode: list and positional args 'group sub-group nested-tool'.
    When hexagon is run with those arguments.
    Then the tool executes without any interactive prompt.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["group", "sub-group", "nested-tool"])
        .then_output_should_be(["nested tool output"])
        .exit()
    )


def test_list_view_env_selection_prompt_still_appears():
    """
    Given view_mode: list and a tool that requires an environment.
    When the tool is selected via argument but no env arg is given.
    Then the environment selection prompt still appears.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["tool-with-env"])
        .then_output_should_be(
            [["On which environment?"]],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["dev output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_env_selection_by_arg_works():
    """
    Given view_mode: list and positional args 'tool-with-env dev'.
    When hexagon is run with those arguments.
    Then the correct env is resolved without prompting.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["tool-with-env", "dev"])
        .then_output_should_be(["dev output"])
        .exit()
    )


def test_list_view_trace_root_tool_with_alias():
    """
    Given view_mode: list.
    When a root-level tool with an alias is selected interactively.
    Then 'To run this tool again do:' shows both the full-name and alias forms.
    """
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        .then_output_should_be(
            [["Hi, which tool would you like to use today?"]],
            discard_until_first_match=True,
        )
        # First item: A Root Tool (alias: rt)
        .enter()
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test root-tool",
                "or:",
                "hexagon-test rt",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_list_view_trace_root_tool_without_alias():
    """
    Given view_mode: list.
    When a root-level tool without an alias is selected interactively.
    Then only the full-name form is shown (no 'or:' line).
    """
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        .then_output_should_be(
            [["Hi, which tool would you like to use today?"]],
            discard_until_first_match=True,
        )
        # Navigate to second item: A Root Tool Without Alias
        .arrow_down()
        .enter()
        .then_output_should_be(
            ["To run this tool again do:", "hexagon-test root-tool-no-alias"],
            discard_until_first_match=True,
        )
        .then_output_should_not_contain(["or:", "hexagon-test rt"])
        .exit()
    )


def test_list_view_trace_group_tool():
    """
    Given view_mode: list.
    When a tool inside a group is selected interactively from the flat list.
    Then the trace is 'group child-tool' (tree-style replayable path) and both
    group and tool aliases appear in the 'or:' line.
    """
    (
        as_a_user(__file__)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        .then_output_should_be(
            [["Hi, which tool would you like to use today?"]],
            discard_until_first_match=True,
        )
        # Navigate to third item: Child Tool | A Group
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test group child-tool",
                "or:",
                "hexagon-test g ct",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_list_view_trace_tool_with_env_prompt():
    """
    Given view_mode: list.
    When a tool with envs is selected by argument and the env is chosen interactively.
    Then the trace includes the env: 'tool-with-env dev'.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["tool-with-env"], os_env_vars={"HEXAGON_THEME": "no_border"})
        .then_output_should_be(
            [["On which environment?"]],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(
            [
                "To run this tool again do:",
                "hexagon-test tool-with-env dev",
                "or:",
                "hexagon-test twe d",
            ],
            discard_until_first_match=True,
        )
        .exit()
    )


def test_list_view_no_trace_when_all_args_provided():
    """
    Given view_mode: list and all positional args fully specified.
    When hexagon runs without any prompting.
    Then 'To run this tool again do:' is NOT shown.
    """
    (
        as_a_user(__file__)
        .run_hexagon(["tool-with-env", "dev"])
        .then_output_should_not_contain(["To run this tool again do:"])
        .exit()
    )


def test_list_view_replay_root_tool_by_name():
    """
    Given view_mode: list and a root tool was previously run interactively.
    When 'replay' is invoked by name.
    Then the previous command is re-executed without prompting.
    """
    spec = as_a_user(__file__).run_hexagon().enter().exit()

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(["replay"])
        .then_output_should_be(["root tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_replay_root_tool_by_alias():
    """
    Given view_mode: list and a root tool was previously run.
    When replay is invoked via its alias 'r'.
    Then the previous command is re-executed.
    """
    spec = as_a_user(__file__).run_hexagon(["root-tool"]).exit()

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(["r"])
        .then_output_should_be(["root tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_replay_group_tool():
    """
    Given view_mode: list and a group tool was previously run.
    When 'replay' is invoked.
    Then the exact nested tool is re-executed without prompting.
    """
    spec = as_a_user(__file__).run_hexagon(["group", "child-tool"]).exit()

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(["r"])
        .then_output_should_be(["child tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_replay_group_tool_with_env():
    """
    Given view_mode: list and a tool with env was previously run.
    When 'replay' is invoked.
    Then the same tool with the same env is re-executed.
    """
    spec = as_a_user(__file__).run_hexagon(["tool-with-env", "dev"]).exit()

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(["r"])
        .then_output_should_be(["dev output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_replay_root_tool_by_prompt():
    """
    Given view_mode: list and a root tool was previously run.
    When hexagon is run again and 'replay' is invoked by name.
    Then the previous command is re-executed.
    """
    spec = as_a_user(__file__).run_hexagon(["root-tool"]).exit()

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(["replay"])
        .then_output_should_be(["root tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_save_alias_for_root_tool():
    """
    Given view_mode: list and a root tool was previously run.
    When save-alias is invoked by argument.
    Then the alias is saved with the correct command ('hexagon-test root-tool').
    """
    spec = (
        as_a_user(__file__)
        .executing_first(_write_alias_file)
        .run_hexagon(["root-tool"])
        .exit()
    )

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(["save-alias"])
        .input("my-root-alias")
        .then_output_should_be(
            [
                "# added by hexagon",
                'alias my-root-alias="hexagon-test root-tool"',
            ],
            discard_until_first_match=True,
        )
        .exit()
    )

    with open(_alias_file_path(spec), "r") as f:
        content = f.read()
    assert 'alias my-root-alias="hexagon-test root-tool"' in content


def test_list_view_save_alias_for_group_tool():
    """
    Given view_mode: list and a group tool was previously run.
    When save-alias is invoked.
    Then the alias is saved with the full tree-style command
    ('hexagon-test group child-tool').
    """
    spec = (
        as_a_user(__file__)
        .executing_first(_write_alias_file)
        .run_hexagon(["group", "child-tool"])
        .exit()
    )

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(["save-alias"])
        .input("my-group-alias")
        .then_output_should_be(
            [
                "# added by hexagon",
                'alias my-group-alias="hexagon-test group child-tool"',
            ],
            discard_until_first_match=True,
        )
        .exit()
    )

    with open(_alias_file_path(spec), "r") as f:
        content = f.read()
    assert 'alias my-group-alias="hexagon-test group child-tool"' in content


def test_list_view_activated_via_env_var():
    """
    Given a YAML with no view_mode set (app_tree.yml) and HEXAGON_VIEW_MODE=list.
    When hexagon is run interactively.
    Then a single flat prompt is shown (list view activated via env var) with
    group children visible directly — no secondary group prompt needed.
    """
    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                "HEXAGON_THEME": "no_border",
                "HEXAGON_VIEW_MODE": "list",
                "HEXAGON_CONFIG_FILE": "app_tree.yml",
            }
        )
        # In list mode the group is exploded — child tools appear with breadcrumb.
        .then_output_should_be(
            [["Child Tool | A Group"]],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["root tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_default_is_tree_when_not_set():
    """
    Given a YAML with no view_mode set (defaults to tree).
    When hexagon is run interactively and the user navigates into a group.
    Then a secondary group prompt appears (tree behaviour confirmed).
    """
    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                "HEXAGON_THEME": "no_border",
                "HEXAGON_CONFIG_FILE": "app_tree.yml",
            }
        )
        .then_output_should_be(
            [["Hi, which tool would you like to use today?"]],
            discard_until_first_match=True,
        )
        # Navigate to the "A Group" entry (3rd item) and enter it.
        .arrow_down()
        .arrow_down()
        .enter()
        # A new nested prompt must appear (tree mode) showing group children.
        .then_output_should_be(
            [["Hi, which tool would you like to use today?", "Child Tool"]],
            discard_until_first_match=True,
        )
        # Select child-tool from the sub-prompt to exit cleanly.
        .enter()
        .then_output_should_be(["child tool output"], discard_until_first_match=True)
        .exit()
    )


def test_list_view_tree_mode_explicit():
    """
    Given view_mode: tree explicitly set via env var.
    When hexagon is run interactively and the user navigates into a group.
    Then a secondary group prompt appears (tree behaviour confirmed).
    """
    (
        as_a_user(__file__)
        .run_hexagon(
            os_env_vars={
                "HEXAGON_THEME": "no_border",
                "HEXAGON_VIEW_MODE": "tree",
            }
        )
        .then_output_should_be(
            [["Hi, which tool would you like to use today?"]],
            discard_until_first_match=True,
        )
        # Navigate to the "A Group" entry (3rd item) and enter it.
        .arrow_down()
        .arrow_down()
        .enter()
        # A new nested prompt must appear (tree mode) showing group children.
        .then_output_should_be(
            [["Hi, which tool would you like to use today?", "Child Tool"]],
            discard_until_first_match=True,
        )
        .enter()
        .then_output_should_be(["child tool output"], discard_until_first_match=True)
        .exit()
    )
