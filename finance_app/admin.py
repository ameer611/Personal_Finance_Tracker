from django.contrib import admin

from finance_app.models import Category, Transaction

admin.site.register([Transaction, Category])
