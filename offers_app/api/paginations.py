from rest_framework.pagination import PageNumberPagination


class DynamicPageSizePagination(PageNumberPagination):
    """
    Pagination class that allows clients
    to set the page size via a query parameter.
    """
    page_size = 6  # should orientate on frontend needs
    page_size_query_param = 'page_size'
