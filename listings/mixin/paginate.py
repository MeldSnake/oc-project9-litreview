from django.core.paginator import Paginator
from typing import Any, Sequence, TypeVar, Iterable, Generic
from django.urls import reverse

T = TypeVar('T')


class PaginateMixin(Generic[T]):
    page_url: str | None = None
    page_arg: str | int = "page"
    limit: int = 10

    def get_paginated_objects(self) -> Iterable[T]:
        return []

    def get_pagination_args(self, page: int) -> Sequence[Any]:
        if isinstance(self.page_arg, int):
            return (page, )
        return tuple()

    def get_pagination_kwargs(self, page: int) -> dict[str, Any]:
        if isinstance(self.page_arg, str):
            return {self.page_arg: page}
        return {}

    def get_pagination_url(self, page: int) -> str | None:
        if self.page_url is None:
            raise ValueError("page_url was not defined for the current view")
        return reverse(self.page_url,
                       args=self.get_pagination_args(page),
                       kwargs=self.get_pagination_kwargs(page))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagination = Paginator(self.get_paginated_objects(), self.limit)
        page = pagination.get_page(self.kwargs["page"] if "page" in self.kwargs else 1)
        context["page"] = page
        if page.has_previous():
            context["page_first_url"] = self.get_pagination_url(1)
            context["page_prev_url"] = self.get_pagination_url(page.number - 1)
        else:
            context["page_first_url"] = None
            context["page_prev_url"] = None
        if page.has_next():
            context["page_next_url"] = self.get_pagination_url(page.number + 1)
            context["page_last_url"] = self.get_pagination_url(pagination.num_pages)
        else:
            context["page_next_url"] = None
            context["page_last_url"] = None
        context["page_count"] = pagination.num_pages
        return context
