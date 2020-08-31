from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from api_basic.models import Article
from api_basic.serializers import ArticleSerializer


class ArticleViewSet(viewsets.ViewSet):
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article  = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request, pk=None):
        article = Article.objects.get(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id = None):

        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id = None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)



class ArticleAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(APIView):

    def get_object(self, primary_key):
        try:
            return Article.objects.get(pk = primary_key)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, primary_key):
        article = self.get_object(primary_key)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, primary_key):
        article = self.get_object(primary_key)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, primary_key):
        article = self.get_object(primary_key)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @csrf_exempt
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many = True)
        # return JsonResponse(serializer.data, safe = False)
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = ArticleSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data, status = 201)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        # return JsonResponse(serializer.errors, status = 400)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, primary_key):
    try:
        article = Article.objects.get(pk = primary_key)
    except Article.DoesNotExist:
        # return HttpResponse(status = 404)
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        # return JsonResponse(serializer.data)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data = request.data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data)
            return Response(serializer.data)
        # return JsonResponse(serializer.errors, status = 400)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        # return HttpResponse(status = 204)
        return Response(status = status.HTTP_204_NO_CONTENT)