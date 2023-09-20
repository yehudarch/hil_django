from django.contrib import admin

# Register your models here.
from .models import UserProfile, Contact, Clip, Frame, OnlineInterventions, Version, RSSUnsafe
from .models import RSSUnsafeTemp
from django.contrib.sessions.models import Session

admin.site.register(RSSUnsafeTemp)
admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(Clip)
admin.site.register(Frame)
admin.site.register(OnlineInterventions)
admin.site.register(Version)
admin.site.register(RSSUnsafe)
