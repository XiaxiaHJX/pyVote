from django.contrib.syndication.views import Feed
from django.shortcuts import reverse
from .models import Article

class BlogFeed(Feed):
    title='个人博客'
    description='一个很好的网站'
    link='/'

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body[:30]

    def item_link(self, item):
        return reverse('blog:detail',args=(str(item.id)))
