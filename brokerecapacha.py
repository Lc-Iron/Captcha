<<<<<<< HEAD
import os  
import time  
import tempfile  
import shutil  
from selenium import webdriver  
from selenium.webdriver.edge.service import Service  
from selenium.webdriver.edge.webdriver import WebDriver  
from selenium.webdriver.common.by import By  
import requests  
import whisper  
import subprocess  
 
# Adiciona o caminho do FFmpeg ao PATH  
ffmpeg_path = r'C:\ffmpeg\bin' 
os.environ["PATH"] += os.pathsep + ffmpeg_path 
 
# Verifica se o FFmpeg está acessível 
try: 
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True) 
    print("FFmpeg version:", result.stdout.split('\n')[0]) 
except FileNotFoundError: 
    print("FFmpeg não encontrado no PATH. Verifique o caminho e a instalação.") 
    exit(1) 
 
# Configuração do EdgeDriver  
service = Service(r"c:\Users\FX4S\Downloads\Python\edgedriver_win64\msedgedriver.exe")  
driver = WebDriver(service=service)  
 
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
 
    # Caminho do arquivo de áudio (usando caminho absoluto)  
    audio_file_path = os.path.abspath(os.path.join(os.getcwd(), "audio.mp3"))  
    response = session.get(link_audio, stream=True)  
 
    if response.status_code == 200:  
        with open(audio_file_path, 'wb') as file:  
            for chunk in response.iter_content(chunk_size=8192):  
                file.write(chunk)  
        print("Áudio salvo em:", audio_file_path)  
 
        # Verifica se o arquivo realmente existe e seu tamanho  
        if os.path.exists(audio_file_path):  
            print(f"O arquivo foi criado com sucesso em {audio_file_path}")  
            print(f"Tamanho do arquivo: {os.path.getsize(audio_file_path)} bytes")  
            print(f"Permissões do arquivo: {oct(os.stat(audio_file_path).st_mode)[-3:]}")  
        else:  
            print(f"Erro: O arquivo {audio_file_path} não foi encontrado.")  
            exit(1)  
 
        # Copia o arquivo para um local temporário  
        temp_dir = tempfile.gettempdir()  
        temp_audio_path = os.path.join(temp_dir, "temp_audio.mp3")  
        shutil.copy2(audio_file_path, temp_audio_path)  
        print(f"Arquivo copiado para: {temp_audio_path}")  
 
        # Converte para WAV  
        wav_file_path = os.path.splitext(temp_audio_path)[0] + ".wav"  
        try: 
            subprocess.run(['ffmpeg', '-i', temp_audio_path, wav_file_path], check=True) 
            print(f"Arquivo convertido para WAV: {wav_file_path}") 
        except subprocess.CalledProcessError as e: 
            print(f"Erro ao converter o arquivo para WAV: {e}") 
            exit(1) 
 
        # Transcrição com Whisper  
        print("Tentando carregar o modelo Whisper...")  
        print(f"Versão do Whisper: {whisper.__version__}")  
        modelo = whisper.load_model("base")  
        print("Modelo Whisper carregado com sucesso.")  
 
        # Confirmação do caminho do arquivo antes da transcrição  
        if os.path.exists(wav_file_path):  
            print(f"Arquivo de áudio confirmado para transcrição: {wav_file_path}")  
            try:  
                # Adicionando um pequeno delay antes da transcrição  
                time.sleep(2)  
                print(f"Caminho do arquivo usado pelo Whisper: {os.path.abspath(wav_file_path)}")  
                resposta = modelo.transcribe(wav_file_path, language="pt")  
                print("Texto transcrito:", resposta['text'])  
            except Exception as e:  
                print(f"Erro durante a transcrição do áudio em {wav_file_path}: {e}")  
        else:  
            print(f"Erro: O arquivo de áudio {wav_file_path} não foi encontrado antes da transcrição.")  
    else:  
        print("Erro ao baixar o áudio. Status code:", response.status_code)  
 
except Exception as e:  
    print("Erro encontrado:", str(e))  
 
finally:  
    # Fechar o driver para evitar recursos abertos  
    driver.quit() 

=======
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

>>>>>>> df3bd18ec86ad99290a3a244fdc853458b4d66bc
