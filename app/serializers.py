from rest_framework import serializers

from app.models import Course, Lesson, UserProfile, Group


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов с добавлением колонки кол-ва уроков и формата данных"""

    lesson_count = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    def get_lesson_count(self, item):
        return Lesson.objects.filter(course_lesson=item).count()

    class Meta:
        model = Course
        fields = ["id", "creator", "course_name", "created_at", "price", "lesson_count"]


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Lesson
        fields = ["id", "course_lesson", "title", "video_link"]


class CourseSummarySerializer(serializers.ModelSerializer):
    """Сериализатор для вывода статистики по курсам"""

    students_count = serializers.SerializerMethodField()
    group_fill_percentage = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    def get_students_count(self, course):
        return UserProfile.objects.filter(course_user=course).count()

    def get_group_fill_percentage(self, course):
        total_groups = Group.objects.filter(course_group=course).count()
        if total_groups == 0:
            return 0
        total_students = UserProfile.objects.filter(course_user=course).count()
        max_group_sum = sum(
            group.max_users for group in Group.objects.filter(course_group=course)
        )
        return f"{((total_students / max_group_sum) * 100):.2f}"

    def get_purchase_percentage(self, course):
        total_users = UserProfile.objects.count()
        access_count = UserProfile.objects.filter(course_user=course).count()
        if total_users == 0:
            return 0
        return f"{((access_count / total_users) * 100):.2f}"

    class Meta:
        model = Course
        fields = [
            "id",
            "course_name",
            "students_count",
            "group_fill_percentage",
            "purchase_percentage",
        ]
