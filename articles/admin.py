from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Scope, ArticleTag


class ArticleTagInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Флаг будет указывать найден ли основной тег
        has_main_tag = False

        # Проходим через каждую форму в наборе форм (формсете)
        for form in self.forms:
            # Проверяем, валидированные ли данные; данный объект не удален
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_main', False):
                    if has_main_tag:  # Если основной тег уже был найден, выходим с ошибкой
                        raise ValidationError(
                            'У статьи может быть только один основной тег.')
                    has_main_tag = True

        # Если мы прошли все формы, и ни один основной тег не был найден, показываем ошибку
        if not has_main_tag:
            raise ValidationError(
                'У статьи должен быть хотя бы один основной тег.')


class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    formset = ArticleTagInlineFormSet
    extra = 3
    fields = ['scope', 'is_main']


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag_text']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    inlines = [ArticleTagInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        for formset in formsets:
            if isinstance(formset, ArticleTagInlineFormSet) and not formset.is_valid():
                raise ValidationError("Пожалуйста, исправьте ошибки в тегах.")
