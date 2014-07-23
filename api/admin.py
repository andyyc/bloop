from django.contrib import admin
from api.models import Play

class PlayAdmin(admin.ModelAdmin):
    list_display = ('gamekey', 'quarter', 'time', 'down', 'text', 'video_url')
admin.site.register(Play, PlayAdmin)