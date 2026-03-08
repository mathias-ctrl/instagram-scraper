from fastapi import FastAPI
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, parse_qs
import json
import re
import os

app = FastAPI()

PROXY = {
    "server": f"http://{os.environ['PROXY_HOST']}:80",
    "username": os.environ['PROXY_USER'],
    "password": os.environ['PROXY_PASS']
}

def capturar_foto_perfil(username):
    requisicoes = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy=PROXY,
            args=[
                '--no-sandbox',
                '--single-process',
                '--no-zygote',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        context.add_cookies([{
            "name": "sessionid",
            "value": os.environ['IG_SESSION'],
            "domain": ".instagram.com",
            "path": "/"
        }])
        page = context.new_page()

        def interceptar(route):
            url = route.request.url
            if route.request.method == "GET" and 'fna.fbcdn.net' in url:
                requisicoes.append(url)
            route.continue_()

        page.route("**/*", interceptar)
        page.goto(f"https://www.instagram.com/{username}/", wait_until='networkidle')
        page.wait_for_timeout(3000)
        html = page.content()
        browser.close()

    match = re.search(r'og:image" content="([^"]+)"', html)
    if not match:
        return None

    og_image = match.group(1).replace('&amp;', '&')
    params = parse_qs(urlparse(og_image).query)
    oe = params.get('oe', [None])[0]

    if not oe:
        return None

    for url in requisicoes:
        if f'oe={oe}' in url:
            return url

    return og_image


@app.get("/")
def root():
    return {"status": "ok", "uso": "/foto?usernames=conta1,conta2"}


@app.get("/foto")
def get_foto(usernames: str):
    lista = [u.strip().replace('@', '') for u in usernames.split(',') if u.strip()]
    resultado = {}
    for username in lista:
        resultado[username] = capturar_foto_perfil(username)
    return resultado


@app.get("/debug")
def debug(username: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy=PROXY,
            args=['--no-sandbox', '--single-process', '--no-zygote', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        context.add_cookies([{
            "name": "sessionid",
            "value": os.environ['IG_SESSION'],
            "domain": ".instagram.com",
            "path": "/"
        }])
        page = context.new_page()
        page.goto(f"https://www.instagram.com/{username}/", wait_until='networkidle')
        page.wait_for_timeout(3000)
        html = page.content()
        browser.close()
    return {"html_trecho": html[:3000]}


@app.get("/ip")
def check_ip():
    import requests
    r = requests.get(
        "https://ipv4.webshare.io/",
        proxies={
            "http": f"http://{os.environ['PROXY_USER']}:{os.environ['PROXY_PASS']}@{os.environ['PROXY_HOST']}:{os.environ['PROXY_PORT']}/",
            "https": f"http://{os.environ['PROXY_USER']}:{os.environ['PROXY_PASS']}@{os.environ['PROXY_HOST']}:{os.environ['PROXY_PORT']}/"
        }
    )
    return {"ip": r.text}
