from django.db import models
from PyPDF2 import PdfFileReader
from wand.image import Image
import os
from urllib.request import pathname2url
from django.conf import settings
import shutil
# from natsort import natsorted, ns
# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.utils.text import slugify


def content_file_name(instance, filename):
    return os.path.join(settings.MEDIA_ROOT,
        instance.slug, filename)

# Class that controls the bookshelf
class ZineApp(models.Model):
    scrollpage = models.ForeignKey('homepage.ScrollPage', null=True, blank=True)

    def sorted_zine_set(self):
        return Zine.objects.order_by('pk')


# Class to create zine issues
class Zine(models.Model):
    # USER-CONFIGURED FIELDS
    title = models.CharField(
        max_length=200,
        help_text='must be unique or there will be an error saving the files')
    description = models.CharField(max_length=200)
    # pdf_file = FileBrowseField("Image", max_length=200, directory="images/", extensions=[".jpg"], blank=True, null=True)
    pdf_file = models.FileField(
        default="",
        upload_to=content_file_name
    )
    # AUTO-CONFIGURED FIELDS
    slug = models.CharField(max_length=200, editable=False)
    page_count = models.IntegerField(editable=False,null=True)

    # PUBLIC MEMBER FUNCTIONS
    # display name
    def __str__(self):
        return self.title

    # return absolute path of pdf file
    def _path(self):
        path = os.path.dirname(self.pdf_file.name)
        return path

    # return relative url of Zine media (used in template)
    def rel_url(self):
        rel_path = os.path.relpath(self._path(), os.path.dirname(settings.MEDIA_ROOT))
        return pathname2url(rel_path)

    # used by template to get the number of pages in the zine
    # def page_count(self):
    #     pages_list = self._get_pages()
    #     return len(pages_list)

    # used by template to return an array of urls for each page
    # def get_page_urls(self):
    #     pages_list = self._get_pages()
    #     pages_list = natsorted(pages_list, alg=ns.IGNORECASE)
    #     pages_urls = []
    #     for filename in pages_list:
    #         pages_urls.append(
    #             os.path.join(settings.MEDIA_URL, self.slug, '/pages/', filename)
    #         )
    #     return pages_urls

    # actions to perform on save
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)  # generate a slug for the save directory
        pdf_changed = True
        if self.pk is not None:
            # changing an existing entry
            old_entry = Zine.objects.get(pk=self.pk)
            if old_entry.title != self.title:
                pdf_changed = False
                # if the title is changed, rename directory
                path = os.path.dirname(old_entry.path())
                new_dir = os.path.normpath(os.path.join(path, self.slug))
                os.rename(old_entry.path(), new_dir)
                # rename filename to reflect new directory
                filename = os.path.basename(self.pdf_file.name)
                self.pdf_file.name = os.path.normpath(os.path.join(new_dir, filename))
            elif old_entry.pdf_file != self.pdf_file:
                # if a new pdf, delete old files
                old_entry.destroy()
        # save the model
        models.Model.save(self, *args, **kwargs)
        if pdf_changed:
            # now that new pdf is saved, convert to images
            self.convert_to_jpg()

    # method to delete associated files when instance deleted
    def destroy(self):
        # delete the image files
        # filename = os.path.splitext(self.pdf_file.name)[0]
        filepath = self.path()
        if(os.path.exists(filepath)):
            shutil.rmtree(filepath)
        # Pass false so FileField doesn't save the model.
        # self.pdf_file.delete(False)

    # METHODS FOR PDF TO IMAGE CONVERSION
    def convert_to_png(self, width=0, height=0):
        self.__convert_to_img__(width, height, 'png')

    def convert_to_jpg(self, width=0, height=0):
        self.__convert_to_img__(width, height, 'jpg')

    def __convert_to_img__(self, width, height, format='jpg'):
        size = ''
        if width and height:
            size = '_' + str(width) + 'x' + str(height) + 'px'

        filepath = self.pdf_file.name
        thumb_dir = os.path.normpath(os.path.join(self.path(), 'pics', ''))
        img_dir = os.path.normpath(os.path.join(self.path(), 'pages', ''))
        os.makedirs(img_dir)  # mkdirs required for making folders recursively
        os.makedirs(thumb_dir)

        input_file = PdfFileReader(open(filepath, 'rb'))

        for i in range(input_file.getNumPages()):
            with Image(filename=filepath + '[' + str(i) + ']') as img:
                if len(size) > 0:
                    img.resize(width, height)
                img.format = format
                filename = img_dir + '/' + str(i+1)
                img.save(filename=filename + '.' + format)  # TO DO: remove explicit '/'
                std = Image(filename=filename + '.' + format)
                std.resize(500, round(std.height/std.width * 500))
                std.save(filename=filename + '-large.' + format)
                if (i == 0):
                    thumb = Image(filename=filename + '.' + format)
                    thumb.resize(92, 115)
                    thumb.save(filename=thumb_dir + '/thumb.' + format)

        #record the number of pages
        self.page_count = input_file.getNumPages()
        models.Model.save(self)  # don't trigger save function again.

    # PRIVATE MEMBER FUNCTIONS
    # def _get_pages(self):
    #     pages_dir = os.path.join(self.path(), 'pages')
    #     pages_list = os.listdir(pages_dir)
    #     return pages_list

    # TO DO: add method to create thumbnail sprites
    # TO DO: add method to create thumbnail for bookshelf


@receiver(post_delete, sender=Zine)
def mymodel_delete(sender, instance, **kwargs):
    instance.destroy()
