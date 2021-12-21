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
import bcrypt

# Create your views here.


def get_roles(request):
    if request.method == 'GET':
        roles = serializers.serialize('json', Role.objects.all())
        return HttpResponse(roles, content_type='application/json')


def add_role(request):
    data = json.loads(request.body.decode('utf-8'))
    role = Role(name=data['role'], description=data['desc'])
    role.save()
    return JsonResponse(model_to_dict(role))


def sign_up(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        #key = hashlib.pbkdf2_hmac(
         #   'sha256', data['password'].encode('utf-8'), salt, 1000)
        #password = (salt+key).hex()
    #     user = User(email=data['email'], first_name=data['first_name'],
    #                 last_name=data['last_name'], password=hashed_password, role=Role.objects.get(id=1))
    #     user.save()
    # return JsonResponse(model_to_dict(user))
    #return HttpResponse(base64.b64encode(password.encode('utf-8')), content_type='application/json')
        key = bcrypt.kdf(data['password'].encode('utf-8'), bcrypt.gensalt(), 32, 1000)
    #return JsonResponse({'hex-salt': salt.hex(), 'hex-password':key.hex(), 'hex-salt+password':(salt+key).hex()})
    return HttpResponse(base64.b64encode(key.hex().encode('utf-8')), content_type='application/json')


def sign_in(request):
    user = User.objects.get(email=request.POST['email'])
    return JsonResponse(user)


def get_users(request):
    users = serializers.serialize('json', User.objects.all())
    return HttpResponse(users, content_type='application/json')
