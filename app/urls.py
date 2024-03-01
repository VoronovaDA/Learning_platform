from django.urls import path
from .views import LessonListView, CourseViewSet, CourseListView

urlpatterns = [
    path("courses/", CourseViewSet.as_view()),
    path("courses/<int:course_id>/lessons/", LessonListView.as_view()),
    path("courses_info/", CourseListView.as_view()),
]
