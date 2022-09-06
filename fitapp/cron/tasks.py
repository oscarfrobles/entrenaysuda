# pylint: disable=E1101
from django.core.management import call_command
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import environ
from fitapp.operaciones import checkCalendarToday

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

def call_hello_world_command(**kwargs):
    sg = False
    message = Mail(
        from_email='oskijob@gmail.com',
        to_emails='juliancamarillo59@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    return sg

''' 
Copia un calendario de ejercicios para el día de hoy para todos los usuarios cogiendo
el evento de 7 días atrás si existe o el último de no existir
'''
def copy_day_calendar_command(**kwargs):
    return str(checkCalendarToday())