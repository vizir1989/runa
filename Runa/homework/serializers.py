from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from homework.models import Category


class CategorySerializer(serializers.ModelSerializer):
    parents = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    siblings = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parents', 'children', 'siblings']

    @staticmethod
    def get_parents(obj):
        result = []
        parent = obj.parent
        while parent:
            item = Category.objects.filter(name=parent).values('id', 'parent', 'name')[0]
            parent = item.pop('parent')
            result.append(item)
        return result

    @staticmethod
    def get_children(obj):
        result = [item for item in Category.objects.filter(parent=obj.name).values('id', 'name')]
        return result

    @staticmethod
    def get_siblings(obj):
        result = [item for item in Category.objects.filter(parent=obj.parent).exclude(name=obj.name).values('id', 'name')]
        return result


class CategoriesSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=250)
    children = serializers.ListField()

    @staticmethod
    def __dict_to_list(data, parent, result):
        result.append({'name': data['name'], 'parent': parent})
        if 'children' in data:
            for children in data['children']:
                CategoriesSerializer.__dict_to_list(children, data['name'], result)

    def create(self, validated_data):
        result = []
        CategoriesSerializer.__dict_to_list(validated_data, '', result)
        categories = []
        for item in result:
            categories.append(Category.objects.create(**item))
        return categories

    def update(self, instance, validated_data):
        raise ValidationError('update operation forbidden')
