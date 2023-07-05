from django.contrib import admin
from .models import Room, Message, Topic
# Register your models here.


admin.AdminSite.site_title = "StudyBuddy"

class RoomAdmin(admin.ModelAdmin):
    # fields = ["host", "topic", "description", "name"]
    fieldsets = [
        ("Author", {
            "fields": ["host"]
            }),
        ("Fields", {
            "fields": ["name", "topic", "description"]
            }),
        ]
    list_display = ("name", "host", "description")
    list_filter= ["host","created"]
    
admin.site.register([Message, Topic])
admin.site.register(Room, RoomAdmin)
