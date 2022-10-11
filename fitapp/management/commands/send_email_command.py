from django.core.management.base import BaseCommand
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import re
from fitapp.operaciones import getUsers, checkNumEventsToday, getTodayIdEvent, getLastActiveIdEvent
import logging

logger = logging.getLogger()



class Command(BaseCommand):

    def add_arguments(self, parser):
        try:
            parser.add_argument(
                '--test',
                type=int,
                help='Executing test',
            )
        except Exception as e:
            print(str(e))

    def handle(self, *args, **kwargs):
        print(kwargs)
        if 1 == kwargs.get('test'):
            try:
                event_id, ejercicios = getLastActiveIdEvent(user_id=1)
                self.sendEmail(
                    username='testing',
                    user_id='1',
                    first_name='name testing',
                    last_name='surname testing',
                    email='juliancamarillo59@gmail.com',
                    event=event_id,
                    ejercicios=ejercicios
                )
            except Exception as e:
                print(e)
        else:
            users = getUsers()
            for user in users:
                if False == self.checkEmail(user['email']):
                    continue
                if checkNumEventsToday(user_id=user['id']) == 0:
                    print("no hay eventos para hoy")
                    return False
                try:
                    event_id, ejercicios = getTodayIdEvent(user_id=user['id'])
                    print(event_id)
                except Exception as e:
                    logger.error(str(e))
                    print(e)
                self.sendEmail(
                    username=user['username'],
                    user_id=user['id'],
                    first_name=user['first_name'],
                    last_name=user['last_name'],
                    email=user['email'],
                    event=event_id,
                    ejericios=ejercicios
                )
            return str(True)


    def sendEmail(self, **kwargs):
        email = kwargs.get('email')
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        username = kwargs.get('username')
        event = kwargs.get('event')
        ejercicios = kwargs.get('ejercicios')
        print(ejercicios)

        sg = False
        home = "https://mimifit.herokuapp.com"
        url = "%s/entrenamientos/%d" % (home, event)

        message = Mail(
            from_email='oskijob@gmail.com',
            to_emails=email,
            subject='Hola %s %s. Hoy tienes un nuevo reto que debes completar' % (
            first_name, last_name),
            html_content='Hola <strong><i>%s</i></strong>. <br/><br/> Tu nuevo reto está en <a href="%s" target="_blank">%s</a>. '
                         'Accede y <strong>termínalo</strong>'
                         '<br/><br/> Si al acceder tienes un error tienes que hacer login de nuevo '
                         'en <a href="%s" target="_blank">%s</a> y conectarte en login<br/><br/>'
                         'Debes realizar los siguientes ejericicios %s' % (
                         username, url, url, home, home, ejercicios)
        )
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
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