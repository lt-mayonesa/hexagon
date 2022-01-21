from enum import Enum
import datetime

from InquirerPy import inquirer

from hexagon.domain import get_options
from hexagon.domain.options import update_options
from hexagon.support.printer import log, translator
from hexagon.support.storage import store_local_data, get_local_data_dir
from hexagon.support.analytics import google_analytics

_ = translator
_data_file_name = "events_" + datetime.date.today().isoformat()


class EventType(Enum):
    session = "session"
    user = "user_event"
    system = "system_event"


class UserEvent(Enum):
    selection = "selection"


class SessionEvent(Enum):
    start = "start"
    end = "end"


class SystemEvent(Enum):
    execution = "execution"


def session(e: SessionEvent):
    s = {
        "datetime": str(datetime.datetime.now()),
        "type": EventType.session.value,
        "name": e.value,
    }
    _send_event(s)


def user_event(e: UserEvent, **kwargs):
    s = {
        **{
            "datetime": str(datetime.datetime.now()),
            "type": EventType.user.value,
            "name": e.value,
        },
        **kwargs,
    }
    _send_event(s)


def system_event(e: SystemEvent, **kwargs):
    s = {
        **{
            "datetime": str(datetime.datetime.now()),
            "type": EventType.system.value,
            "name": e.value,
        },
        **kwargs,
    }
    _send_event(s)


def _send_event(s):
    # TODO: actually execute in background
    store_local_data(_data_file_name, str(s))
    if _send_telemetry():
        google_analytics.event(**s)


def _send_telemetry():
    opt = get_options()
    if opt.send_telemetry is None:
        log.info(_("msg.support.analytics.telemetry_notice"))
        log.info(
            _("msg.support.analytics.telemetry_directory").format(
                directory=get_local_data_dir()
            ),
            gap_start=1,
        )
        opt.send_telemetry = inquirer.confirm(
            message=_("action.support.analytics.confirm_telemetry"), default=True
        ).execute()
        update_options(opt)
    return opt.send_telemetry
