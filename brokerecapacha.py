import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import whisper

# Inicializar o navegador Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Acessar o site
    link = "https://sei.anp.gov.br/sei/modulos/pesquisa/md_pesq_processo_pesquisar.php?acao_externa=protocolo_pesquisar&acao_origem_externa=protocolo_pesquisar&id_orgao_acesso_externo=0"
    driver.get(link)
    driver.implicitly_wait(5)

    # Capturar o link do áudio do CAPTCHA
    try:
        # Localizar o elemento do CAPTCHA de áudio (se disponível)
        src = driver.find_element(By.XPATH, "//audio/source")
        link_audio = src.get_attribute("src")
        print("Link do áudio:", link_audio)
    except Exception as e:
        print("Erro ao capturar o link do áudio:", e)
        driver.quit()
        exit(1)

    # Configurar sessão Requests com cookies do Selenium
    session = requests.Session()
    cookies = driver.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Baixar o áudio
    audio_file_path = os.path.join(os.getcwd(), "audio.wav")
    try:
        response = session.get(link_audio, stream=True)
        response.raise_for_status()  # Verificar erros HTTP
        with open(audio_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Áudio convertido para WAV em:", audio_file_path)
    except Exception as e:
        print("Erro ao baixar o áudio:", e)
        driver.quit()
        exit(1)

    # Transcrever o áudio usando Whisper
    try:
        modelo = whisper.load_model("base")  # Carregar o modelo Whisper
        resposta = modelo.transcribe(audio_file_path, language="pt")
        print("Texto do CAPTCHA reconhecido:", resposta['text'])
    except Exception as e:
        print("Erro ao transcrever o áudio:", e)
        driver.quit()
        exit(1)

finally:
    # Fechar o navegador
    driver.quit()
