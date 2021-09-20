from hexagon.support.storage import store_user_data
from hexagon.support.hooks import HexagonHooks
from hexagon.support.hooks.hook import HookSubscription

SUBSCRIPTION_NAME = "test-plugin"


def main():
    HexagonHooks.start.subscribe(
        HookSubscription(SUBSCRIPTION_NAME, lambda _: store_user_data("started", "1"))
    )
    HexagonHooks.tool_selected.subscribe(
        HookSubscription(
            SUBSCRIPTION_NAME,
            lambda selection: store_user_data("tool_selected", selection.selected.name),
        )
    )
    HexagonHooks.env_selected.subscribe(
        HookSubscription(
            SUBSCRIPTION_NAME,
            lambda selection: store_user_data("env_selected", selection.selected.name),
        )
    )
    HexagonHooks.before_tool_executed.subscribe(
        HookSubscription(
            SUBSCRIPTION_NAME,
            lambda parameters: store_user_data(
                "execution_parameters", parameters.tool.name
            ),
        )
    )
    HexagonHooks.tool_executed.subscribe(
        HookSubscription(
            SUBSCRIPTION_NAME,
            lambda data: store_user_data("execution_data", data.tool.name),
        )
    )
    HexagonHooks.end.subscribe(
        HookSubscription(SUBSCRIPTION_NAME, lambda _: store_user_data("ended", "1"))
    )
