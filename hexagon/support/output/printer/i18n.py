import builtins
import gettext
import os
import site
import sys
from typing import List

LOCALEDIR = os.environ.get("HEXAGON_LOCALES_DIR", None)

# site.USER_BASE is usually ~/.local (this is used when pip WAS NOT installed globally)
LOCAL_LOCALEDIR = os.path.join(site.USER_BASE, "locales")

# sys.prefix is usually /usr/local (this is used when pip WAS installed globally)
SYSTEM_LOCALEDIR = os.path.join(sys.prefix, "locales")

DEFAULT_LANGUAGE = "en"


def install():
    """
    gettext translations are a PAIN, seriously considering of dropping it.

    Any-who, this function will install the translations for the current process.
    It will try to load the translations from the known paths, and fallback to the default ones.
    If nothing works we'll create a GNUTranslations object ourselves.
    """
    if getattr(builtins, "_", None):
        return
    el = (
        _load_first_match_from_dirs(
            [LOCALEDIR] if LOCALEDIR else [LOCAL_LOCALEDIR, SYSTEM_LOCALEDIR]
        )
        or _load_gettext_default()
        or _load_from_local()
    )

    el.install()


def _load_first_match_from_dirs(paths: List[str]):
    for path in paths:
        el = __try_translation(localedir=path)
        if el:
            return el
    for path in paths:
        el = __try_translation(localedir=path, languages=[DEFAULT_LANGUAGE])
        if el:
            return el
    return None


def _load_gettext_default():
    """
    gettext default path is os.path.join(sys.base_prefix, 'share', 'locale')
    for some reason when installing with pip locales are not copied there.
    """
    return __try_translation() or __try_translation(languages=[DEFAULT_LANGUAGE])


def _load_from_local():
    """
    If everything fails, we'll create a GNUTranslations object ourselves.
    File en.py is actually an .mo and is copied by .github/scripts/i18n/build.sh .
    We use .py, so it's packaged with everything else without any modifications to setup.

    Cheap tricks, I know.
    """
    return gettext.GNUTranslations(
        open(os.path.join(os.path.dirname(__file__), "en.py"), mode="rb")
    )


def __try_translation(**kwargs):
    try:
        return gettext.translation("hexagon", **kwargs)
    except FileNotFoundError:
        return None
