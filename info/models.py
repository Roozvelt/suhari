from django.db import models

class OrganizationInfo(models.Model):
    title = models.CharField(max_length=255, default='О нас')
    content = models.TextField()

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title