import threading
from enum import Enum
from typing import Callable, Generic, List, TypeVar


class HookSubscrptionType(Enum):
    blocking = "blocking"
    background = "background"


T = TypeVar("T")


class HookSubscription(Generic[T]):
    def __init__(
        self,
        name: str,
        callback: Callable[[T], None],
        type: HookSubscrptionType = HookSubscrptionType.blocking,
    ):
        self.name = name
        self.type = type
        self.callback = callback

    callback: Callable[[T], None]


class Hook(Generic[T]):
    def __init__(self, name: str):
        self.name = name
        self.subscriptions = []

    subscriptions: List[HookSubscription[T]]

    def subscribe(self, subscription: HookSubscription[T]):
        self.subscriptions.append(subscription)

    def run(self, data: T = None):
        for subscription in self.subscriptions:
            if subscription.type == HookSubscrptionType.blocking:
                subscription.callback(data)
            elif subscription.type == HookSubscrptionType.background:
                thread = threading.Thread(
                    target=subscription.callback,
                    name=f"{self.name}:{subscription.name}",
                    kwargs={"data": data},
                )
                thread.daemon = True
                thread.start()
            else:
                # Unknown HookSubscriptionType {subscription_type}
                raise Exception(
                    _("error.support.hooks.hook.unknown_type").format(
                        subscription_type=subscription.type
                    )
                )
