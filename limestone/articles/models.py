from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db.models import Count


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_article')
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)], unique=True)
    content = models.TextField(max_length=10000)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    # Get dictionary, key - article, value - numbers of article comments
    @staticmethod
    def comment_statistics():
        statistic = {article: article.article_comment.all().count()
                     for article in Article.objects.all() if article.tag.all().count() > 1}
        return sorted(statistic.items(), key=lambda x: x[1], reverse=True)

    class Meta:
        ordering = ['created_at', 'updated_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comment')
    content = models.TextField(max_length=500)
    add_at = models.DateTimeField(default=timezone.now)

    @property
    def is_article_author(self):
        return self.article.author == self.author

    class Meta:
        ordering = ['add_at']

    def __str__(self):
        return self.content


class Tag(models.Model):
    title = models.CharField(max_length=35)
    slug = models.TextField(max_length=250)
    article = models.ManyToManyField(Article, related_name='tag')

    @property
    def rating(self):
        return self.article.all().count()

    def __str__(self):
        return self.title
