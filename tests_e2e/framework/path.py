import os


def e2e_test_folder_path(test_file: str):
    """
    Find test_resources target folder:

    - dynamically crawl up the tree from the test file until we find a directory named "tests_e2e"
    - identify test_file relative path from __specs directory
    - return path to test_resources joining the two

    :param test_file: the __file__ of the test
    :return: the path to the test_resources directory
    """
    path_with_filename = os.path.realpath(
        test_file.replace("__specs", "__test_resources")
    )
    dirname = os.path.dirname(path_with_filename)
    filename = os.path.splitext(os.path.basename(path_with_filename))[0]
    return os.path.join(dirname, filename)
