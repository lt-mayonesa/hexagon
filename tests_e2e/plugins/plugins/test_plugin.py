import os
import time

from hexagon.support.hooks import HexagonHooks
from hexagon.support.hooks.hook import HookSubscription, HookSubscrptionType
from hexagon.support.storage import store_user_data

SUBSCRIPTION_NAME = "test-plugin"


def sleep_15_seconds(data):
    time.sleep(15)


def main():
    test_name = os.environ.get("HEXAGON_TEST_PLUGIN_TEST_NAME", "all_hooks")
    if test_name == "all_hooks":
        HexagonHooks.start.subscribe(
            HookSubscription(
                SUBSCRIPTION_NAME, lambda _: store_user_data("hook_start", "1")
            )
        )
        HexagonHooks.tool_selected.subscribe(
            HookSubscription(
                SUBSCRIPTION_NAME,
                lambda selection: store_user_data(
                    "hook_tool_selected-tool_name", selection.selected.name
                ),
            )
        )
        HexagonHooks.env_selected.subscribe(
            HookSubscription(
                SUBSCRIPTION_NAME,
                lambda selection: store_user_data(
                    "hook_env_selected-env_name", selection.selected.name
                ),
            )
        )
        HexagonHooks.before_tool_executed.subscribe(
            HookSubscription(
                SUBSCRIPTION_NAME,
                lambda parameters: store_user_data(
                    "hook_before_tool_executed-tool_name", parameters.tool.name
                ),
            )
        )
        HexagonHooks.tool_executed.subscribe(
            HookSubscription(
                SUBSCRIPTION_NAME,
                lambda data: store_user_data(
                    "hook_tool_executed-env_args", list(data.tool_env_args)
                ),
            )
        )
        HexagonHooks.end.subscribe(
            HookSubscription(
                SUBSCRIPTION_NAME, lambda _: store_user_data("hook_end", "1")
            )
        )
    elif test_name == "async_cancel_early":
        HexagonHooks.start.subscribe(
            HookSubscription(
                SUBSCRIPTION_NAME, sleep_15_seconds, HookSubscrptionType.background
            )
        )
        HexagonHooks.end.subscribe(
            HookSubscription(SUBSCRIPTION_NAME, lambda x: time.sleep(1))
        )
    elif test_name == "async_error_early":
        HexagonHooks.start.subscribe(
            HookSubscription(
                SUBSCRIPTION_NAME, sleep_15_seconds, HookSubscrptionType.background
            )
        )
        HexagonHooks.end.subscribe(
            HookSubscription(SUBSCRIPTION_NAME, lambda x: time.sleep(1))
        )
    else:
        raise Exception("Unknown test name")
