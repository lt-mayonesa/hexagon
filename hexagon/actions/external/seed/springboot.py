from typing import Dict, NamedTuple
from hexagon.utils.monad import IdentityMonad
from functools import partial
from InquirerPy import inquirer
import requests
import zipfile
import tempfile
import os
import subprocess


def __id_name_to_choice(id_name: Dict) -> Dict:
    return {"name": id_name["name"], "value": id_name["id"]}


map_id_name_to_choice = partial(map, __id_name_to_choice)


class SpringBootSeedOptions(NamedTuple):
    project_type: str
    language: str
    springboot_version: str
    group: str
    artifact: str
    name: str
    description: str
    package_name: str
    packaging: str
    java_version: str


def scaffold_springboot(options: SpringBootSeedOptions = None):
    initializr_data = requests.get("https://start.spring.io/metadata/client").json()

    project_type = (options and options.project_type) or inquirer.select(
        message="Project type",
        choices=IdentityMonad(initializr_data["type"]["values"])
        .bind(partial(filter, lambda type: type["tags"]["format"] == "project"))
        .bind(map_id_name_to_choice)
        .value,
        default=initializr_data["type"]["default"],
    ).execute()

    language = (options and options.language) or inquirer.select(
        message="Language",
        choices=IdentityMonad(initializr_data["language"]["values"])
        .bind(map_id_name_to_choice)
        .value,
        default=initializr_data["language"]["default"],
    ).execute()

    springboot_version = (options and options.springboot_version) or inquirer.select(
        message="Spring Boot Version",
        choices=IdentityMonad(initializr_data["bootVersion"]["values"])
        .bind(map_id_name_to_choice)
        .value,
        default=initializr_data["bootVersion"]["default"],
    ).execute()

    group = (options and options.group) or inquirer.text(
        message="Group", default=initializr_data["groupId"]["default"]
    ).execute()

    artifact = (options and options.artifact) or inquirer.text(
        message="Artifact", default=initializr_data["artifactId"]["default"]
    ).execute()

    name = (options and options.name) or inquirer.text(
        message="Name", default=artifact
    ).execute()

    description = (options and options.description) or inquirer.text(
        message="Description", default=initializr_data["description"]["default"]
    ).execute()

    package_name = (options and options.package_name) or inquirer.text(
        message="Package name", default=f"{group}.{artifact}"
    ).execute()

    packaging = (options and options.packaging) or inquirer.select(
        message="Packaging",
        choices=IdentityMonad(initializr_data["packaging"]["values"])
        .bind(map_id_name_to_choice)
        .value,
        default=initializr_data["packaging"]["default"],
    ).execute()

    java_version = (options and options.java_version) or inquirer.select(
        message="Java Version",
        choices=IdentityMonad(initializr_data["javaVersion"]["values"])
        .bind(map_id_name_to_choice)
        .value,
        default=initializr_data["javaVersion"]["default"],
    ).execute()

    with requests.get(
        url="https://start.spring.io/starter.zip",
        params={
            "type": project_type,
            "language": language,
            "bootVersion": springboot_version,
            "baseDir": name,
            "groupId": group,
            "artifactId": artifact,
            "name": name,
            "description": description,
            "packageName": package_name,
            "packaging": packaging,
            "javaVersion": java_version,
        },
        stream=True,
    ) as download:
        download.raise_for_status()
        with tempfile.NamedTemporaryFile("wb") as zipped_file:
            for chunk in download.iter_content(chunk_size=8192):
                zipped_file.write(chunk)

            with zipfile.ZipFile(zipped_file.name, "r") as zip_ref:
                zip_ref.extractall(os.getcwd())

    project_path = os.path.join(os.getcwd(), name)

    subprocess.check_call("chmod +x ./gradlew", cwd=project_path, shell=True)
