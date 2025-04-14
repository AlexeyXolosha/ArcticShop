from django.test import TestCase
from django.urls import reverse

from users.models import User
# Create your tests here.

class IndexViewTests(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        print(response)

        print("Users: ", User.objects.all())

