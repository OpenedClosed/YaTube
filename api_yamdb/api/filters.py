from django_filters import CharFilter, FilterSet

from reviews.models import Title


class TitleFilterSet(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']
        ordering = ['id']
