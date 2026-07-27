from django.db import models

# Create your models here.
class Summary(models.Model):
    url=models.URLField(unique=True)
    title=models.CharField(max_length=300)
    summary=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    last_accessed=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title