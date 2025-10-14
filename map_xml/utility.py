from django.contrib.sitemaps import Sitemap
from django.contrib import sitemaps
from django.urls import reverse

from blog.models import Blog, PostCategory
from event.models import Event, EventsCategory


class PostCategorySitemap(Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return PostCategory.objects.filter(is_active=True, is_deleted=False)


class BlogSitemap(Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return Blog.objects.get_all_active()


class EventsCategorySitemap(Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return EventsCategory.objects.filter(is_active=True, is_deleted=False)


class EventSitemap(Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return Event.objects.filter(save_type="P", is_active=True, is_deleted=False)


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return [
            'application:home', 'account:login', "account:register", "about:about",
            'contact:contact', 'contact:request',
            'blogs:blogs', "events:events"
        ]

    def location(self, item):
        return reverse(item)


#
# ##############################################################
SiteMaps = {}


def add_to_sitemaps(key, value, flag=0):
    # add
    if flag == 0:
        SiteMaps[key] = value
    # update
    else:
        SiteMaps.update({key: value})


add_to_sitemaps('static', StaticViewSitemap)
add_to_sitemaps('PostCategory', PostCategorySitemap)
add_to_sitemaps('Blog', BlogSitemap)
add_to_sitemaps('EventsCategory', EventsCategorySitemap)
add_to_sitemaps('Event', EventSitemap)
