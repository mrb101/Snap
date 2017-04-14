import urllib
import urllib2
import requests
import json

from app.settings import API_KEY, API_SEC

def send_sms_notification(number, text):
    params = {
        'api_key': str(API_KEY),
        'api_secret': str(API_SEC),
        'from': '01137480800',
        'to': number,
        'text': text
    }
    url = 'https://rest.nexmo.com/sms/json?' + urllib.urlencode(params)
    req = urllib2.Request(url)
    req.add_header('Accept', 'application/json')
    res = urllib2.urlopen(req)
    if res.code == 200:
        data = res.read()
        decoded_res = json.loads(data.decode('utf-8'))
        messages = decoded_res["messages"]
        for message in messages:
            if message["status"] == "0":
                print("Success")
            else:
                print("Error {0}".format(res.code))


def send_email_notification(email, text):
    """ Sending an email using mailgun """
    URL = "https://api.mailgun.net/v3/sandboxedba71b9ee904dc5aab7a79a7492098b.mailgun.org/messages"
    params = {
        "from": "Cruz <postmaster@sandboxedba71b9ee904dc5aab7a79a7492098b.mailgun.org>",
        "to": [email,],
        "subject": "Cruz",
        "text": text
    }
    return requests.post(
        URL,
        auth=("api", str(API)),
        data=params
    )
