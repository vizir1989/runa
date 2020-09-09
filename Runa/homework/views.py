from django.http import Http404

from homework.models import Category
from rest_framework.views import APIView
from rest_framework.response import Response
from homework.serializers import CategoriesSerializer, CategorySerializer
from rest_framework import status


class Categories(APIView):
    """
    List all categories, or create a new categories.
    """
    def post(self, request):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        snippet = self.get_object(pk)
        serializer = CategorySerializer(snippet)
        return Response(serializer.data)

