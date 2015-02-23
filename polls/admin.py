from django.contrib import admin
from polls.models import Choice, Question


# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # define how fields should be displayed (e.g collapse pub_date)
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']})
    ]
    # instruct Django that Choices are defined when defining a Question
    # inlines = [ChoiceInline]
    # instruct Django how to display Question objects
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # allow admins to filter based upon pub_date
    list_filter = ['pub_date']
    # allow admins to search
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
