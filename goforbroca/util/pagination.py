"""Simple helper to paginate query
"""
from typing import Optional

from flask import url_for, request

default_page_number = 1
default_page_size = 50


def paginate(name,
             query,
             schema,
             page_number: Optional[int],
             page_size: Optional[int]):

    if page_number is None:
        page_number = default_page_number
    if page_size is None:
        page_size = default_page_size

    page_obj = query.paginate(page=page_number, per_page=page_size)
    after = url_for(
        request.endpoint,
        page=page_obj.next_num if page_obj.has_next else page_obj.page,
        per_page=page_size,
        **request.view_args,
    )
    before = url_for(
        request.endpoint,
        page=page_obj.prev_num if page_obj.has_prev else page_obj.page,
        per_page=page_size,
        **request.view_args,
    )

    results = {
        'total': page_obj.total,
        'pages': page_obj.pages,
        'next': after,
        'prev': before,
        name: schema.dump(page_obj.items).data,
    }
    return results
