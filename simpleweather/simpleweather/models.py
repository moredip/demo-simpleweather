from datetime import datetime,timezone

from django.conf import settings
from django.db import models

# CachedTemperature is an intentionally silly mechanism for
# caching temperatures for a specific zipcode using an append-only store

class CachedTemperatureManager(models.Manager):
    def latest_entry_for_zipcode(self,zipcode):
        try:
            return self.filter(zipcode=zipcode).order_by('-created_at')[0]
        except IndexError:
            return None

    def latest_fresh_entry_for_zipcode(self,zipcode,ttl=settings.TEMPERATURE_CACHE_TTL):
        latest_entry = self.latest_entry_for_zipcode(zipcode)
        if not latest_entry:
            return None

        age_of_entry = datetime.now(timezone.utc) - latest_entry.created_at

        if age_of_entry > ttl:
            return None

        return latest_entry


class CachedTemperature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    zipcode = models.TextField()
    temperature = models.FloatField()

    objects = CachedTemperatureManager()

    def __str__(self):
        return f"{self.zipcode} @ {self.created_at} - {self.temperature}"
