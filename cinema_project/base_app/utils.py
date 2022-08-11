import csv
import datetime
import json
import requests

from django.conf import settings


def today() -> datetime.datetime:
    return datetime.datetime.today()


def next_days(days: int) -> datetime.datetime:
    now = today()
    return now + datetime.timedelta(days=days)


def send_email(
        from_email: str,
        html_content: str,
        subject: str = '',
        to_email: str = settings.CONTACT_EMAIL,
):
    response = requests.post(
        url=settings.SENDIN_BLUE["api_url"],
        headers={
            'content-type': 'application/json',
            'api-key': f'{settings.SENDIN_BLUE["api_key"]}'
        },
        data=json.dumps({
            "sender": {"name": "Cinema X ",
                        "email": f"{from_email.split('@')[0]}@test.com"},
            "to": [{"email": f"{to_email}",
                    "name": "Cinema X HQ"}],
            "subject": subject or 'Message from Cinema X website',
            "htmlContent":
                f"<html><head></head><body>{html_content}</body></html>"
        })
    )
    print(f'Successfully sent email with response: {response.content}')


def fetch_from_csv(file_name) -> list[dict]:
    with open(f'static/{file_name}.csv', 'r', encoding='utf-8') as f:
        rows = csv.DictReader(f)
        return [dict(row) for row in rows]


def thirty_minutes_ahead() -> datetime.datetime:
    return today() + datetime.timedelta(minutes=30)
