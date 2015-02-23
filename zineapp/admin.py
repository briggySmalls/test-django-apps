from django.contrib import admin
from zineapp.models import ZineApp, Zine
# from filebrowser.widgets import ClearableFileInput
# from django.db import models


# Register your models here.
class ZineAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    # fields = ('title', 'description', 'pdf_file')
    # formfield_overrides = {
    # # models.FileField: {'widget': ClearableFileInput},
    # }

    # function called when model form is saved
    # TO DO: move this to Zine model
    # def save_model(self, request, obj, form, change):
        # NOTE: obj.pdf_file is a django FILE object
        # NOTE: request.FILES is a MultiValueDict object
        # NOTE: change indicates new object created/existing obj changed

        # if we have changed an exisitng entry
        # if(change):
        #     # get the 'current' file
        #     old_file = Zine.objects.get(pk=obj.pk)
        #     # d

        # # save our 'new' model entry
        # obj.save()

        # # check if a new file was submitted
        # if 'pdf_file' in request.FILES:
        #     # if we have changed an exisitng entry
        #     if(change):
        #         # delete old files
        #         print('I will now delete old files')
        #         old_file.destroy()

        #     # convert pdf to images
        #     obj.convert_to_jpg()
        # else:
        #     # no cleanup necessary!
        #     print('No old files to delete')

    # function called when model entry is deleted
    # def delete_model(request, obj):
        # delete old files
        # obj.delete()  # delete model entry


admin.site.register(Zine, ZineAdmin)
admin.site.register(ZineApp)
