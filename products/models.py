from distutils.command.upload import upload
from django.db import models
from datetime import datetime
# Create your models here.

class Product(models.Model):
      name = models.CharField(max_length=150)
      description = models.TextField()
      price = models.DecimalField(max_digits=6, decimal_places=2)#5243.54
      photo = models.ImageField(upload_to = 'photos/%Y/%M/%D/')
      is_active = models.BooleanField(default=True)
      publish_data = models.DateTimeField(default=datetime.now)
      
      def __str__(self):
            return self.name
      class Meta :
            ordering = ['-publish_data']