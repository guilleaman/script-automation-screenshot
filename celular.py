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
output_folder = 'screenshots-celular'  # Pasta para armazenar os prints

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
chrome_options.add_argument("--window-size=375x812")  # Definir tamanho da janela para celular

# Simular user-agent de um dispositivo móvel (iPhone X)
mobile_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"
chrome_options.add_argument(f"user-agent={mobile_user_agent}")

# Inicia o driver do Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Itera sobre cada URL lida do arquivo
for index, url in enumerate(urls):
    # Codifica a URL para evitar erros
    encoded_url = quote(url, safe=":/?&=")  # Codifica a URL mantendo os caracteres válidos

    # Abre a URL no navegador
    driver.get(encoded_url)
    time.sleep(4)  # Aguarda o carregamento completo da página

    # Define o nome do arquivo de saída
    screenshot_file = os.path.join(output_folder, f'screenshot_{index + 1}.png')

    # Tira o print da página
    driver.save_screenshot(screenshot_file)
    print(f'Screenshot da URL {url} salva como {screenshot_file}')

    # Adiciona data, hora e URL no screenshot
    # Carrega a imagem capturada
    image = Image.open(screenshot_file)
    draw = ImageDraw.Draw(image)

    # Define a fonte padrão e a cor do texto
    font = ImageFont.load_default()  # Usar a fonte padrão
    text_color = (240, 0, 0)  # Cor do texto (vermelho)

    # Extrai a parte da URL até o primeiro '/'
    parsed_url = urlparse(url)
    short_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Texto a ser adicionado no screenshot
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    text = f"URL: {short_url}\nData e Hora: {current_time}"

    # Define a posição para adicionar o texto (canto superior esquerdo)
    text_position = (10, 10)

    # Adiciona o texto na imagem
    draw.text(text_position, text, fill=text_color, font=font)

    # Salva a imagem com o texto adicionado
    image.save(screenshot_file)
    print(f'Informações de data, hora e URL adicionadas ao screenshot: {screenshot_file}')

# Fecha o navegador
driver.quit()
