from django.contrib import admin
from .models import Genre, Game, Tag, Review, Developer

admin.site.register(Genre)
admin.site.register(Game)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(Developer)