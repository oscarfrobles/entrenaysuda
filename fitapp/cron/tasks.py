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

def call_send_email_command(**kwargs):
    return call_command('send_email_command')


''' 
Copia un calendario de ejercicios para el día de hoy para todos los usuarios cogiendo
el evento de 7 días atrás si existe o el último de no existir
'''
def call_day_calendar_command(**kwargs):
    return call_command('copy_day_calendar_command')
