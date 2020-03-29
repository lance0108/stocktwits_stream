from crendentials import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    REDIRECT_URI,
    SCOPE
)
import requests
from pprint import pprint

"""
How to obtain access token?
0. Define your API credentials in the credential.py file.
1. Run the main method.
2. Paste the authorization URL into your browser. Click Connect if prompted.
3. After redirected, the authorization code should be shown in the URL of the page.
4. Input the authorzation code to the console.
5. Based on the outputs from the console, manually update the ACCESS_TOKEN constant in credentials.py.  
"""


def get_authorization_url():
    return "".join([
        "https://api.stocktwits.com/api/2/oauth/authorize?",
        f"client_id={CONSUMER_KEY}&",
        f"client_secreted={CONSUMER_SECRET}&",
        f"redirect_uri={REDIRECT_URI}&",
        f"scope={SCOPE}&",
        "response_type=code"
    ])


def get_access_token(auth_code):
    url = "https://api.stocktwits.com/api/2/oauth/token"
    params = {
        "client_id": CONSUMER_KEY,
        "client_secret": CONSUMER_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": "http://www.google.com",
        "code": auth_code
    }
    response = requests.post(url, params=params)
    return response.json()


if __name__ == "__main__":
    print("Paste the following authorization URL into your browser:")
    print(get_authorization_url())
    authorization_code = input("Enter the authorzation code:")
    pprint(get_access_token(authorization_code))
