import profile
from rest_framework import serializers

from .models import StudentUser, CommunityWriting, CommentModel

import datetime


class StudentUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StudentUser
        fields = [
            'user_id',
            'user_pw',
            'name',
            'phone_number',
            'email',
            'grade_number',
            'class_number',
            'student_number'
        ]


class ID_Name(serializers.ModelSerializer):

    class Meta:

        model = StudentUser
        fields = [
            'user_id', 'name'
        ]


class CommentSerializer(serializers.ModelSerializer):
    
    comment_user = ID_Name(read_only=True)
    comment_likes = ID_Name(many=True, read_only=True)

    class Meta:

        model = CommentModel
        fields = [
            'create_at',
            'update_at',
            'comment_user',
            'comment',
            'comment_likes',
        ]


class CommunityWritingSerializer(serializers.ModelSerializer):
    author = ID_Name(read_only=True)
    post_likes = ID_Name(many=True, read_only=True)
    comment_list = CommentSerializer(many=True,read_only=True)

    class Meta:

        model = CommunityWriting
        fields = [
            'create_at',
            'update_at',
            'format_of_writing',
            'title',
            'post',
            'post_likes',
            'author',
            'comment_list',
        ]


class Post_CommunityWritingSerializer(serializers.ModelSerializer):
    post_likes = ID_Name(many=True, read_only=True)

    class Meta:

        model = CommunityWriting
        fields = [
            'create_at',
            'update_at',
            'format_of_writing',
            'title',
            'post',
            'post_likes',
            'author',
            'comment',
        ]