import os.path

from tests_e2e.__specs.utils.hexagon_spec import as_a_user


def test_dir_with_hexagon_tool_execute_extra_tool():
    spec = as_a_user(__file__)
    (
        spec.run_hexagon(
            test_dir=os.path.join(spec.test_dir, "cli"),
            execution_cwd=os.path.join(spec.test_dir, "dir_with_tools"),
        )
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "5/5",
                "Extra tool",
                "Normal tool",
                "Save Last Command",
                "Replay Last Command",
                "Create A New Tool",
            ],
        )
        .enter()
        .then_output_should_be(
            [
                ["Hi, which tool would you like to use today?", "Extra tool"],
                "executed extra tool",
            ]
        )
        .exit()
    )


def test_dir_with_hexagon_tool_execute_normal_tool():
    spec = as_a_user(__file__)
    (
        spec.run_hexagon(
            test_dir=os.path.join(spec.test_dir, "cli"),
            execution_cwd=os.path.join(spec.test_dir, "dir_with_tools"),
        )
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "5/5",
                "Extra tool",
                "Normal tool",
                "Save Last Command",
                "Replay Last Command",
                "Create A New Tool",
            ],
        )
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                ["Hi, which tool would you like to use today?", "Normal tool"],
                "executed normal tool",
            ]
        )
        .exit()
    )


def test_dir_without_hexagon_tool_execute_normal_tool():
    spec = as_a_user(__file__)
    (
        spec.run_hexagon(
            test_dir=os.path.join(spec.test_dir, "cli"),
            execution_cwd=os.path.join(spec.test_dir, "dir_without_tools"),
        )
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "4/4",
                "Normal tool",
                "Save Last Command",
                "Replay Last Command",
                "Create A New Tool",
            ],
        )
        .enter()
        .then_output_should_be(
            [
                ["Hi, which tool would you like to use today?", "Normal tool"],
                "executed normal tool",
            ]
        )
        .exit()
    )


def test_dir_with_hexagon_tool_dont_load_if_disabled():
    spec = as_a_user(__file__)
    (
        spec.run_hexagon(
            test_dir=os.path.join(spec.test_dir, "cli_cwd_disabled"),
            execution_cwd=os.path.join(spec.test_dir, "dir_with_tools"),
        )
        .then_output_should_be(
            [
                "Hi, which tool would you like to use today?",
                "4/4",
                "Normal tool",
                "Save Last Command",
                "Replay Last Command",
                "Create A New Tool",
            ],
        )
        .enter()
        .then_output_should_be(
            [
                ["Hi, which tool would you like to use today?", "Normal tool"],
                "executed normal tool",
            ]
        )
        .exit()
    )
