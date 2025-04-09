from bs4 import BeautifulSoup
import pyotp
import requests
import urllib.parse
from dataclasses import dataclass


@dataclass
class LoginCredentials:
    registrar_id: str
    user_id: str
    password: str
    otp_secret: str


def post_login_url(input:str, base_url:str) -> str:
    soup = BeautifulSoup(input, 'html.parser') 
    form = soup.find("form")
    form_action = form.get("action")
    return urllib.parse.urljoin(base_url, form_action)


def find_export_download_url(input:str, base_url, export_name:str) -> str:
    soup = BeautifulSoup(input, 'html.parser')
    for a in soup.find_all("a"):
        span = a.find("span")
        if span and span.text.strip() == export_name:
            href = a.get("href")
            break
    else:
        raise Exception("Download link not found.")
    return urllib.parse.urljoin(base_url, href)


def save_file(file_content:bytes, file_name:str) -> None:
    with open(file_name, "wb") as f:
        f.write(file_content)
    print(f"✅ File saved as: {file_name}")


def download_export(session:requests.Session, download_url:str) -> bytes:
    file_response = session.get(download_url)
    return file_response.content


def login_to_page(session:requests.Session, login_url, loginCredentials:LoginCredentials, page):
    totp = pyotp.TOTP(loginCredentials.otp_secret)

    payload = {
        'userPass:agentId': loginCredentials.registrar_id, 
        'userPass:userId': loginCredentials.user_id, 
        'userPass:password': loginCredentials.password, 
        'userPass:otp': totp.now(),
        'dest': page
    }

    response = session.get(login_url)
    absolute_url = post_login_url(response.text, login_url)
    post_response = session.post(absolute_url, data=payload)
    return post_response


if __name__ == "__main__":
    LOGIN_URL = "LOGIN_URL_TO_DNSBELGIUM_REGISTRAR_PORTAL"
    CREDENTIALS = LoginCredentials(
        registrar_id="UPDATE_REGISTRAR_ID", 
        user_id="UPDATE_USER_ID", 
        password="UPDATE_PASSWORD_OF_USER",
        otp_secret="UPDATE_OTP_SECRETE_OF_USER"
    )
    

    session = requests.Session()
    #We need to set the sec-fetch-site header, otherwise we get redirected to the login page. 
    session.headers.update({
        "sec-fetch-site": "none"})
    
    view_export_page = login_to_page(
        session=session, 
        login_url=LOGIN_URL, 
        loginCredentials=CREDENTIALS, 
        page="view-export")
    
    download_url = find_export_download_url(
        input=view_export_page.text, 
        base_url=view_export_page.url, 
        export_name=f"{CREDENTIALS.registrar_id}_reg.csv")
    
    file_content = download_export(
        session=session, 
        download_url=download_url)

    save_file(
        file_content=file_content,
        file_name=f"{CREDENTIALS.registrar_id}_reg.csv")