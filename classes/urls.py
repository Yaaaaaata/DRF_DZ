from django.urls import path
from rest_framework.routers import DefaultRouter

from classes.apps import ClassesConfig
from classes.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView

app_name = ClassesConfig.name

router = DefaultRouter()

router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path("payment/", PaymentListAPIView.as_view(), name="payment-list"),
    path('sub/create/<int:course_id>/', SubscriptionCreateAPIView.as_view(), name='sub-create'),
    path('sub/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='sub-delete')
] + router.urls

