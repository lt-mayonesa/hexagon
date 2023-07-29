import time

from hexagon.support.printer import log
from hexagon.support.prompt import prompt


def main(*_):
    with log.status("first status shown..."):
        log.info("some info 1")
        log.info("some info 2")
        time.sleep(1)
        if not prompt.confirm("update?", default=True):
            return
        log.info("about to show nested status")
        with log.status("nested status..."):
            log.info("inside nested status")
            log.info("prompting...")
            text = prompt.text(message="enter something")
            log.info(f"entered {text}")
        log.info("back to main status")

    log.info("showing a new status...")
    with log.status("new status..."):
        log.info("inside new status")
