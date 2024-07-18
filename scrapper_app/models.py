from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class EntitiesMaster(models.Model):
    web_url = models.URLField()
    details_json = models.JSONField()
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "EntitiesMaster"
        verbose_name_plural = "EntitiesMasters"
        ordering = ['-created_date']

    def __str__(self):
        return self.web_url

    def clean(self):
        if not self.web_url:
            raise ValidationError("Url cannot be empty")