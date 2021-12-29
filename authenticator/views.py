from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.serializers import Serializer

from authenticator.serializers import UserSerializer
from .models.user import User
from .models.role import Role
from django.core import serializers
from django.forms.models import model_to_dict
from rest_framework.parsers import JSONParser
from . import hasher
import json

# Create your views here.


def get_roles(request):
    if request.method == 'GET':
        roles = serializers.serialize('json', Role.objects.all())
        return HttpResponse(roles, content_type='application/json')


def get_role(request, id):
    if request.method == 'GET':
        role = Role.objects.get(id=id)
        return JsonResponse(model_to_dict(role))


def add_role(request):
    data = json.loads(request.body.decode('utf-8'))
    role = Role(name=data['role'], description=data['desc'])
    role.save()
    return JsonResponse(model_to_dict(role))


def sign_up(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        encoded = hasher.hash_password(data['password'])
        user = User(email=data['email'], first_name=data['first_name'],
                    last_name=data['last_name'], password=encoded, role=Role.objects.get(id=1))
        user.save()
    return JsonResponse(model_to_dict(user))


def sign_in(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return HttpResponse(status=404)
        new = hasher.check_password(data['password'], user.password)
        if hasher.check_password(data['password'],user.password):
            return JsonResponse(model_to_dict(user))
        else:
            return HttpResponse(status=401)


def get_users(request):
    users = serializers.serialize('json', User.objects.all())
    return HttpResponse(users, content_type='application/json')


def get_users(request, id):
    user = User.objects.get(id=id)
    return JsonResponse(model_to_dict(user))

def get_users(request, email):
    user = User.objects.get(email=email)
    return JsonResponse(model_to_dict(user))

def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)
