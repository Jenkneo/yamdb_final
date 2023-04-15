from django.contrib import admin

from .models import (
    MyUser, Category, Genre, Title, Review, Comment
)

admin.site.register(MyUser)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_id', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title_id', 'author')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description', 'genre', 'category')
    search_fields = ('name', 'year', 'genre', 'category')
