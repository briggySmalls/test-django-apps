import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from homepage.models import HomePage, ScrollPage
from container.models import Container, Tab
from zineapp.models import ZineApp, Zine
from articles.models import Article, Category

def populate():

    # make the pages
    homepage = add_HomePage('Skin Deep Home')
    # default_colour = 'ffffff'
    welcome_scrollpage = add_ScrollPage(homepage, 'welcome')
    zine_scrollpage = add_ScrollPage(homepage, 'zine')
    social_scrollpage = add_ScrollPage(homepage, 'social')

    # make the zineapp
    zineapp = add_ZineApp(zine_scrollpage)

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

    # make the containers
    welcome_container = add_Container(welcome_scrollpage, 'welcome_widget')
    home_tab = add_Tab(welcome_container, 'Home', 1, home_article)
    about_tab = add_Tab(welcome_container, 'About', 2, about_article)
    news_tab = add_Tab(welcome_container, 'News', 3, news_category)
    social_container = add_Container(social_scrollpage, 'social_widget')
    social_tab = add_Tab(social_widget, 'Social', 1, 3, social_category)

# homepage app models
def add_HomePage(title):
    return HomePage.objects.get_or_create(title=title)[0]

def add_ScrollPage(homepage, name):
    return ScrollPage.objects.get_or_create(homepage=homepage,
                                            name=name)[0]

# container app models
def add_Container(scrollpage, title):
    return Container.objects.get_or_create(scrollpage=scrollpage, title=title)[0]

def add_Tab(container, keyword, order, foreign_key, column_count=1):
    if(isinstance(foreign_key, Article)):
        return Tab.objects.get_or_create(container=container,
                                         keyword=keyword,
                                         order=order,
                                         column_count=column_count,
                                         article=foreign_key)[0]
    elif(isinstance(foreign_key, Category)):
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
    populate()