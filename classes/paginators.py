from rest_framework.pagination import PageNumberPagination


class ClassesPaginator(PageNumberPagination):
    page_size = 10

