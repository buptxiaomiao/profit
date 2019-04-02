# coding: utf-8

import json


def json_dumps(d):
    try:
        return json.dumps(d)
    except Exception as e:
        return ''


def json_loads(s):
    try:
        return json.loads(s)
    except Exception as e:
        return {}
