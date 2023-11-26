from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Test(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True
    )
    is_active = models.BooleanField(
        default=False
    )
    description = models.CharField(
        max_length=300,
    )

    def __str__(self):
        return self.title


class Result(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
    )
    is_finished = models.BooleanField(default=False)
    test = models.ForeignKey(
        to=Test,
        on_delete=models.DO_NOTHING
    )
    total_result = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    test = models.ForeignKey(
        to=Test,
        on_delete=models.DO_NOTHING
    )
    text = models.CharField(
        max_length=250,
        verbose_name="Text",
        unique=True
    )

    is_active = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        to=Question,
        on_delete=models.DO_NOTHING,
        verbose_name='Question',
    )
    text = models.CharField(
        max_length=50,
        verbose_name='Text',
    )
    is_right = models.BooleanField()
    lock_other = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Answer(models.Model):

    result = models.ForeignKey(
        to=Result,
        on_delete=models.DO_NOTHING,
    )

    question = models.ForeignKey(
        to='Question',
        on_delete=models.DO_NOTHING,
    )
    is_right = models.BooleanField()
    choice = models.ForeignKey(
        to='Choice',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.choice.text
