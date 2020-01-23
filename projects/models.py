from django.db import models
from django.urls import reverse

class Project(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    website = models.URLField()
    image = models.ImageField(upload_to='projects/')
    technology = models.CharField(max_length=40)
    completed = models.DateField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', args={'pk': self.pk})