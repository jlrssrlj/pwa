from .models import Categorias, Blog
from django.contrib import admin

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display =('title', 'category','status', 'is_featured')
    search_fields = ('id','title','category__category_name','status')
    list_editable = ('is_featured',)

admin.site.register(Categorias)
admin.site.register(Blog, BlogAdmin)