import uuid

import pkg_resources
import requests

from hexagon.support.storage import load_user_data, store_user_data


def event(name: str, **kwargs):
    version = pkg_resources.require("hexagon")[0].version

    cid = load_user_data("user_id")
    if not cid:
        cid = str(uuid.uuid4())
        store_user_data("user_id", cid)

    mid = "G-Y28H5KHQEZ"

    params = {
        "client_id": cid,
        "events": [{"name": name, "params": {**kwargs}}],
        "user_properties": {"hexagon_version": {"value": version}},
    }
    # TODO: externalize mid and api_secret
    requests.post(
        f"https://www.google-analytics.com/mp/collect?measurement_id={mid}&api_secret=lalUv8tgR4OfjXl88FjrFw",
        json=params,
    )
