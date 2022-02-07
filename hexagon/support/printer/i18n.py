import os
import site
import sys

import gettext

LOCALEDIR = os.environ.get("HEXAGON_LOCALES_DIR", None)

# site.USER_BASE is usually ~/.local (this is used when pip WAS NOT installed globally)
LOCAL_LOCALEDIR = os.path.join(site.USER_BASE, "locales")

# sys.prefix is usually /usr/local (this is used when pip WAS installed globally)
SYSTEM_LOCALEDIR = os.path.join(sys.prefix, "locales")

DEFAULT_LANGUAGE = "en"


def install():
    el = lookup_localedir() if LOCALEDIR else lookup_install_localedirs()

    el.install()

    return el.gettext


def lookup_install_localedirs():
    return (
        __try_translation(localedir=LOCAL_LOCALEDIR)
        or __try_translation(localedir=LOCAL_LOCALEDIR, languages=[DEFAULT_LANGUAGE])
        or __try_translation(localedir=SYSTEM_LOCALEDIR)
        or __try_translation(localedir=SYSTEM_LOCALEDIR, languages=[DEFAULT_LANGUAGE])
        or __try_translation(fallback=True)
    )


def lookup_localedir():
    return __try_translation(localedir=LOCALEDIR) or __try_translation(
        localedir=LOCALEDIR, languages=[DEFAULT_LANGUAGE]
    )


def __try_translation(**kwargs):
    try:
        return gettext.translation("hexagon", **kwargs)
    except FileNotFoundError:
        return None
