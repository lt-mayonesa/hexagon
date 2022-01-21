from hexagon.actions.external.seed.react import scaffold_react
from hexagon.actions.external.seed.springboot import scaffold_springboot
from InquirerPy import inquirer

from hexagon.support.tracer import tracer

SEEDS = ["springboot", "react", "nextjs"]


def main(tool, env, env_args, cli_args):
    seed = None

    if isinstance(env_args, str) and env_args in SEEDS:
        seed = env_args

    if (
        cli_args
        and cli_args.length
        and isinstance(cli_args[0], str)
        and cli_args[0] in SEEDS
    ):
        seed = cli_args[0]

    seed = tracer.tracing(
        seed
        or inquirer.fuzzy(message="¿Qué seed querés usar?", choices=SEEDS).execute()
    )

    if seed == "springboot":
        scaffold_springboot()
    elif seed == "react":
        scaffold_react()
    elif seed == "nextjs":
        scaffold_react(use_next_js=True)
