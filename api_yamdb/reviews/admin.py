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

# class GenreInline(admin.StackedInline):
#     model = Genre
#     extra = 0


class TitleAdmin(admin.ModelAdmin):
    # inlines = (GenreInline, )
    list_display = [
        'name',
        'category',
        'year',
        'description',
    ]
    list_editable = ('category', )
    list_filter = ('category', 'name')
    filter_horizontal = ('genre',)


admin.site.register(User, UserAdmin)
admin.site.register(Category, SlugNameAdmin)
admin.site.register(Genre, SlugNameAdmin)
admin.site.register(Title, TitleAdmin)
# TODO:  вывести список жанров через запятую в листе произведений 
admin.site.register(Review)
admin.site.register(Comment)
