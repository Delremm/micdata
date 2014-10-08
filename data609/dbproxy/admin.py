from dbproxy.models import Node, NodeUser, Space, UserSpace, Server

from django.contrib import admin
admin.site.register(Node)
admin.site.register(NodeUser)
admin.site.register(Space)
admin.site.register(UserSpace)
admin.site.register(Server)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from dbproxy.models import Profile


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'employee'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Profile)
