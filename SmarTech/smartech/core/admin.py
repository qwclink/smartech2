from django.contrib import admin
from .models import Product, Category, Article, Banner, Guestbook

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ()
    fields = ('name', 'category', 'description', 'price', 'available', 'image')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'content')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    readonly_fields = ()
    fields = ('title', 'image')

@admin.register(Guestbook)
class GuestbookAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'message')
    ordering = ('-created_at',)
    search_fields = ('name', 'message')
