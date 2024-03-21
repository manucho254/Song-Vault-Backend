from rest_framework.pagination import PageNumberPagination

from django.http import HttpRequest
from django.db.models import QuerySet


class CustomPagination(PageNumberPagination):
    """ Extend PageNumberPagination class

    Args:
        PageNumberPagination (_type_): Pagination Class
    """
    default_page = 1
    page_size = 20

    def get_paginated_response(
        self, query_set: QuerySet, serializer_obj, request: HttpRequest
    ) -> dict:
        try:
            page_data = self.paginate_queryset(query_set, request)
        except Exception:
            return {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "total": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "page": int(request.GET.get("page", self.default_page)),
                "page_size": int(request.GET.get("page_size", self.page_size)),
                "url": request.build_absolute_uri(),
                "results": [],
            }

        serialized_page = serializer_obj(
            page_data, many=True, context={"request": request}
        )

        return {
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "total": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "page": int(request.GET.get("page", self.default_page)),
            "page_size": int(request.GET.get("page_size", self.page_size)),
            "url": request.build_absolute_uri(),
            "results": serialized_page.data,
        }
