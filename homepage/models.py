from django.db import models
from colorfield.fields import ColorField


# Create your models here.
class HomePage(models.Model):
    # this is the main, configurable homepage model
    title = models.CharField(max_length=250)

    # function used to identify homepage
    def __str__(self):
        return self.title

    # function used to ensure scrollpages ordered
    @property
    def sorted_scrollpage_set(self):
        return self.scrollpage_set.order_by('pk')


class ScrollPage(models.Model):
    # a homepage contains multiple ScrollPages
    homepage = models.ForeignKey(HomePage)  # parent homepage
    name = models.CharField(max_length=200)  # scrollpage has a name
    bg_colour = ColorField(default='ffffff')  # scrollpage has a background colour

    def __str__(self):
        return self.name

    def sorted_zine_set(self):
        return self.zineapp_set.order_by('title')
