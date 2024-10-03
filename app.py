import os
import time
import pyautogui  # Usado para captura de tela completa
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import sys

# Obtém o diretório do executável
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # Diretório temporário para o executável
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # Diretório do script

# Configurações
urls_file = os.path.join(base_path, 'urls.txt')  # Caminho para urls.txt
output_folder = os.path.join(base_path, 'screenshots')  # Caminho completo para a pasta de screenshots

# Verifica se a pasta de saída existe, caso contrário, cria
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Lê as URLs do arquivo de texto
with open(urls_file, 'r') as file:
    urls = [line.strip() for line in file.readlines() if line.strip()]  # Remove linhas vazias

# Configurações do Selenium e do Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Inicia o navegador maximizado para capturar a tela toda
chrome_options.add_argument("--disable-gpu")  # Desativar a GPU para aumentar a compatibilidade

# Inicia o driver do Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Itera sobre cada URL lida do arquivo
for index, url in enumerate(urls):
    # Abre a URL completa no navegador
    driver.get(url)
    time.sleep(8)  # Aguarda o carregamento completo da página

    # Obtém apenas a URL base (protocolo + domínio)
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"

    # Executa JavaScript para substituir a URL na barra de endereço do navegador sem recarregar a página
    script = f"window.history.pushState('', '', '{base_url}');"
    driver.execute_script(script)

    # Tira o print da tela inteira com a URL simplificada visível na barra de endereço
    screenshot_file = os.path.join(output_folder, f'screenshot_full_{index + 1}.png')
    screenshot = pyautogui.screenshot()  # Captura a tela inteira
    screenshot.save(screenshot_file)
    print(f'Screenshot da tela inteira salva como {screenshot_file} para a URL base {base_url}')

# Fecha o navegador
driver.quit()
