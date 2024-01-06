from typing import Any

import requests
import xmltodict

JSON_DATA = {"Content-Type": "application/json"}
JSON_RESPONSE = {"Accept": "application/json"}
XML_DATA = {"Content-Type": "application/xml"}
XML_RESPONSE = {"Accept": "application/xml"}


def get_header(data_style: str = "", response_style: str = "") -> dict:
    header = {}
    if "json" in data_style.lower():
        header.update(JSON_DATA)
    if "xml" in data_style.lower():
        header.update(XML_DATA)
    if "json" in response_style.lower():
        header.update(JSON_RESPONSE)
    if "xml" in response_style.lower():
        header.update(XML_RESPONSE)
    return header


def curl(
    method: str,
    url,
    data_style: str = "",
    response_style: str = "",
    data=None,
    params=None,
    json=None,
):
    method = method.upper()
    assert method in ["GET", "POST", "PUT", "DELETE", "HEAD", "PATCH"]
    headers = get_header(data_style, response_style)
    response = requests.request(
        method, url, headers=headers, data=data, params=params, json=json, timeout=1
    )
    content = ""
    if response.text:
        if "xml" in response_style.lower():
            content = xmltodict.parse(response.text)
            if content.get("projects"):
                content["projects"] = content["projects"]["project"]
        elif "json" in response_style.lower():
            content = response.json()
        else:
            content = response.content.decode()

    return response.status_code, content


def sort_json(item):
    if isinstance(item, dict):
        return sorted((key, sort_json(values)) for key, values in item.items())
    if isinstance(item, list):
        return sorted(sort_json(x) for x in item)
    if item:
        return item
    return ""
