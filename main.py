from fastapi import FastAPI
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, parse_qs
import re

app = FastAPI()

def capturar_foto_perfil(username):
    requisicoes = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--single-process',
                '--no-zygote',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
            ]
        )
        page = browser.new_page()

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


@app.get("/foto")
def get_foto(usernames: str):
    """
    ?usernames=conta1,conta2,conta3
    """
    lista = [u.strip().replace('@', '') for u in usernames.split(',') if u.strip()]
    resultado = {}
    for username in lista:
        resultado[username] = capturar_foto_perfil(username)
    return resultado

