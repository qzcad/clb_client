from django.contrib import admin

from .models import Parameter, Task, JobParameter, Job

admin.site.register(Parameter)
admin.site.register(Task)
admin.site.register(JobParameter)
admin.site.register(Job)
