from django.db import models

# Create your models here.
class Music(models.Model):
    Album = models.CharField(max_length=30)
    Title = models.CharField(max_length=30)
    Genre = models.CharField(max_length=30)
    Release_Date = models.DateField()
    Album_Image = models.ImageField(upload_to='Album_pics',blank=True)
    Artist = models.CharField(max_length=15)
    Poplularity = models.IntegerField()
    Artist_Image = models.ImageField(upload_to='Artist_pics',blank=True)
    Artist_Id = models.CharField(max_length=30)
    Track_Id = models.CharField(max_length=30)