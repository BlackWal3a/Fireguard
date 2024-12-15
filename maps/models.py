from django.db import models
from django.utils import timezone

class CoordinateData(models.Model):
    title = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - ({self.latitude}, {self.longitude})"

