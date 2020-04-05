from django.contrib import admin
from .models import Custom_User_Model,Vote,Laws

admin.site.register(Custom_User_Model)
admin.site.register(Vote)
admin.site.register(Laws)
