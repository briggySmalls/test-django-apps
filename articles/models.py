from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    # CONTENT
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    content = RichTextField()

    # METADATA
    category = models.ForeignKey(Category, blank=True, null=True)

    # PUBLISHING
    start_date = models.DateTimeField(
        'Date to start publishing from',
        blank=True, null=True)  # allow this field to be optional
    end_date = models.DateTimeField(
        'Date to end publishing on',
        blank=True, null=True)  # allow this field to be optional

    def in_date(self):
        now = timezone.now()
        in_date_range = (
            self.start_date < now if
            self.start_date is not None else True) and (
            now < self.end_date if
            self.end_date is not None else True)
        return in_date_range
    in_date.boolean = True
    in_date.short_description = 'Status based on start and end dates'

    def __str__(self):
        return self.title
