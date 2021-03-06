from django.contrib import admin
from core.models import Event
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'event_date', 'creation_date', 'description')
    list_filter = ('title', 'event_date',)


admin.site.register(Event, EventAdmin)