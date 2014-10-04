from django.contrib import admin
from api.models import Play

class PlayAdmin(admin.ModelAdmin):
    pass
admin.site.register(Play, PlayAdmin)