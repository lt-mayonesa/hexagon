import os


def e2e_test_folder_path(test_file: str):
    return os.path.realpath(os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        os.path.basename(test_file).split('.')[0]
    ))
