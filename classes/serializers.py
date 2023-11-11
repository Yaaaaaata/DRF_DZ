from rest_framework import serializers
from classes.models import Course, Lesson, Payment, Subscription
from classes.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(course=obj, user=user, subscribed=True).exists()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = '__all__'

    def get_subscribed(self, obj):
        user = self.context['request'].user
        return obj.user == user and obj.subscribed
