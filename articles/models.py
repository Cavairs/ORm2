from django.core.exceptions import ValidationError
from django.db import models


class Scope(models.Model):
    tag_text = models.CharField(max_length=50)
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.tag_text


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True,
                              verbose_name='Изображение')
    tags = models.ManyToManyField(
        Scope, through='ArticleTag', related_name='articles', blank=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class ArticleTag(models.Model):
    article = models.ForeignKey(
        Article, related_name='articletag_set', on_delete=models.CASCADE)
    scope = models.ForeignKey(Scope, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.article.title} - {self.scope.tag_text}"
