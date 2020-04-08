from django.contrib import admin
from .models import Custom_User_Model,UserVote,Opinion,CodeVote

admin.site.register(Custom_User_Model)
admin.site.register(UserVote)
admin.site.register(Opinion)
admin.site.register(CodeVote)
