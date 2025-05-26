from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=50, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    published_at = models.DateTimeField(db_index=True)
    thumbnail_url = models.URLField()
    channel_title = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['channel_title', '-published_at']),
        ]
        
    def __str__(self):
        return self.title