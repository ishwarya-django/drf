from django.db import models

# Create your models here.
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

  
class Transformer(models.Model):
    name = models.CharField(max_length=150, unique=True)
    alternate_mode = models.CharField(
        max_length=250,
        blank=True,
        null=True)
    description = models.CharField(
        max_length=500,
        blank=True,
        null=True)
    alive = models.BooleanField(default=False)
    image=models.ImageField(upload_to=upload_to, blank=True, null=True)
    class Meta:
        ordering = ('name',)
  
    def __str__(self):
        return self.name

class Product(models.Model):
    product=models.CharField(max_length=30)
    cost = models.IntegerField()
    def __str__(self):
        return self.product

class Singer(models.Model):
    name=models.CharField(max_length=30)
    gender =models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Song(models.Model):
    singer=models.ForeignKey(Singer,on_delete=models.CASCADE ,related_name="sung_by")
    title =models.CharField(max_length=30)
    duration= models.IntegerField()
    def __str__(self):
        return self.title



