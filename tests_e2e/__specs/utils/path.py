import os

_e2e_tests_folder_path = os.path.realpath(
    os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
)


def e2e_test_folder_path(test_file: str):
    return os.path.join(
        _e2e_tests_folder_path,
        os.path.relpath(
            os.path.join(
                os.path.dirname(test_file), os.path.basename(test_file).split(".")[0]
            ),
            os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir)),
        ),
    )
