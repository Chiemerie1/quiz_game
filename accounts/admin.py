from django.contrib import admin
from .models import User

# Register your models here.


admin.site.site_header = "Quiz Admin"
admin.site.site_title = "Welcome to Quiz Gamee Admin"
admin.site.index_title = "Quiz Game"


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "score"]

admin.site.register(User, UserAdmin)

