from tests_e2e.framework.hexagon_spec import as_a_user


def test_replay_last_command_by_prompt():
    spec = (
        as_a_user(__file__)
        .run_hexagon()
        .enter()
        .input("john")
        .input("10")
        .input("Argentina")
        .input("banana")
        .input("orange")
        .esc()
        .carriage_return()
        .exit()
    )

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(os_env_vars={"HEXAGON_THEME": "no_border"})
        .then_output_should_be(
            [
                "",
                "",
                "Hi, which tool would you like to use today?",
                "5/5",
                "Python Module Test",
                "Save Last Command",
                "Replay Last Command",
                "Create A New Tool",
                "Update CLI",
            ]
        )
        .arrow_down()
        .arrow_down()
        .enter()
        .then_output_should_be(
            [
                "",
                "replaying command: hexagon-test python-module john 10 --country=Argentina --likes=banana --likes=orange",
                "name: john",
                "age: 10",
                "country: Argentina",
                "likes: ['banana', 'orange']",
            ]
        )
        .exit()
    )


def test_replay_last_command_by_name():
    spec = (
        as_a_user(__file__)
        .run_hexagon()
        .enter()
        .input("john")
        .input("10")
        .input("Argentina")
        .input("banana")
        .input("orange")
        .esc()
        .carriage_return()
        .exit()
    )

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(["replay"])
        .then_output_should_be(
            [
                "name: john",
                "age: 10",
                "country: Argentina",
                "likes: ['banana', 'orange']",
            ]
        )
        .exit()
    )


def test_replay_last_command_by_alias():
    spec = (
        as_a_user(__file__)
        .run_hexagon()
        .enter()
        .input("john")
        .input("10")
        .input("Argentina")
        .input("banana")
        .input("orange")
        .esc()
        .carriage_return()
        .exit()
    )

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(["r"])
        .then_output_should_be(
            [
                "name: john",
                "age: 10",
                "country: Argentina",
                "likes: ['banana', 'orange']",
            ]
        )
        .exit()
    )


def test_replay_last_command_with_spaced_arg():
    spec = (
        as_a_user(__file__)
        .run_hexagon()
        .enter()
        .input("john")
        .input("10")
        .input("The Netherlands")
        .input("orange")
        .esc()
        .carriage_return()
        .exit()
    )

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(["replay"])
        .then_output_should_be(
            [
                "name: john",
                "age: 10",
                "country: The Netherlands",
                "likes: ['orange']",
            ]
        )
        .exit()
    )


def test_replay_last_command_with_complex_arg():
    spec = (
        as_a_user(__file__)
        .run_hexagon()
        .enter()
        .input("john")
        .input("10")
        .input('The "Netherlands"')
        .input("orange")
        .esc()
        .carriage_return()
        .exit()
    )

    (
        as_a_user(__file__, test_dir=spec.test_dir)
        .run_hexagon(["replay"])
        .then_output_should_be(
            [
                "name: john",
                "age: 10",
                'country: The "Netherlands"',
                "likes: ['orange']",
            ]
        )
        .exit()
    )
