from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User,
)

# Добавляем поле с биографией
# к стандартному набору полей (fieldsets) пользователя в админке.
UserAdmin.fieldsets += (
    # Добавляем кортеж, где первый элемент —
    # это название раздела в админке,
    # а второй элемент — словарь,
    # где под ключом fields можно указать нужные поля.
    ('Extra Fields', {'fields': ('bio',)}),
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


admin.site.register(User, UserAdmin)
admin.site.register(Category, SlugNameAdmin)
admin.site.register(Genre, SlugNameAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review)
admin.site.register(Comment)
