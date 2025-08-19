from django.contrib import admin

# Register your models here.

from .models import Member, Event, Notice, Music, File, MusicMember

class FilesInline(admin.TabularInline):
    model = File
    extra = 1
class MusicAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'year', 'created_at']
    search_fields = ['name', 'author']
    inlines = [FilesInline]

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'location']
    search_fields = ['name', 'date', 'location']

admin.site.register(Member)
admin.site.register(Event, EventAdmin)
admin.site.register(Notice)
admin.site.register(Music, MusicAdmin)
admin.site.register(MusicMember)
