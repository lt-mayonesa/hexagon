import subprocess
from InquirerPy import inquirer
import os


def scaffold_react(use_next_js=False):
    name = inquirer.text(message="Project Name, e.g: my-react-app").execute()
    package_manager = inquirer.select(
        message="Package Manager", choices=["npm", "yarn"], default="npm"
    ).execute()
    use_typescript = inquirer.confirm(message="TypeScript", default=True).execute()

    app = "next-app" if use_next_js else "react-app"

    create_command = (
        f"yarn create {app}" if package_manager == "yarn" else f"npx create-{app}"
    ) + f" {name}"

    if package_manager == "npm":
        create_command += " --use-npm"

    if use_typescript:
        if use_next_js:
            create_command += "--typescript"
        else:
            create_command += " --template typescript"

    subprocess.check_call(create_command, shell=True)

    if use_next_js:
        cwd = os.path.join(os.getcwd(), name)
        if package_manager == "yarn":
            subprocess.check_call("yarn run build", shell=True, cwd=cwd)
        else:
            subprocess.check_call("npm run build", shell=True, cwd=cwd)
