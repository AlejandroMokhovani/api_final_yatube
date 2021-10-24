from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db.models import F, Q

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE,
        related_name="posts", blank=True, null=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text


class Follow(models.Model):
    # ссылка на объект пользователя, который подписывается
    user = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE,
    )
    # ссылка на объект пользователя, на которого подписываются
    following = models.ForeignKey(
        User, related_name="following", blank=True, null=True,
        on_delete=models.CASCADE,
    )

    # лучше костыль в руке чем CheckConstraint в небе
    # но замечание устранено - проверка на уровне модели
    def clean(self):
        if self.user == self.following:
            raise serializers.ValidationError(
                _('Себя фоловить нельзя!'), code='invalid'
            )

    def save(self, *args, **kwargs):
        self.clean()
        return super(Follow, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_following'
            ),
            # опытные люди сказали что это 102% рабочий код, но почему то нет
            # и, к сожалению, никто не может объяснить как это работает

            #     models.CheckConstraint(
            #     check=~models.Q(user=models.F('following')),
            #     name='not_yourself_follow'
            # ),
        ]
