from django.contrib import admin
from .models import Roadmap, Task, CustomUser, PasswordResetToken

# Register your models here.
admin.site.register(Roadmap)
admin.site.register(Task)
admin.site.register(CustomUser)
admin.site.register(PasswordResetToken)
