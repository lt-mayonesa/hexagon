from enum import Enum
from typing import Callable, Generic, List, TypeVar
import threading


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
                thread.start()
            else:
                raise Exception(f"Unknown HookSubscriptionType {subscription.type}")
