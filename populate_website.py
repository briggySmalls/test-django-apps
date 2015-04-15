import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import sys
import django
django.setup()

from homepage.models import HomePage, ScrollPage
from container.models import Container, Tab
from zineapp.models import ZineApp, Zine
from articles.models import Article, Category

default_colour = 'ffffff'

def populate(args):
    no_args = args[1] is None
    if no_args or 'homepage' in args:
        # make the pages
        homepage = add_HomePage('Skin Deep Home')
        welcome_scrollpage = add_ScrollPage(homepage, 'welcome')
        zine_scrollpage = add_ScrollPage(homepage, 'zine')
        social_scrollpage = add_ScrollPage(homepage, 'social')

    if no_args or 'zineapp' in args:
        # make the zineapp
        zineapp = add_ZineApp(zine_scrollpage)

    if no_args or 'articles' in args:
        # make the articles
        home_article = add_Article('Home Article', 'st', 'The home')
        about_article = add_Article('About Article', 'st', 'The aobut')
        news_category = add_Category('News')
        news1_article = add_Article('News Item 1', 'st', 'First news', news_category)
        news2_article = add_Article('News Item 2', 'st', 'Second news', news_category)
        social_category = add_Category('Social')
        fbgroup_article = add_Article('FB Group', 'st', 'The facebook group feed', social_category)
        fbpage_article = add_Article('FB Page', 'st', 'The facebook page feed', social_category)
        twitter_article = add_Article('Twitter', 'st', 'The twitter feed', social_category)

    if no_args or 'container' in args:
        # make the containers
        if no_args:
            welcome_container = add_Container('welcome_widget', welcome_scrollpage)
        else:
            welcome_container = add_Container('welcome_widget')
        home_tab = add_Tab(welcome_container, 'Home', 1, home_article)
        about_tab = add_Tab(welcome_container, 'About', 2, about_article)
        news_tab = add_Tab(welcome_container, 'News', 3, news_category)
        if no_args:
            social_container = add_Container('social_widget', social_scrollpage)
        else:
            social_container = add_Container('social_widget')
        social_tab = add_Tab(social_container, 'Social', 1, 3, social_category)

# homepage app models
def add_HomePage(title):
    return HomePage.objects.get_or_create(title=title)[0]

def add_ScrollPage(homepage, name, colour=default_colour):
    return ScrollPage.objects.get_or_create(homepage=homepage,
                                            name=name,
                                            bg_colour=colour)[0]

# container app models
def add_Container(title, **kwargs):
    return Container.objects.get_or_create(title=title, **kwargs)[0]

def add_Tab(container, keyword, order, foreign_key, column_count=1):
    if isinstance(foreign_key, Article):
        return Tab.objects.get_or_create(container=container,
                                         keyword=keyword,
                                         order=order,
                                         column_count=column_count,
                                         article=foreign_key)[0]
    elif isinstance(foreign_key, Category):
        return Tab.objects.get_or_create(container=container,
                                         keyword=keyword,
                                         order=order,
                                         column_count=column_count,
                                         category=foreign_key)[0]

# zineapp app models
def add_ZineApp(scrollpage):
    return ZineApp.objects.get_or_create(scrollpage=scrollpage)[0]

# def add_Zine(title, description, pdf_file, slug, page_count)

# articles app models
def add_Article(title, subtitle, content, category=None):
    return Article.objects.get_or_create(title=title,
                                         subtitle=subtitle,
                                         content=content,
                                         category=category)[0]

def add_Category(name):
    return Category.objects.get_or_create(name=name)[0]

# Start execution here!
if __name__ == '__main__':
    print("Starting Skin Deep Website population script...")
    populate(sys.argv)