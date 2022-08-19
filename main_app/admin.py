from django.contrib import admin

from main_app.models import Project, Page, Product


# class SessionAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'created_at', 'took_at', 'processed_at', 'received_at', 'duration', 'soundtrack', 'processing_time',
#         'is_failed', 'has_expired_mp3', 'processed_counter', 'status', 'first_page_passed', 'second_page_passed',
#         'waited_for_loading_end', 'feedback_results',)
#     list_filter = ('status', 'worker_ip')
#     search_fields = ['id']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user',)


class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'project',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Product, ProductAdmin)
