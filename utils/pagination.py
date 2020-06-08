from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.LimitOffsetPagination):

    def get_paginated_response(self, data):
        next_page = self.offset + self.limit
        has_more = next_page < self.count

        return Response({
            'limit': self.limit,
            'nextPage': next_page if has_more else 0,
            'hasMorePages': has_more,
            'results': data
        })
