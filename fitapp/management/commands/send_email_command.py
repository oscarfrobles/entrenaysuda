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
            home = "https://mimifit.herokuapp.com/"
            url = "%s/entrenamientos/%d" % (home, getTodayIdEvent(user_id=user['id']) )

            message = Mail(
                from_email='oskijob@gmail.com',
                to_emails=user['email'],
                subject='Hola %s %s. Hoy tienes un nuevo reto que debes completar' % (user['first_name'], user['last_name']),
                html_content='Hola <strong><i>%s</i></strong>. <br/><br/> Tu nuevo reto está en %s. '
                             'Accede y <strong>termínalo</strong>'
                             '<br/><br/> Si al acceder tienes un error tienes que hacer login de nuevo '
                             'en %s y conectarte en login' % (user['username'], url, home)
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