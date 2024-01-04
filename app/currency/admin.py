from django.contrib import admin
from currency.models import Source, ContactUs, RequestResponseTimeMiddlewareModel


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
    list_display = ('id', 'source_url', 'source_name')
    list_filter = ('source_name',)
    search_fields = ('source_name',)


@admin.register(RequestResponseTimeMiddlewareModel)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'path', 'request_method', 'execute_time')
    list_filter = ('request_method',)
    search_fields = ('path',)
