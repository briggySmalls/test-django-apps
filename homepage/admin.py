from django.contrib import admin
from homepage.models import HomePage, ScrollPage


# Register your models here.
class ScrollPageInline(admin.TabularInline):
    model = ScrollPage
    extra = 0


class HomePageAdmin(admin.ModelAdmin):
    inlines = [ScrollPageInline]


admin.site.register(HomePage, HomePageAdmin)
#admin.site.register(ScrollPage)
