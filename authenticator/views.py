from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.serializers import Serializer

from authenticator.serializers import RoleSerializer, UserSerializer
from .models.user import User
from .models.role import Role
from .models.token import Token
from django.core import serializers
from rest_framework.parsers import JSONParser
from . import hasher
import json


def refresh_token(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        payload = hasher.decode_refresh_token(data['refresh_token'])
        if (payload is None or payload['user'] != data['email']):
            return JsonResponse({}, status=401)
        try:
            user = User.objects.get(email=payload['user'])
        except User.DoesNotExist:
            return JsonResponse({}, status=401)
        token = __make_token(user, data['refresh_token'])
        if token is None:
            return JsonResponse({}, status=401)
        return JsonResponse({"access_token": token.access_token, "refresh_token": token.refresh_token})


def roles(request):
    if request.method == 'GET':
        roles = RoleSerializer(Role.objects.all(), many=True)
        return JsonResponse(roles.data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        role = Role(name=data['role'], description=data['desc'])
        role.save()
        return JsonResponse(RoleSerializer(role).data, safe=False)


def role_detail(request, id):
    try:
        role = Role.objects.get(id=id)
    except Role.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        return JsonResponse(RoleSerializer(role).data)
    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        if (not data):
            return JsonResponse({}, status=204)
        if ('name' in data and len(data['name']) != 0):
            role.name = data['name']
        if ('description' in data and len(data['description']) != 0):
            role.description = data['description']
        role.save()
        return JsonResponse(RoleSerializer(role).data)
    elif request.method == 'DELETE':
        role.delete()
        return JsonResponse({}, status=204)


def authorize(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return JsonResponse({}, status=404)
        if hasher.check_password(data['password'], user.password):
            token = __make_token(user)
            return JsonResponse({"user": user.email, "role": user.role.name, "access_token": token.access_token, "refresh_token": token.refresh_token})
        else:
            return JsonResponse({}, status=401)


def logout(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if not __logout(data['email']):
            return JsonResponse({}, status=404)
        return JsonResponse()


def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        encoded = hasher.hash_password(data['password'])
        user = User(email=data['email'], first_name=data['first_name'],
                    last_name=data['last_name'], password=encoded, role=Role.objects.get(id=1))
        user.save()
        return JsonResponse(UserSerializer(user).data)


def user_detail(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({}, status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        if not data:
            return JsonResponse({}, status=204)
        user = __update_user(user, data)
        return JsonResponse(UserSerializer(user).data)

    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({}, status=204)


def __make_token(user, old_token=None):
    access_token = hasher.encode_access_token(user.email)
    refresh_token = hasher.encode_refresh_token(user.email)
    try:
        token = Token.objects.get(user=user.id)
        if (old_token != None and token.refresh_token != old_token):
            return None
        token.access_token = access_token
        token.refresh_token = refresh_token
    except Token.DoesNotExist:
        token = Token.objects.create(
            user=user, access_token=access_token, refresh_token=refresh_token)
    token.save()
    return token


def __update_user(user, data):
    if ('email' in data and len(data['email'])!=0):
        __logout(user.email)
        user.email = data['email']
    if ('first_name' in data and data['first_name'] is not None):
        user.first_name = data['first_name']
    if ('last_name' in data and  data['last_name'] is not None):
        user.last_name = data['last_name']
    if ('role' in data and data['role'] is not None):
        try:
            new_role = Role.objects.get(id=data['role'])
            user.role = new_role
        except Role.DoesNotExist:
            pass
    if ('password' in data and data['password'] is not None):
        if (hasher.check_password(data['password']['old'], user.password)):
            if (data['password']['new'] == data['password']['confirm']):
                user.password = hasher.hash_password(
                    data['password']['new'])
                __logout(user.email)
    user.save()
    return user


def __logout(email):
    try:
        # Not the efficent way, but works
        user_id = User.objects.only('id').get(email=email)
        token = Token.objects.get(user=user_id)
        token.delete()
    except (User.DoesNotExist, Token.DoesNotExist):
        return False
    return True
