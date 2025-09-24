import africastalking
from django.conf import settings

africastalking.initialize(username=settings.AT_USERNAME, api_key=settings.AT_API_KEY)
_sms = africastalking.SMS

def send_sms(phone, message):
    try:
        response = _sms.send(message, [phone])
        return response
    except Exception as e:
        # log
        return None
