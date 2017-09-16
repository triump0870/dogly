from django.contrib import admin
from django.db import DatabaseError, IntegrityError

from app.models import Dog, Visit
from django.contrib import messages


# Register your models here.
class DogModelAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url='', extra_context=None):
        try:
            return super(DogModelAdmin, self).add_view(request, form_url, extra_context)
        except (IntegrityError, DatabaseError) as e:

            request.method = 'GET'
            print "form: ", form_url
            messages.add_message(request, messages.ERROR, e.message)
            print e.message
            print "context=",extra_context
            return super(DogModelAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            return super(DogModelAdmin, self).change_view(request, object_id, form_url, extra_context)
        except (IntegrityError, DatabaseError) as e:

            request.method = 'GET'
            messages.error(request, e.message)
            print e.message

            return super(DogModelAdmin, self).change_view(request, object_id, form_url, extra_context)


admin.site.register(Dog, DogModelAdmin)
admin.site.register(Visit)
