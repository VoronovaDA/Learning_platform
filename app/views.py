from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from app.models import Lesson, Course
from app.serializers import LessonSerializer, CourseSerializer, CourseSummarySerializer


class CourseViewSet(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def distribute_users(self, instance, groups):
        """Распределение пользователей по группам"""

        if instance.course.created_at > timezone.now():
            students = sum([group.user.count() for group in groups])
            avg_st_group = students // len(groups)
            for group in groups:
                st_count = group.user.count()
                if st_count > avg_st_group + 1:
                    group.students.remove(instance.user)
                    print(f"Студент {instance.user} удален из группы {group.name}.")
                elif st_count < avg_st_group - 1:
                    group.user.add(instance.user)
                    print(f"Студент {instance.user} добавлен в группу {group.name}.")
                    break


class LessonListView(ListAPIView):
    """Вывод списка уроков по конкретному продукту к которому пользователь имеет доступ"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        user = self.request.user

        try:
            course = Course.objects.get(id=course_id, creator=user)
        except Course.DoesNotExist:
            return Lesson.objects.none()

        return Lesson.objects.filter(course_lesson=course)


class CourseListView(ListAPIView):
    """Вывод статистики по курсам"""

    queryset = Course.objects.all()
    serializer_class = CourseSummarySerializer
