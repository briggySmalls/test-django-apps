from django.contrib import admin
from container.models import Container, Tab


# Register your models here.
class TabInline(admin.StackedInline):
    model = Tab
    extra = 0


class ContainerAdmin(admin.ModelAdmin):
    inlines = [TabInline]
    # ORDER ACCORDING TO SCROLLPAGE PK

admin.site.register(Container, ContainerAdmin)
