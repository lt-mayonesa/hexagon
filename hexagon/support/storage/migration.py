import os

from hexagon.domain.cli import Cli


def migrate_storage_to_command_key(cli: Cli):
    """
    Migrate storage directory from the legacy cli.name-based path to cli.command.

    The old storage key was derived from cli.name.lower(), which produces
    directories with spaces and special characters. The new key is cli.command,
    which is always a clean shell identifier.

    Cases:
    - Only old dir exists: rename it to the new path (atomic, silent).
    - Neither or only new dir exists: no-op.
    - Both dirs exist: do nothing, emit a warning asking for maintainer help.
    """
    from hexagon.support.storage import _get_storage_dir_path

    storage_base = _get_storage_dir_path()
    old_key = cli.name.lower()
    new_key = cli.command

    if old_key == new_key:
        return

    old_dir = os.path.join(storage_base, old_key)
    new_dir = os.path.join(storage_base, new_key)

    old_exists = os.path.isdir(old_dir)
    new_exists = os.path.isdir(new_dir)

    if not old_exists:
        return

    if old_exists and new_exists:
        from hexagon.support.output.printer import log

        log.panel(
            _("msg.support.storage.migration.conflict").format(
                old_dir=old_dir, new_dir=new_dir
            ),
            title=_("msg.support.storage.migration.conflict_title"),
        )
        return

    os.rename(old_dir, new_dir)
