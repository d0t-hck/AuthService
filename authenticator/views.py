from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .models.user import User
from .models.role import Role
from django.core import serializers
from django.forms.models import model_to_dict
import hashlib
import json
import base64
import os

# Create your views here.


def get_roles(request):
    if request.method == 'GET':
        roles = serializers.serialize('json', Role.objects.all())
        return HttpResponse(roles, content_type='application/json')

def get_roles(request, id):
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
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
           'sha256', data['password'].encode('utf-8'), salt, 100000).hex()
        key = base64.b64encode(key.encode('utf-8')).decode()
        salt = base64.b64encode(salt.hex().encode('utf-8')).decode()
        password = salt + key
        user = User(email=data['email'], first_name=data['first_name'],
                    last_name=data['last_name'], password=password, role=Role.objects.get(id=1))
        user.save()
    return JsonResponse(model_to_dict(user))


def sign_in(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(email=data['email'])
        if user is not None:
            salt = base64.b64decode(user.password[:88].encode('ascii'))
            new_key = hashlib.pbkdf2_hmac('sha256', data['password'].encode('utf-8'), salt, 100000).decode('ascii')
            key = base64.b64decode(user.password[88:].encode('ascii')).decode('ascii')
            return JsonResponse({"new-key":new_key, "key":key})
        else:
            return JsonResponse({"404":"user not found"})


def get_users(request):
    users = serializers.serialize('json', User.objects.all())
    return HttpResponse(users, content_type='application/json')

def get_users(request, id):
    user = User.objects.get(id=id)
    return JsonResponse(model_to_dict(user))

