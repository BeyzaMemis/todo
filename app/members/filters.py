import django_filters
from django_filters import CharFilter, DateFilter
from core.models import *


class ProjectFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    description = CharFilter(field_name='description', lookup_expr='icontains')
    start_date = CharFilter(field_name='start_date', lookup_expr='gte')
    deadline = CharFilter(field_name='deadline', lookup_expr='lte')

    class Meta:
        model = Projects
        fields = '__all__'
