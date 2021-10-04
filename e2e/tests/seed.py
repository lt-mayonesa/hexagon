import subprocess
from e2e.tests.utils.hexagon_spec import as_a_user
from e2e.tests.utils.path import e2e_test_folder_path
import os
from shutil import rmtree
import time
import requests
import signal

test_folder_path = os.path.join(e2e_test_folder_path(__file__))
springboot_folder_path = os.path.join(test_folder_path, "springboot")


def __clean_springboot() -> str:
    if not os.path.exists(springboot_folder_path):
        os.mkdir(springboot_folder_path)

    created_project_path = os.path.join(springboot_folder_path, "demo")

    if os.path.exists(created_project_path):
        rmtree(created_project_path)

    return created_project_path


def __assert_gradle_works(created_project_path: str):
    subprocess.check_call("./gradlew build", shell=True, cwd=created_project_path)


def __assert_react_app_works(created_project_path: str):
    with open(os.path.join(created_project_path, ".env"), "w") as env_file:
        env_file.write("BROWSER=none")

    local_server_process = subprocess.Popen(
        "npm start", shell=True, cwd=created_project_path
    )

    time.sleep(5)

    try:
        response = requests.get("http://localhost:3000")
        assert response.status_code == 200
    finally:
        local_server_process.send_signal(signal.SIGINT)


def test_seed_springboot():
    created_project_path = __clean_springboot()

    (
        as_a_user(__file__)
        .run_hexagon(cwd=springboot_folder_path)
        .enter()
        .enter()
        .arrow_down()
        .carriage_return()
        .arrow_down()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .exit(timeout_in_seconds=60)
    )

    __assert_gradle_works(created_project_path)


def test_seed_react():
    react_folder_path = os.path.join(test_folder_path, "react")

    if not os.path.exists(react_folder_path):
        os.mkdir(react_folder_path)

    created_project_path = os.path.join(react_folder_path, "react-seed-test")

    if os.path.exists(created_project_path):
        rmtree(created_project_path)

    (
        as_a_user(__file__)
        .run_hexagon(cwd=react_folder_path)
        .enter()
        .arrow_down()
        .carriage_return()
        .input("react-seed-test")
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .exit(timeout_in_seconds=300)
    )

    __assert_react_app_works(created_project_path)


def test_seed_nextjs():
    nextjs_folder_path = os.path.join(test_folder_path, "nextjs")

    if not os.path.exists(nextjs_folder_path):
        os.mkdir(nextjs_folder_path)

    created_project_path = os.path.join(nextjs_folder_path, "nextjs-seed-test")

    if os.path.exists(created_project_path):
        rmtree(created_project_path)

    (
        as_a_user(__file__)
        .run_hexagon(cwd=nextjs_folder_path)
        .enter()
        .arrow_down()
        .arrow_down()
        .carriage_return()
        .input("nextjs-seed-test")
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .exit(timeout_in_seconds=300)
    )

    __assert_react_app_works(created_project_path)


def test_seed_type_as_env_arg():
    created_project_path = __clean_springboot()

    (
        as_a_user(__file__)
        .run_hexagon(["seed-spring-test"], cwd=springboot_folder_path)
        .arrow_down()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .carriage_return()
        .exit()
    )

    __assert_gradle_works(created_project_path)
