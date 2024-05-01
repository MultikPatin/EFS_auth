from django.contrib.postgres.aggregates.general import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from ...models import FilmWork, PersonFilmWork


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = self.model.objects.values(
            "id", "title", "description", "creation_date", "rating", "type"
        ).annotate(
            genres=ArrayAgg("genres__name", distinct=True),
            actors=ArrayAgg(
                "persons__full_name",
                filter=Q(
                    personfilmwork__role=PersonFilmWork.RoleType.ACTOR.value
                ),
                distinct=True,
            ),
            directors=ArrayAgg(
                "persons__full_name",
                filter=Q(
                    personfilmwork__role=PersonFilmWork.RoleType.DIRECTOR.value
                ),
                distinct=True,
            ),
            writers=ArrayAgg(
                "persons__full_name",
                filter=Q(
                    personfilmwork__role=PersonFilmWork.RoleType.WRITER.value
                ),
                distinct=True,
            ),
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )
        previous_page_number = None
        next_page_number = None
        if is_paginated:
            if page.has_previous():
                previous_page_number = page.previous_page_number()
            if page.has_next():
                next_page_number = page.next_page_number()
        else:
            queryset = self.get_queryset()

        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": previous_page_number,
            "next": next_page_number,
            "results": list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return self.get_object()
