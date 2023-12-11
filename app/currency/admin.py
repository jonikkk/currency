from django.contrib import admin
from currency.models import Source, ContactUs


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'email_from', 'subject', 'message')
    list_filter = ('email_from',)
    search_fields = ('email_from',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('source_id', 'source_url', 'source_name')
    list_filter = ('source_name',)
    search_fields = ('source_name',)
