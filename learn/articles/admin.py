from django.contrib import admin
from articles.models import UserDetails, Category, Articles

# Register your models here.
admin.site.register(UserDetails)

admin.site.register(Articles)

admin.site.register(Category)