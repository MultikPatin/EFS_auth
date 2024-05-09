import http
import json

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        url = settings.AUTH_API_LOGIN_URL
        payload = {"email": username, "password": password}
        response = requests.post(url, data=json.dumps(payload))
        print(response.status_code)
        if response.status_code != http.HTTPStatus.OK:
            return None
        data = response.json()
        try:
            user, created = User.objects.get_or_create(id=data["uuid"])
            print(user)
            # user.email = data.get("email")
            # print(user.email)
            # user.first_name = data.get("first_name")
            # print(user.first_name)
            # user.last_name = data.get("last_name")
            # print(user.first_name)
            # print(user.last_name)
            # user.role_uuid = data.get("role_uuid")
            # print(user.role_uuid)
            # user.is_superuser = data.get("is_superuser")
            # print(user.is_superuser)
            # user.is_stuff = data.get("is_superuser")
            # print(user.is_stuff)
            # user.save()
        except Exception as e:
            print(f"==> {e}")
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
