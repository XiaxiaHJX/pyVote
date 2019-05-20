from django.contrib import admin

# Register your models here.
from .models import VoteHeadline,VoteOption_1


admin.site.register(VoteHeadline)
admin.site.register(VoteOption_1)

