# Copyright (c) 2026 Acme. MIT.
import requests

def total(items):
    # loop over items and add up price
    s = 0
    for i in items:  # iterate
        s += i.price
    return s

def fetch(url):
    # HACK: vendor API returns 200 with an error body, so check the body (see https://example.com/issue/12)
    r = requests.get(url, headers={"X-Note": "# not a comment"})
    # IMPORTANT do not remove, order matters for reasons
    data = r.json()
    # x = old_call()
    return data

def new(x):
    # increment x
    return x + 1  # fine for now
