import inspect

from rest_framework import serializers


class BaseTaskSerializer(serializers.Serializer):
    serializer_field_mapping = {
        int: serializers.IntegerField,
        float: serializers.FloatField,
        str: serializers.CharField,
        list: serializers.ListField,
        dict: serializers.DictField,
    }

    SERIALIZER_CLASSES = {}

    @classmethod
    def for_func(cls, func):
        if not callable(func):
            raise NotImplementedError()
        signature = inspect.signature(func)
        cl = cls._get_serializer_class_for_callable(func)
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

    @classmethod
    def _get_serializer_class_for_callable(cls, func):
        name = cls.__name__ + '_{}'.format(func.__name__)
        serializer_class = cls.SERIALIZER_CLASSES.get(name)
        if not serializer_class:
            serializer_class = type(
                name,
                cls.__bases__,
                dict(cls.__dict__)
            )
            cls.SERIALIZER_CLASSES[name] = serializer_class
        return serializer_class
