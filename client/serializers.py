import inspect

from rest_framework import serializers


class BaseTaskSerializer(serializers.Serializer):
    """
    Serializer aimed to create individual serializers.Serializer subclasses
    for functions to validate input parameters
    based on function argument type annotations.
    """
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
        """
        get Serializer subclass for function and
        dynamically add fields to it based on passed function.
        :param func: function
        :return: Serializer subclass with set of fields
        required to validate input arguments for function
        """
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
        """
        get Serializer subclass with name based on function name.
        :param func:
        :return: Serializer subclass
        """
        name = cls.__name__ + '_{}'.format(func.__name__)
        # check if serializer class already exists in cache
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
        """
        get parameters based on type annotations.
        :param func:
        :return: An ordered mapping of parameters’ names to
        the corresponding Parameter objects.
        """
        signature = inspect.signature(func)
        return signature.parameters

    @staticmethod
    def _get_field_for_parameter(field_class, parameter):
        """
        create field instance
        :param field_class: serializer.Field subclass
        :param parameter: inspect.Parameter instance
        :return: field instance
        """
        if parameter.default is inspect._empty:
            return field_class(required=True)
        return field_class(
            required=False,
            default=parameter.default
        )
