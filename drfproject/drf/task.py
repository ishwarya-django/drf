from celery import shared_task


@shared_task(bind= True)
def test_func(self):

    for i in range(10):
        print(i)
    return "DONE"



from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from drfproject import settings
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def send_mail_func(self):
    # timezone.localtime(users.date_time) + timedelta(days=2)
    users = get_user_model().objects.all()
    for user in users:
        mail_subject = "Hi! Celery Testing"
        message = "If you are liking my content, please hit the like button and do subscribe to my channel"
        to_email = user.email
        send_mail(
            subject = mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "Done"