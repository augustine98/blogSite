from django.contrib import admin
from .models import Post , Community, Comment
from mptt.admin import MPTTModelAdmin
# Register your models here.
admin.site.register(Post)
admin.site.register(Community)
admin.site.register(Comment , MPTTModelAdmin)