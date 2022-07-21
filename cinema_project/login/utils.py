import datetime
import json
import requests
from django.conf import settings


def today() -> datetime.datetime:
    return datetime.datetime.today()


def next_days(days: int) -> datetime.datetime:
    now = today()
    return now + datetime.timedelta(days=days)


def send_contact_email(user_data: dict) -> None:
    response = requests.post(
        url=settings.SENDIN_BLUE["api_url"],
        headers={
            'content-type': 'application/json',
            'api-key': f'{settings.SENDIN_BLUE["api_key"]}'
        },
        data=json.dumps({
            "sender": {
              "name": "Cinema X ",
              "email": f"{user_data['email'].split('@')[0]}@test.com",
            },
            "to": [
                {
                    "email": "liviu.m.farcas@gmail.com",
                    "name": "Cinema X HQ"
                }
            ],
            "subject": user_data['subject'] or 'Message from Cinema X website',
            "htmlContent":
                f"<html><head></head><body><p>Hello,"
                f"</p>Received a new email from {user_data['name']},"
                f"<p> message: {user_data['message']}</p>"
                f"<p>Other contact details:</p>"
                f"<p>Phone number: {user_data['phone']}</p>"
                f"<p>City: {user_data['city']}</p>"
                f"<p>Cinema: {user_data['cinema']}</p>"
                f"</body></html>"
        })
    )
    print(f'Successfuly sent email with response: {response.content}')
