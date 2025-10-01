import africastalking
from django.conf import settings

africastalking.initialize(username=settings.AT_USERNAME, api_key=settings.AT_API_KEY)
_sms = africastalking.SMS


def send_sms(phone, message):
    """
    Send an SMS message to a specified phone number using Africa's Talking API.

    Args:
        phone (str): The recipient's phone number in international format.
        message (str): The text message to be sent.

    Returns:
        dict | None: A response dictionary from Africa's Talking API if successful,
        otherwise None if an exception occurs.
    """
    try:
        response = _sms.send(message, [phone])
        return response
    except Exception:
        return None
