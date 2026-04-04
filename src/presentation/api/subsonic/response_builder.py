from fastapi import Response
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Any
import xml.etree.ElementTree as ET

from application.config.constants import REST_API_VERSION, ERROR_MESSAGES


def build_response(data: dict, response_format: str = "xml") -> Response:
    status = "ok"

    if response_format == "json":
        return _build_json_response(data, status)
    else:
        return _build_xml_response(data, status)


def build_error_response(error_code: int, response_format: str = "xml") -> Response:
    data = {
        "error": {
            "@code": error_code,
            "@message": ERROR_MESSAGES.get(error_code)
        }
    }
    status = "failed"

    if response_format == "json":
        return _build_json_response(data, status)
    else:
        return _build_xml_response(data, status)


def _build_json_response(data: dict, status: str) -> JSONResponse:
    new_data = _build_json_response_data_from_dict(data)

    if not isinstance(new_data, dict):
        new_data = {}

    return JSONResponse(
        {
            "subsonic-response": {
                "status": status,
                "version": REST_API_VERSION,
                **new_data
            }
        }
    )


def _build_xml_response(data: dict, status: str) -> HTMLResponse:
    root = ET.Element("subsonic-response", {
        "status": status,
        "version": REST_API_VERSION,
        "xmlns": "http://subsonic.org/restapi"
    })

    _build_xml_response_data_from_dict(
        parent=root,
        data=data
    )

    return HTMLResponse(ET.tostring(root, encoding="utf-8", xml_declaration=True))


def _build_json_response_data_from_dict(data) -> Any:
    if isinstance(data, dict):
        new_data = {}
        text_value = None

        for key, value in data.items():
            if key.startswith("@"):
                new_data[key[1:]] = _build_json_response_data_from_dict(value)
            elif key == "#text":
                text_value = value
            else:
                new_data[key] = _build_json_response_data_from_dict(value)

        if not new_data and text_value is not None:
            return text_value
        elif new_data and text_value is not None:
            raise Exception
        else:
            return new_data

    elif isinstance(data, list):
        return [_build_json_response_data_from_dict(item) for item in data]
    else:
        return data


def _build_xml_response_data_from_dict(parent: ET.Element, data) -> None:
    for key, value in data.items():
        if key.startswith("@"):
            parent.set(key[1:], str(value))
        elif key == ("#text"):
            parent.text = str(value)
        elif isinstance(value, dict):
            child = ET.SubElement(parent, key)
            _build_xml_response_data_from_dict(child, value)
        elif isinstance(value, list):
            for item in value:
                item_elem = ET.SubElement(parent, key)
                if isinstance(item, dict):
                    _build_xml_response_data_from_dict(item_elem, item)
                else:
                    item_elem.text = str(item)
        else:
            ET.SubElement(parent, key).text = str(value)
