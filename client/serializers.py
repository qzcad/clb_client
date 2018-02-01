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
        parameters = cls._get_parameters(func)
        cl = cls._get_serializer_class_for_callable(func)
        for field, parameter in parameters.items():
            field_class = cls.serializer_field_mapping[parameter.annotation]
            field_obj = cls._get_field_for_parameter(field_class, parameter)
            cl._declared_fields[field] = field_obj
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

    @staticmethod
    def _get_parameters(func):
        signature = inspect.signature(func)
        return signature.parameters

    @staticmethod
    def _get_field_for_parameter(field_class, parameter):
        if parameter.default == inspect._empty:
            return field_class(required=True)
        return field_class(
            required=False,
            default=parameter.default
        )
