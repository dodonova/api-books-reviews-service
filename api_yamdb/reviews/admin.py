from django.contrib import admin

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)


class SlugNameAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


class GenreInline(admin.TabularInline):
    model = Title.genre.through


class TitleAdmin(admin.ModelAdmin):

    def genres_list(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])

    genres_list.short_description = "Жанры"
    list_display = [
        'name',
        'year',
        'category',
        'genres_list',
        'description',
    ]
    list_editable = ('category', )
    list_filter = ('category', 'genre')
    filter_horizontal = ('genre',)
    inlines = [GenreInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'text',
        'pub_date',
    ]


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'pub_date',
        'author'
    )


admin.site.register(Category, SlugNameAdmin)
admin.site.register(Genre, SlugNameAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
