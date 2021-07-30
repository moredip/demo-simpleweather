from django.db import models

# an intentionally silly mechanism for caching temperatures for a
# specific zipcode using an append-only store

class CachedTemperature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    zipcode = models.TextField()
    temperature = models.FloatField()
