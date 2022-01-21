from hexagon.support.hooks import HexagonHooks
from hexagon.support.wax import Selection
from hexagon.support.hooks.hook import HookSubscription, HookSubscrptionType
from hexagon.support.analytics import SessionEvent, SystemEvent, UserEvent
from hexagon.support import analytics

SUBSCRIPTION_NAME = "analytics"


def _track_selection(data: Selection):
    analytics.user_event(
        UserEvent.selection,
        mode=data.type.value,
        selected=data.selected.name,
        **(data.additional_data if data.additional_data else {}),
    )


def main():
    HexagonHooks.start.subscribe(
        HookSubscription(
            SUBSCRIPTION_NAME, lambda data: analytics.session(SessionEvent.start)
        )
    )

    HexagonHooks.end.subscribe(
        HookSubscription(
            SUBSCRIPTION_NAME,
            lambda data: analytics.session(SessionEvent.end),
            type=HookSubscrptionType.background,
        )
    )

    HexagonHooks.tool_selected.subscribe(
        HookSubscription(
            SUBSCRIPTION_NAME, _track_selection, type=HookSubscrptionType.background
        )
    )

    HexagonHooks.env_selected.subscribe(
        HookSubscription(
            SUBSCRIPTION_NAME, _track_selection, type=HookSubscrptionType.background
        )
    )

    HexagonHooks.tool_executed.subscribe(
        HookSubscription(
            SUBSCRIPTION_NAME,
            lambda data: analytics.system_event(
                SystemEvent.execution, tool=data.tool.name, duration=data.duration
            ),
            type=HookSubscrptionType.background,
        )
    )
