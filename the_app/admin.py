from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(AppUser)
admin.site.register(Posts)
admin.site.register(Followers)
admin.site.register(Chatroom)
admin.site.register(ChatroomMessages)