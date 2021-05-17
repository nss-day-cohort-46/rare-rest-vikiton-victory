from django.db import models


class Post(models.Model):

    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateField()
    image_url = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    content = models.CharField(max_length=50)
    approved = models.BooleanField()
    tags = models.ManyToManyField("Tag", related_name="posts")