from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from ServerApi import serializers

from ServerApi.models import CommentModel, StudentUser
from ServerApi.models import CommunityWriting as Post

from ServerApi.serializers import CommentSerializer, StudentUserSerializer
from ServerApi.serializers import CommunityWritingSerializer as PostSerializer
from ServerApi.serializers import Post_CommunityWritingSerializer as P_PostSerializer

from rest_framework.parsers import JSONParser

# Create your views here.


@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        query_set = StudentUser.objects.all()
        serializer = StudentUserSerializer(query_set, many= True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == "POST":
        data = JSONParser().parse(request)

        try:
            getUser = StudentUser.objects.get(user_id=data['user_id'])
            return JsonResponse({"Message" : "this user id is already exist"})
        except StudentUser.DoesNotExist:
            pass

        try:
            getUser = StudentUser.objects.get(
                grade_number=data['grade_number'], 
                class_number=data['class_number'], 
                student_number=data['student_number']
            )
            return JsonResponse({"Message" : "this studentID is already exist"})
        except StudentUser.DoesNotExist:
            pass

        try:
            getUser=StudentUser.objects.get(email=data['email'])
            return JsonResponse({"Message" : "this email is already useing"})
        except StudentUser.DoesNotExist:
            pass

        serializer = StudentUserSerializer(data=data) 

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"Message" : "user creating has succeeded"}, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def user(request,user_id) :
    try:
        user_data = StudentUser.objects.get(user_id=user_id)
    except: 
        return JsonResponse({"Message" : "data find error"})

    if request.method == 'GET':
        serializer = StudentUserSerializer(user_data)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = StudentUserSerializer(user_data, data=data)

        if serializer.is_valid():
            return JsonResponse(serializer, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user_data.delete()
        return JsonResponse(status=204)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_user = data['user_id']
        user_data = StudentUser.objects.get(user_id=search_user)

        if data['user_pw'] == user_data.user_pw:
            return JsonResponse({"Message": "login success"}, status=200)
        else:
            return JsonResponse({"Message" : "login fail"}, status=400)


@csrf_exempt
def post_list(request):
    if request.method == 'GET':
        query_set = Post.objects.all()
        serializer = PostSerializer(query_set, many= True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = P_PostSerializer(data=data) 

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"Message" : "posting has successed"}, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def post_edit(request, post_id):
    try :
        getpost = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"Message" : "This post is not exist"})

    if request.method == "GET":
        serializer = PostSerializer(getpost)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = PostSerializer(getpost, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == "DELETE":
        getpost.delete()
        return JsonResponse({"Message" : "post deleting has successd"})


@csrf_exempt
def post_comments(request, post_id):
    try :
        getpost = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"Message" : "This post is not exist"})

    if request.method == "GET":
        comment_serializer = CommentSerializer(getpost.comment_list, many=True)
        return JsonResponse(comment_serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        try :
            getUser = StudentUser.objects.get(user_id=data['comment_user'])
        except:
            return JsonResponse({"Message" : "User is not exist"})
        
        comment = CommentModel.objects.create(comment=data['comment'], comment_user=getUser)
        comment_serializer = CommentSerializer(comment)

        getpost.comment_list.add(comment)
        serializer = PostSerializer(getpost)
        return JsonResponse(serializer.data, status=201, safe=False)

    return JsonResponse({"" : ""})
