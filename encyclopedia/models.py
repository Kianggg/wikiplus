from django.db import models

# Create your models here.
class WikiEntry(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    images = models.URLField()
    edits = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}"