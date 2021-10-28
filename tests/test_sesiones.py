from fitapp.apigoogle.sesiones import Sesiones, Oauth
from django.test import Client
from django.test import TestCase
import json


# class test_Oauth(TestCase):

    # def test_Oauth(self):
    #     c = Client()
    #     response = c.post('/google/')
    #     # assert response.status_code
    #     self.content = response.content
    #     assert 'hola'
        # oauth = Oauth(request)
        # sesion = Sesiones(Oauth)
        # assert sesion.getSession()

    # def test_Sesiones(self):
    #     response = self.client.get('http://127.0.0.1:8000')
    #     self.assertEqual(response.status_code, 200)


    # def test_Datasets(self):
        # sesion = Sesiones(Oauth)
        # ds = sesion.listDataSources()
        # print(ds)

