from django.contrib import admin
from .models import User, ArtPost

# Register your models here.
admin.site.register(User)


class ArtPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'timestamp')
    list_filter = ('status', 'category')
    actions = ['make_approved', 'make_rejected']

    def make_approved(self, request, queryset):
        queryset.update(status='approved')

    make_approved.short_description = "Mark selected posts as approved"

    def make_rejected(self, request, queryset):
        queryset.update(status='rejected')

    make_rejected.short_description = "Mark selected posts as rejected"


admin.site.register(ArtPost, ArtPostAdmin)
