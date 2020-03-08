from typing import Dict
from urllib.parse import parse_qs

from flask import request


def get_unique_query_parameters() -> Dict[str, str]:
    query_parameters = parse_qs(request.query_string)
    if any([len(value) != 1 for value in query_parameters.values()]):
        raise TypeError('query parameter keys must be unique (they should only appear once in a query)')

    query_parameters = {key.decode(): value[0].decode() for key, value in query_parameters.items()}
    return query_parameters
