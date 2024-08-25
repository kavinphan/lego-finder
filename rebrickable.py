import os
from requests import get
import json
from urllib.parse import quote_plus

REBRICKABLE_API_KEY = os.environ["REBRICKABLE_API_KEY"]

def get_sets(search):
    return json.loads(get(
        f"https://rebrickable.com/api/v3/lego/sets?search={quote_plus(search)}",
        headers={
            "Authorization": f"key {REBRICKABLE_API_KEY}"
        }
    ).text)['results']

def get_set(set_id):
    return json.loads(get(
        f"https://rebrickable.com/api/v3/lego/sets/{set_id}",
        headers={
            "Authorization": f"key {REBRICKABLE_API_KEY}"
        }
    ).text)
