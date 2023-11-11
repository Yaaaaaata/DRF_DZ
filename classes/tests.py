from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from classes.models import Course, Lesson, Subscription, Payment
from classes.serializers import SubscriptionSerializer

User = get_user_model()


class ClassesCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@user.com', password='123')
        self.client.force_authenticate(user=self.user)
        self.user.set_password('123')
        self.user.save()

        self.course = Course.objects.create(title='TestCourse', description='TestCourse', owner=self.user)

        self.lesson = Lesson.objects.create(title='TestLesson', course=self.course, owner=self.user)

        self.subscription = Subscription.objects.create(course=self.course, user=self.user)

    def test_create_lesson(self):
        """"""

        url = reverse('classes:lesson-create')
        data = {
            'title': 'Test Lesson',
            'description': 'This is a test lesson'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Lesson')
        self.assertEqual(response.data['description'], 'This is a test lesson')

    def test_list_lesson(self):
        """"""

        response = self.client.get(reverse('classes:lesson-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.id,
                        "title": "TestLesson",
                        "description": "",
                        "preview": None,
                        "video_link": None,
                        "owner": self.user.id
                    },
                ]
            }
        )

    def test_update_lesson(self):
        """"""
        permission = Permission.objects.get(codename='change_lesson')
        self.user.user_permissions.add(permission)

        url = reverse('classes:lesson-update', args=[self.lesson.id])
        data = {
            'title': 'Updated Lesson'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'TestLesson')

    def test_retrieve_lesson(self):
        """"""

        url = reverse('classes:lesson-get', kwargs={'pk': self.lesson.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'title': 'TestLesson',
                'description': "",
                "preview": None,
                "video_link": None,
                "owner": self.user.id
            }
        )

    def test_delete_lesson(self):
        """"""

        response = self.client.delete(reverse('classes:lesson-delete', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.all().exists())


class PaymentListAPIViewTest(APITestCase):
    """"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@user.com', password='123')
        self.client.force_authenticate(user=self.user)
        self.user.set_password('123')
        self.user.save()

        self.course = Course.objects.create(title='TestCourse', description='TestCourse', owner=self.user)

        self.lesson = Lesson.objects.create(title='TestLesson', course=self.course, owner=self.user)

        self.subscription = Subscription.objects.create(course=self.course, user=self.user)

        self.url = reverse('classes:payment-list')

    def test_get_payment_list(self):
        payment = Payment.objects.create(amount=10, user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]['amount']), payment.amount)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@user.com', is_active=True, password='123')
        self.client.force_authenticate(user=self.user)
        self.user.set_password('123')
        self.user.save()

        self.course = Course.objects.create(title='TestCourse', description='TestCourse', owner=self.user)
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)

    def test_create_subscription(self):
        data = {
            'course_id': self.course.id,
        }

        response = self.client.post(reverse('classes:sub-create', kwargs={'course_id': self.course.id}), data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {
                'id': response.json()['id'],
                'course': self.course.id,
                'user': self.user.id,
                'subscribed': True,
            }
        )

    def test_delete_subscription(self):
        response = self.client.delete(reverse('classes:sub-delete', kwargs={'pk': self.subscription.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.all().exists())


