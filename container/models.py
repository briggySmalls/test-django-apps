from django.db import models
from django.utils.text import slugify
from articles.models import Article, Category


# Create your models here.
class Container(models.Model):
    # a container is registered to a scrollpage
    # this could later be registered to a scrollpage POSITION
    # TO DO: make OnetoOne so that position gets taken?
    scrollpage = models.ForeignKey('homepage.ScrollPage', blank=True, null=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def sorted_tab_set(self):
        return self.tab_set.order_by('order')  # TO DO: sort by something else

    def slugify_title(self):
        return slugify(self.title)


class Tab(models.Model):
    # a Container is made up of Tabs
    container = models.ForeignKey(Container)
    keyword = models.CharField(max_length=15)  # word that appears on the Tab
    order = models.PositiveIntegerField(default=1)
    column_count = models.PositiveIntegerField(default=1)

    # link tab to article or category
    article = models.ForeignKey(Article, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    # theme = enumerate # consider adding a theme/style for a container from some options

    def __str__(self):
        return self.keyword

    def sorted_article_set(self):
        return self.category.article_set.order_by('pk')  # TO DO: sort by something else

    def slugify_keyword(self):
        return slugify(self.keyword)

    def get_pk(self):
        return self.pk

    # TO DO: on save, check if order already used, if so iterate through all objects and increment clashes