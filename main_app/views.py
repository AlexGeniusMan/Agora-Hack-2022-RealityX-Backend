import json
from pprint import pprint

from django.shortcuts import render
from django.template import engines
from django.template.response import TemplateResponse
from rest_framework.views import APIView
from django.apps import apps
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from project.permissions import CustomIsAuthenticated
from .serializers import PageSerializer, ProductSerializer
from .models import Page, Product


def get_schema(request):
    schema = {}
    app_models = apps.get_app_config('main_app').get_models()
    for model in app_models:
        schema[model.__name__] = {}
        for field in model._meta.get_fields():
            schema[model.__name__][field.name] = type(field).__name__
    return schema


def get_object_from_queryset_by_id(queryset, object_id, default=None):
    try:
        return queryset.get(id=object_id)
    except BaseException:
        return default


class ProductsView(APIView):
    permission_classes = [CustomIsAuthenticated]

    def get(self, request):
        product = get_object_from_queryset_by_id(Product.objects.all(), request.query_params.get('product_id'))
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': 'Product not found.',
            })
        serializer = ProductSerializer(product, context={'request': request}).data

        return Response(status=status.HTTP_200_OK, data={
            'product': serializer,
        })

    def post(self, request):
        product = Product.objects.create(
            user=request.user,
            name=request.data['name'],
        )
        serializer = ProductSerializer(product, context={'request': request}).data

        return Response(status=status.HTTP_200_OK, data={
            'product': serializer,
        })

    def delete(self, request):
        product = get_object_from_queryset_by_id(Product.objects.all(), request.query_params.get('product_id'))
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': 'Product not found.',
            })
        product.delete()

        return Response(status=status.HTTP_200_OK, data={
            'message': 'Product deleted.',
        })


class UpdateProductView(APIView):
    permission_classes = [CustomIsAuthenticated]

    def post(self, request):
        product = get_object_from_queryset_by_id(Product.objects.all(), request.data['product_id'])
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': 'Product not found.',
            })
        if 'name' in request.data:
            product.name = request.data['name']
        product.save()
        serializer = ProductSerializer(product, context={'request': request}).data

        return Response(status=status.HTTP_200_OK, data={
            'product': serializer,
        })


class PagesView(APIView):
    permission_classes = [CustomIsAuthenticated]

    def get(self, request):
        page = get_object_from_queryset_by_id(Page.objects.filter(user=request.user),
                                              request.query_params.get('page_id'))
        if not page:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': 'Page not found.',
            })
        serializer = PageSerializer(page, context={'request': request}).data

        return Response(status=status.HTTP_200_OK, data={
            'page': serializer,
            'schema': get_schema(request),
        })

    def post(self, request):
        page = Page.objects.create(
            user=request.user,
            json=request.data['json'],
            template=request.data['template'],
        )
        serializer = PageSerializer(page, context={'request': request}).data

        return Response(status=status.HTTP_200_OK, data={
            'page': serializer,
            'schema': get_schema(request),
        })

    def delete(self, request):
        page = get_object_from_queryset_by_id(Page.objects.filter(user=request.user),
                                              request.query_params.get('page_id'))
        if not page:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': 'Page not found.',
            })
        page.delete()

        return Response(status=status.HTTP_200_OK, data={
            'message': 'Page deleted.',
        })


class UpdatePageView(APIView):
    permission_classes = [CustomIsAuthenticated]

    def post(self, request):
        page = get_object_from_queryset_by_id(Page.objects.filter(user=request.user),
                                              request.data['page_id'])
        if not page:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': 'Page not found.',
            })
        if 'json' in request.data:
            page.json = request.data['json']
        if 'template' in request.data:
            page.template = request.data['template']
        page.save()
        serializer = PageSerializer(page, context={'request': request}).data

        return Response(status=status.HTTP_200_OK, data={
            'page': serializer,
            'schema': get_schema(request),
        })


class PreviewView(APIView):

    def get(self, request):
        page = get_object_from_queryset_by_id(Page.objects.all(),
                                              request.query_params.get('page_id'))
        if not page:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': 'Page not found.',
            })
        temp = {}
        if not page.template:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': 'Page template is missing.',
            })
        for field in json.loads(page.template)['models'].items():
            model_name = field[1].split('.')[0]
            method = field[1].split('.')[1]
            model = apps.get_model('main_app', model_name)
            print(model_name, method, model)
            if method == 'all' and len(field[1].split('.')) == 2:
                queryset = model.objects.all()
            elif method == 'first':
                queryset = model.objects.first()
            elif method == 'all' and len(field[1].split('.')) == 3:
                queryset = model.objects.all()[0:int(field[1].split('.')[2])]
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={
                    'message': f"Invalid field: {len(field[1].split('.'))}"
                })
            temp[field[0]] = queryset
        print(temp)

        template = engines['django'].from_string(json.loads(page.template)['template'])

        return TemplateResponse(request=request, template=template, context=temp)
