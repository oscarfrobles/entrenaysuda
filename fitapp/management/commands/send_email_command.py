from django.core.management.base import BaseCommand
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import re
from fitapp.operaciones import getUsers, checkNumEventsToday, getTodayIdEvent



class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        users = getUsers()
        for user in users:
            if False == self.checkEmail(user['email']):
                continue
            if checkNumEventsToday(user_id=user['id']) == 0:
                print("no hay eventos para hoy")
                return False
            sg = False
            url = "https://mimifit.herokuapp.com/entrenamientos/%d" % getTodayIdEvent(user_id=user['id'])
            message = Mail(
                from_email='oskijob@gmail.com',
                to_emails=user['email'],
                subject='Hoy tienes un nuevo reto que debes completar',
                html_content='Tu reto está en %s. Accede y <strong>termínalo</strong>' % url
            )
            try:
                sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
                response = sg.send(message)
                #print(response.status_code)
                #print(response.headers)
                #print(response.body)
            except Exception as e:
                print(e.message)
        return sg


    def checkEmail(self, email):
        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        comp = re.compile(pattern)
        if re.match(pattern, email):
            return True
        else:
            print("Invalid Email %s" % email)
            return False