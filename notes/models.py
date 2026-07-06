from django.db import models
from django.contrib.auth.models import User
from .ai import get_embedding


class Note(models.Model):

    CATEGORY_CHOICES = [
        ("AI", "AI"),
        ("ML", "Machine Learning"),
        ("DL", "Deep Learning"),
        ("NLP", "NLP"),
        ("CV", "Computer Vision"),
        ("Programming", "Programming"),
        ("Other", "Other"),
    ]

    # Owner of the note
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    title = models.CharField(max_length=255)

    content = models.TextField()

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="Other"
    )

    favorite = models.BooleanField(default=False)

    embedding = models.JSONField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        text = f"{self.title} {self.content}"

        self.embedding = get_embedding(text)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

    from django.contrib.auth.models import User

class SearchHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    query = models.CharField(max_length=255)

    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query