import pytest
from fitapp.apigoogle.sesiones import Sesiones, Oauth
from django.test import Client
import json

class test_Oauth:

    def test_Oauth(self):
        c = Client()
        response = c.post('/google/')
        # assert response.status_code
        self.content = response.content.json()
        assert response.content.json()
        # oauth = Oauth(request)
        # sesion = Sesiones(Oauth)
        # assert sesion.getSession()

    def test_Sesiones(self):
        pass

