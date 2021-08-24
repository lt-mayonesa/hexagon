from hexagon.support.storage import HexagonStorageKeys, load_user_data, store_user_data
import datetime

LAST_UPDATE_DATE_FORMAT = "%Y%m%d"


def already_checked_for_updates(app: str = None) -> bool:
    last_checked = load_user_data(HexagonStorageKeys.last_update_check.value, app)

    result = False

    if last_checked:
        last_checked_date = datetime.datetime.strptime(
            last_checked, LAST_UPDATE_DATE_FORMAT
        ).date()

        # TODO: Move to hexagon configuration
        # See https://github.com/redbeestudios/hexagon/pull/35#discussion_r670870804 for more information
        result = last_checked_date >= datetime.date.today()

    if not result:
        store_user_data(
            HexagonStorageKeys.last_update_check.value,
            datetime.date.today().strftime(LAST_UPDATE_DATE_FORMAT),
            app=app,
        )

    return result
