from django.contrib import admin

from  .models import StudentUser, CommunityWriting, CommentModel

# Register your models here.

admin.site.register(StudentUser)
admin.site.register(CommunityWriting)
admin.site.register(CommentModel)

