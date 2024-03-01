from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Course(models.Model):
    """Модель по основному продукту - 'Курсы'"""

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    course_name = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"


class UserProfile(models.Model):
    """Модель для определения доступа пользователя к курсам"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    course_user = models.ForeignKey(Course, on_delete=models.CASCADE)

    def has_access_to_course(self, course):
        if course.group_set.exists():
            for group in course.group_set.all():
                if self.user in group.users.all():
                    return True
        return False


class Lesson(models.Model):
    """Модель по урокам курсов"""

    course_lesson = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False, blank=False)
    video_link = models.URLField(null=False, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "lesson"
        verbose_name_plural = "lessons"


class Group(models.Model):
    """Модель групп пользователей на курсах"""

    group_name = models.CharField(max_length=50, null=False, blank=False)
    course_group = models.ForeignKey(Course, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="users_groups")
    min_users = models.IntegerField()
    max_users = models.IntegerField()

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = "group"
        verbose_name_plural = "groups"
