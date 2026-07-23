from rest_framework.pagination import PageNumberPagination


class AdPaginator(PageNumberPagination):
    page_size = 4
