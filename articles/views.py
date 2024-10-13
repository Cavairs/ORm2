from django.views.generic import ListView
from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'

    # Получаем все статьи
    object_list = Article.objects.all().order_by('-published_at')

    # Предзагружаем связанные данные
    for article in object_list:
        # Сортируем по 'tag_text' теги, которые не являются основными
        article.sorted_tags = article.articletag_set.filter(
            is_main=False).order_by('scope__tag_text')

    context = {
        'object_list': object_list,
    }

    return render(request, template, context)
