from django.contrib import admin

from .models import Profile, Activity, View, Post


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'description')

    def save_model(self, request, obj, form, change):
        obj.username = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)


admin.site.register(Profile)
admin.site.register(Activity)
admin.site.register(View)
admin.site.register(Post, PostAdmin)
