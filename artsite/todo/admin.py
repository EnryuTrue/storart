from django.contrib import admin
from .models import User, ArtPost





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


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'status')
    list_filter = ('status',)
    actions = ['approve_as_seller', 'reject_as_seller']

    def approve_as_seller(self, request, queryset):
        queryset.update(status='seller')

    approve_as_seller.short_description = "Approve selected users as sellers"

    def reject_as_seller(self, request, queryset):
        queryset.update(status='basic_user')

    reject_as_seller.short_description = "reject selected users as sellers"


admin.site.register(User, UserProfileAdmin)
