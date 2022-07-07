from xml.etree.ElementTree import Comment
from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.CharField(max_length=30)
    user_pw = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    school_name = models.CharField(max_length=100)

    class Meta:
        abstract = True
    

class StudentUser(User):
    grade_number = models.IntegerField(default=1)
    class_number = models.IntegerField(default=1)
    student_number = models.IntegerField(default=1)

    def __str__(self):
        return self.user_id


class TimeStampedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CommentModel(TimeStampedModel):
    comment_user = models.ForeignKey(
            StudentUser,
            blank = False,
            null=False,
            on_delete = models.DO_NOTHING,
            related_name = 'comment_author'
        )
    comment_likes = models.ManyToManyField(StudentUser, blank=True)
    comment = models.TextField(blank=True)


class CommunityWriting(TimeStampedModel):

    FORMAT_CHOICES = (
        (1, 'Free writing'),
        (2, 'Suggestion'),
        (3, 'Notice'),
    )

    format_of_writing = models.IntegerField(
        choices=FORMAT_CHOICES, blank=True, default=1
    )
    author = models.ForeignKey(
                StudentUser,
                blank = False,
                null=False,
                on_delete = models.DO_NOTHING,
                related_name = 'post_author'
            )
    title = models.CharField(max_length=150, blank=True, default='Unnamed post')
    post = models.TextField(blank=True)
    post_likes = models.ManyToManyField(StudentUser, blank=True)
    comment_list = models.ManyToManyField(CommentModel, blank=True)

    



