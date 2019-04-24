from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class TestSnippet(models.Model):
    """A snippet model for testing purposes."""
    text = models.CharField(max_length=255)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text