import django_filters
from django_filters import FilterSet

from django import forms
from .models import Post

class PostFilter(FilterSet):
    created_at__gt = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Дата публикации после',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control',},
            format='%Y-%m-%dT%H:%M')
        )

    class Meta:
        model = Post
        fields = {
           'title': ['icontains'],
           'content':['icontains'],
        }