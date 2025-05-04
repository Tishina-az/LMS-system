from rest_framework.pagination import PageNumberPagination


class CoursePaginator(PageNumberPagination):
    """Пагинатор с выводом 5 курсов на страницу"""

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20


class LessonPaginator(PageNumberPagination):
    """Пагинатор с выводом 10 уроков на страницу"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
