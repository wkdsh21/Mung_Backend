import json

from django.test import TestCase
from member.models import User

# Create your tests here.

class TestPwChService(TestCase):
    def test_you_can_change_password(self):
        # given
        test_user = User.objects.create_user(username='test', password='asdf1357')

        # when
        self.client.force_login(test_user)

        response = self.client.put(
            "/api/v1/users/pw_change",
            data={
                "old_password": "asdf1357", "new_password": "asdf1346"
            },
            content_type='application/json'
        )
        print(response.status_code)

        # then
        user = User.objects.get(username="test")
        self.assertTrue(user.check_password("asdf1346"))