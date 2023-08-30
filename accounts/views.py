
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import Users
import json
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
def dataConversion(user):
    data = user.decode('utf-8').replace('\n', '').replace('\r', '')
    json_data = json.loads(data)
    return json_data

def customErrorMessage(error_data):
    error_messages = error_data.get("error",{})
    error_message = None
    for field, messages in error_messages.items():
        if messages:
            error_message = messages[0]
        return error_message
        break




def fetchUsers():
    users = Users.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({"message":"successfully fetched all users", "users":serializer.data, "status":status.HTTP_200_OK})


def signUp(req):
    diction = dataConversion(req.body)
    serializer = UserSerializer(data=diction)
    if serializer.is_valid():
        serializer.save()
        user = Users.objects.get(email=diction['email'])
        user.set_password(diction['password'])
        user.save()
        return Response({"message":"successfly added user", "user":serializer.data, "status":status.HTTP_200_OK})
    return Response({"message":customErrorMessage({"error":serializer.errors}), "status":status.HTTP_400_BAD_REQUEST})


def signIn(req):
    user = dataConversion(req.body)
    try:
        usr = get_object_or_404(Users, email=user['email'])
    except:
        return Response({"message":"A user with that email does not exist"})
    found_user = authenticate(email=user['email'], password=user['password'])
    if not found_user:
        return Response({"message":"Incorect password", "status":status.HTTP_400_BAD_REQUEST})
    token, _ = Token.objects.get_or_create(user=usr)
    serializer = UserSerializer(instance=usr)
    #login(req, usr) --- gives an issue when trying a post route later
    return Response({"message":"lets log in your", "data":serializer.data , "token":token.key, "status":status.HTTP_200_OK})


def fetchUser(id, user):
    return Response({"message": user, "status":status.HTTP_200_OK})

def updateUser(req, user):
    user_data = dataConversion(req.body)
    serializer = UserSerializer(user, data=user_data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"successfully updated the user", "status": status.HTTP_200_OK})
    return Response({"message": customErrorMessage({"error":serializer.errors}), "status":status.HTTP_400_BAD_REQUEST})

def patchUser(req, user):
    user_data = dataConversion(req.body)
    serializer = UserSerializer(user, data=user_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"successfully patched the user", "status": status.HTTP_200_OK})
    return Response({"message": customErrorMessage({"error":serializer.errors}), "status":status.HTTP_400_BAD_REQUEST})


def removeUser(req, user):
    user.delete()
    return Response({"message":"successfully removed the user from the database", "status":status.HTTP_200_OK})


@api_view(['GET','POST'])
def users_view(req):
    if req.method == 'GET':
        return fetchUsers()

    elif req.method == 'POST':
        return signUp(req)

@api_view(['POST'])
def sign_view(req):
    if req.method == 'POST':
        return signIn(req)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def specific_user_view(req):
    id = req.user._id
    serializer = UserSerializer(instance=req.user)
    if req.method == 'GET':
        return fetchUser(id, serializer.data)
    elif req.method == 'PUT':
        return updateUser(req, req.user)
    elif req.method == 'PATCH':
        return patchUser(req, req.user)
    elif req.method == 'DELETE':
        return removeUser(req, req.user)



