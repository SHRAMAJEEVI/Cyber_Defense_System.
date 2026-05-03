from django.contrib import admin
from .models import AttackLog


@admin.register(AttackLog)
class AttackLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'username_attempted', 'password_attempted', 'timestamp', 'attack_type')
    list_filter = ('attack_type', 'timestamp')
    search_fields = ('ip_address', 'username_attempted')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
