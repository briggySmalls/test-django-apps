from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    # CONSTANTS
    # The following HTML is substituted in place of its corresponding tag
    # This enables easy inclusion of HTML content in an article
    WIDGETS = {
        '{facebook-page}': '<div class="fb-like-box" data-href="https://www.facebook.com/SkinDeepMagazine" data-colorscheme="light" data-show-faces="true" data-header="false" data-stream="true" data-show-border="true"></div>',
        '{facebook-group}': '<script type="text/javascript"> rssfeed_url = new Array(); rssfeed_url[0]="https://facebook-rss.herokuapp.com/rss/501953199923737";  rssfeed_frame_width="300"; rssfeed_frame_height="250"; rssfeed_scroll="on"; rssfeed_scroll_step="6"; rssfeed_scroll_bar="off"; rssfeed_target="_blank"; rssfeed_font_size="12"; rssfeed_font_face=""; rssfeed_border="on"; rssfeed_css_url=""; rssfeed_title="on"; rssfeed_title_name=""; rssfeed_title_bgcolor="#55a0ff"; rssfeed_title_color="#fff"; rssfeed_title_bgimage="http://"; rssfeed_footer="off"; rssfeed_footer_name="rss feed"; rssfeed_footer_bgcolor="#fff"; rssfeed_footer_color="#333"; rssfeed_footer_bgimage="http://"; rssfeed_item_title_length="50"; rssfeed_item_title_color="#000"; rssfeed_item_bgcolor="#fff"; rssfeed_item_bgimage="http://"; rssfeed_item_border_bottom="on"; rssfeed_item_source_icon="off"; rssfeed_item_date="off"; rssfeed_item_description="on"; rssfeed_item_description_length="120"; rssfeed_item_description_color="#666"; rssfeed_item_description_link_color="#333"; rssfeed_item_description_tag="off"; rssfeed_no_items="0"; rssfeed_cache = "91b637f873c2307ed5387cba32ed7d1c"; </script> <script type="text/javascript" src="http://feed.surfing-waves.com/js/rss-feed.js"></script> <!-- The link below helps keep this service FREE, and helps other people find the SW widget. Please be cool and keep it! Thanks. --> <div style="text-align:right; width:300px;"><a href="http://www.surfing-waves.com/feed.htm" target="_blank" style="color:#ccc;font-size:10px">widget @</a> <a href="http://www.surfing-waves.com" target="_blank" style="color:#ccc;font-size:10px">surfing-waves.com</a></div> <!-- end sw-rss-feed code -->',
        '{twitter}': '<a class="twitter-timeline" href="https://twitter.com/skindeepzine" data-widget-id="571117174111363072">Tweets by @Skindeepzine</a><script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?"http":"https";if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>',
    }

    # CONTENT
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    content = RichTextField()
    full_content = models.CharField(max_length=500, editable=False)

    # METADATA
    category = models.ForeignKey(Category, blank=True, null=True)

    # PUBLISHING
    start_date = models.DateTimeField(
        'Date to start publishing from',
        blank=True, null=True)  # allow this field to be optional
    end_date = models.DateTimeField(
        'Date to end publishing on',
        blank=True, null=True)  # allow this field to be optional

    # METHODS
    def __str__(self):
        return self.title

    # used to determine articles to be published
    def in_date(self):
        now = timezone.now()
        in_date_range = (
            self.start_date < now if
            self.start_date is not None else True) and (
            now < self.end_date if
            self.end_date is not None else True)
        return in_date_range
    in_date.boolean = True
    in_date.short_description = 'In date?'

    # on save populate full_content with widget html (see below)
    def save(self, *args, **kwargs):
        self.full_content = self.content
        for tag, html in Article.WIDGETS.items():
            self.full_content = self.full_content.replace(tag, html)
        # save the model
        models.Model.save(self, *args, **kwargs)
