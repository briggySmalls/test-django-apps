from django.contrib import admin
from articles.models import Category, Article


class ArticleAdmin(admin.ModelAdmin):
    # arrange fields into fieldsets (collapse the optional publishing fields)
    fieldsets = [
        ('Content', {
            'fields': ['title', 'subtitle', 'content', 'category']}),
        ('Publishing', {
            'fields': ['start_date', 'end_date'],
            'classes': ('grp-collapse grp-closed',)})
    ]
    # properties to display in list of Article objects
    list_display = ('title', 'subtitle', 'in_date')
    # allow admins to filted based on in_date
    ['in_date', 'category']
    # allow admins to search
    ['title']

# registering Category is necessary for 'add another' to be available in
# ArticleAdmin
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
