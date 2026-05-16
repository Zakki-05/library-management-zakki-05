from django.contrib import admin
from .models import Category, Author, Book

admin.site.register(Category)
admin.site.register(Author)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'total_quantity', 'available_quantity')
    search_fields = ('title', 'isbn', 'author__name')
    list_filter = ('category',)
