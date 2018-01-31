import inspect

from rest_framework import serializers


class BaseTaskSerializer(serializers.Serializer):
    # TODO: extend serializer_field_mapping
    serializer_field_mapping = {
        int: serializers.IntegerField,
    }

    @classmethod
    def for_func(cls, func):
        if not callable(func):
            raise NotImplementedError()
        signature = inspect.signature(func)
        cl = type(
            cls.__name__ + '_{}'.format(func.__name__),
            cls.__bases__,
            dict(cls.__dict__)
        )
        for field, parameter in signature.parameters.items():
            field_class = cls.serializer_field_mapping[parameter.annotation]
            if parameter.default == inspect._empty:
                cl._declared_fields[field] = field_class(required=True)
            else:
                cl._declared_fields[field] = field_class(
                    required=False,
                    default=parameter.default
                )
        return cl
