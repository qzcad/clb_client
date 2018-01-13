from django.db import models


class Parameter(models.Model):
    class TYPES:
        INTEGER = 'integer'
        FLOAT = 'float'
        STRING = 'string'
        TYPE_CHOICES = (
            (INTEGER, INTEGER),
            (FLOAT, FLOAT),
            (STRING, STRING),
        )
    TYPE_MAPPING = {
        'integer': int,
        'float': float,
        'string': str,
    }
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=15, choices=TYPES.TYPE_CHOICES,
                            default=TYPES.INTEGER)

    def __str__(self):
        return 'Parameter {}: {}'.format(self.name, self.type)


class Task(models.Model):
    name = models.CharField(max_length=120)
    parameters = models.ManyToManyField(Parameter)

    def __str__(self):
        return 'Task {}'.format(self.name)


class JobParameter(models.Model):
    parameter_type = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    @property
    def value_to_python(self):
        return self.parameter_type.TYPE_MAPPING[
            self.parameter_type.type](self.value)

    def __str__(self):
        return '{} ({})'.format(self.parameter_type, self.value)


class Job(models.Model):
    task = models.ForeignKey(Task, related_name='jobs',
                             on_delete=models.CASCADE)
    parameters = models.ManyToManyField(JobParameter)

    @property
    def args(self):
        return [parameter.value_to_python for parameter in self.parameters.all()]

    @property
    def kwargs(self):
        return {parameter.parameter_type.name: parameter.value_to_python
                for parameter in self.parameters.all()}

    def __str__(self):
        return 'Job: {} (#{})'.format(self.task, self.pk)
