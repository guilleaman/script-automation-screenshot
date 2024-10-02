import os
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, quote

# Configurações
urls_file = 'urls.txt'  # Nome do arquivo texto contendo as URLs
output_folder = 'screenshots'  # Pasta para armazenar os prints
keyword = "sest"  # Palavra-chave a ser buscada

# Verifica se a pasta de saída existe, caso contrário, cria
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Lê as URLs do arquivo de texto
with open(urls_file, 'r') as file:
    urls = [line.strip() for line in file.readlines() if line.strip()]  # Remove linhas vazias

# Configurações do Selenium e do Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar o Chrome em modo headless
chrome_options.add_argument("--disable-gpu")  # Desativar a GPU para aumentar a compatibilidade
chrome_options.add_argument("--window-size=375,667")  # Tamanho da janela para simular um dispositivo móvel

# Inicia o driver do Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Itera sobre cada URL lida do arquivo
for index, url in enumerate(urls):
    # Codifica a URL para evitar erros
    encoded_url = quote(url, safe=":/?&=")  # Codifica a URL mantendo os caracteres válidos

    # Abre a URL no navegador
    driver.get(encoded_url)
    time.sleep(2)  # Aguarda o carregamento completo da página

    # Busca pela palavra-chave
    body = driver.find_element("tag name", "body")
    if keyword in body.text:
        print(f'Palavra-chave "{keyword}" encontrada na URL: {url}')

        # Captura a posição do elemento que contém a palavra-chave
        element = driver.find_element("xpath", f"//*[contains(text(), '{keyword}')]")

        # Define o nome do arquivo de saída
        screenshot_file = os.path.join(output_folder, f'screenshot_{index + 1}.png')

        # Tira o screenshot da tela inteira
        driver.save_screenshot(screenshot_file)

        # Carrega a imagem capturada
        image = Image.open(screenshot_file)
        draw = ImageDraw.Draw(image)

        # Define a fonte e o tamanho do texto
        try:
            # Tenta usar a fonte Arial
            font_path = "/Library/Fonts/Arial.ttf"  # Caminho para fontes no macOS
            font = ImageFont.truetype(font_path, size=20)  # Define tamanho da fonte como 20
        except IOError:
            font = ImageFont.load_default()  # Usa a fonte padrão se não encontrar

        text_color = (0, 0, 0)  # Cor do texto (preto)

        # Texto a ser adicionado no screenshot
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text = f"URL: {url}\nData e Hora: {current_time}"

        # Define a posição para adicionar o texto (canto superior esquerdo)
        text_position = (10, 10)

        # Adiciona o texto na imagem
        draw.text(text_position, text, fill=text_color, font=font)

        # Salva a imagem com o texto adicionado
        image.save(screenshot_file)
        print(f'Screenshot da palavra-chave "{keyword}" na URL: {url} salva como {screenshot_file}')

    else:
        print(f'Palavra-chave "{keyword}" não encontrada na URL: {url}')

# Fecha o navegador
driver.quit()
