from django.contrib import admin
from .models import Tag, Count


class TagsRatingFilter(admin.SimpleListFilter):
    title = 'Rating'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return (
            ('asc', 'Ascending'),
            ('desc', 'Descending'),
        )

    # We can't use property 'rating' for ordering queryset,
    # that why we need use annotate with calculating rating another one time
    def queryset(self, request, queryset):
        if self.value() == 'asc':
            return queryset.annotate(tag_rating=Count('article')).order_by('tag_rating')
        if self.value() == 'desc':
            return queryset.annotate(tag_rating=Count('article')).order_by('-tag_rating')
        

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'rating')
    fields = ('title', 'slug', 'rating')
    list_filter = (TagsRatingFilter, )
    search_fields = ('title', 'slug')
