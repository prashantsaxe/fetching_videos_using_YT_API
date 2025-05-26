from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail_url = models.URLField()
    
    class Meta:
        ordering = ['-published_at']  # For sorting in descending order using published_at

    def __str__(self):
        return self.title