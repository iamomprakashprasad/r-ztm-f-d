from rest_framework.pagination import PageNumberPagination


class TaskPagination(PageNumberPagination):
    """
    Pagination for the task list endpoint.

    Clients can control the page size via the `page_size` query parameter,
    up to a maximum of `max_page_size`.

    Examples:
        GET /api/tasks/?page=2
        GET /api/tasks/?page=1&page_size=5
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
