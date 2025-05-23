from hexagon.support.hooks import HexagonHooks
from hexagon.support.hooks.hook import HookSubscription
from hexagon.support.output.printer import log

SUBSCRIPTION_NAME = "test-plugin"


def main():
    HexagonHooks.end.subscribe(
        HookSubscription(
            SUBSCRIPTION_NAME, lambda _: log.result("plugin inside action")
        )
    )
