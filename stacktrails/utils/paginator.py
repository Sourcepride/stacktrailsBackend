from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    # page_size_query_param = "size"

    def get_paginated_response(self, data, **kwargs):
        return Response(
            {
                "total_pages": self.page.paginator.num_pages,
                "items_count": self.page.paginator.count,
                "current_page": int(self.request.query_params.get("page", 1)),
                "next": self.page.next_page_number() if self.page.has_next() else None,
                "previous": (
                    self.page.previous_page_number()
                    if self.page.has_previous()
                    else None
                ),
                "next_url": self.get_next_link(),
                "previous_url": self.get_previous_link(),
                "results": data,
                **kwargs,
            }
        )
