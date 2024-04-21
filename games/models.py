import os
from django.conf import settings
from django.db import models
from datetime import datetime

from services.image_converter import ImageService

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/game_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField()
    developers = models.ManyToManyField(Developer, related_name='games')
    genres = models.ManyToManyField(Genre, related_name='games')
    tags = models.ManyToManyField(Tag, related_name='games')
    downloads = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)

        if self.image:
            image_path = self.image.path
            output_path = os.path.splitext(image_path)[0] + '.webp'
            ImageService.convert_and_resize_image(image_path, output_path)
            os.remove(image_path)
            self.image.name = 'media/game_images/' + os.path.basename(output_path)
            super(Game, self).save(update_fields=['image'], *args, **kwargs)


class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = ('game', 'user') 

    def __str__(self):
        return f"Review for {self.game.title} by {self.user.username}"

