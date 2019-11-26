from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    website = models.URLField()
    image = models.ImageField(upload_to='projects/')
    completed = models.DateField()

    def __str__(self):
        return self.title