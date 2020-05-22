from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'nextPage': self.page.next_page_number() if self.page.has_next() else self.page.number,
            'hasMorePages': self.page.has_next(),
            'count': self.page.paginator.count,
            'results': data
        })
