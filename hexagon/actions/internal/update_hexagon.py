import sys

from hexagon.runtime.update.shared import (
    check_hexagon_version,
    get_hexagon_changelog,
    perform_hexagon_update,
)
from hexagon.support.input.prompt import prompt
from hexagon.support.output.printer import log


def main(tool, env, env_args, cli_args):
    """
    Manually check for and install hexagon updates.

    This bypasses time throttle and always checks PyPI for latest version.
    Shows changelog and prompts for confirmation before updating.
    """
    with log.status(_("msg.support.update.hexagon.checking_new_versions")):
        current_version, latest_version = check_hexagon_version()

    if current_version >= latest_version:
        log.info(
            _("msg.actions.internal.update_hexagon.already_latest").format(
                version=current_version
            )
        )
        return

    log.info(
        _("msg.support.update.hexagon.new_version_available").format(
            latest_version=latest_version
        )
    )

    with log.status(_("msg.support.update.hexagon.fetching_changelog")):
        changelog = get_hexagon_changelog(current_version)

    log.example(changelog, syntax="md")

    if not prompt.confirm(
        _("action.support.update.hexagon.confirm_update"), default=True
    ):
        log.info(_("msg.actions.internal.update_hexagon.cancelled"))
        return

    with log.status(_("msg.support.update.hexagon.updating")):
        perform_hexagon_update()

    log.info(_("msg.support.update.hexagon.updated"))
    log.finish()
    sys.exit(1)
