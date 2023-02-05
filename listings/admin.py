from . import models as LModels
from django.contrib import admin


# Register your models here.
class Ticket(admin.ModelAdmin):
    list_display = ["title", "user", "time_created"]


class Review(admin.ModelAdmin):
    list_display = ["user", "rating", "headline", "time_created"]


class UserFollows(admin.ModelAdmin):
    list_display = ["user", "followed_user"]


admin.site.register([LModels.Ticket, LModels.Review, LModels.UserFollows])
