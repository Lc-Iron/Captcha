import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import whisper

# Configuração do ChromeDriver
service = Service(r"C:\Users\Lucass\Downloads\test\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)

try:
    # Acesse a página
    driver.get("https://sei.anp.gov.br/sei/modulos/pesquisa/md_pesq_processo_pesquisar.php?acao_externa=protocolo_pesquisar&acao_origem_externa=protocolo_pesquisar&id_orgao_acesso_externo=0")
    driver.implicitly_wait(2)

    # Captura o link de áudio
    src = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/form/div/div[2]/div[1]/div[2]/audio/source")
    link_audio = src.get_attribute("src")
    print("Link do áudio:", link_audio)

    # Baixa o áudio usando cookies do Selenium
    session = requests.Session()
    cookies = driver.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Caminho do arquivo de áudio
    audio_file_path = os.path.abspath(r"C:\Users\Lucass\Downloads\cody naty\audio.wav")
    response = session.get(link_audio, stream=True)

    if response.status_code == 200:
        with open(audio_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Áudio salvo em:", audio_file_path)

        # Verifica se o arquivo realmente existe
        if not os.path.exists(audio_file_path):
            print(f"Erro: O arquivo {audio_file_path} não foi encontrado.")
            exit(1)

        # Testa a abertura do arquivo antes de usar o Whisper
        try:
            with open(audio_file_path, 'rb') as f:
                print(f"Arquivo de áudio acessado com sucesso: {audio_file_path}")
        except Exception as e:
            print(f"Erro ao acessar o arquivo de áudio: {str(e)}")
            exit(1)

        # Transcrição com Whisper
        print("Tentando carregar o modelo Whisper...")
        modelo = whisper.load_model("base")
        print("Modelo Whisper carregado com sucesso.")

        print("Iniciando transcrição do áudio...")
        resposta = modelo.transcribe(audio_file_path, language="pt")
        print("Texto transcrito:", resposta['text'])

    else:
        print("Erro ao baixar o áudio. Status code:", response.status_code)

except Exception as e:
    print("Erro encontrado:", str(e))


# Removendo o fechamento automático temporariamente, só um teste
#finally:
    #driver.quit()

