###################################################################################################
# Desenvolvido por 
# Israel Kraisch - Analista de TI - israel.kraisch@gmail.com
# Ricardo Dias Lemos dos Santos - Programador
# Este codigo fonte foi criado usando inteligencia artificial em sua construção.
# 16/01/2026
# SECRETARIA DE SAUDE  DE JOINVILLE-SC
# 
# Comandos para compilação
# pip install pyinstaller
# pyinstaller --onefile --windowed --icon=IMG/AIH-PRONT.ico --clean --noupx --hidden-import=openpyxl RPA-AIH-SISREG-HOSPv7.2.py
# Verfica Obito
# Regras Eletivas e Urgencia Externalizadas - configh.txt cnes
# Regras Externalizadas de Proxy e Webhook  - configh.txt settings
###################################################################################################
import os
import re
import pandas as pd
import tkinter as tk
import sys
import requests
import getpass
import ctypes
from ctypes import wintypes, byref
import os
from tkinter import Tk, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from pathlib import Path
from openpyxl import load_workbook
import configparser
# from statistics import mean
import time
from datetime import timedelta, datetime
# Importações adicionais para encriptação e leitura do binário
import pickle
from cryptography.fernet import Fernet, InvalidToken

# Declarar log_content como global
# Esta variável global armazena o conteúdo do log para envio posterior ao Google Chat.
global log_content
log_content = ""

# Mapeamento de caráter SISREG
CARATER_ELETIVO   = '10'
CARATER_URGENCIA  = '11'   # ou '02' em alguns fluxos, mas no seu código é 11

# Mapeamento de risco / prioridade
RISCO_ELETIVO     = '2'    # ou '2' — comum em eletivo (amarelo ou verde)
RISCO_URGENCIA    = '1'    # prioridade alta (vermelho/amarelo)

WEBHOOK_URL_DEFAULT = " "

def get_full_username():
    try:
        advapi32 = ctypes.WinDLL('secur32', use_last_error=True)
        GetUserNameEx = advapi32.GetUserNameExW
        NameDisplay = 3  # NameDisplay
        buffer_size = wintypes.DWORD(0)
        GetUserNameEx(NameDisplay, None, byref(buffer_size))
        buffer = ctypes.create_unicode_buffer(buffer_size.value)
        if GetUserNameEx(NameDisplay, buffer, byref(buffer_size)):
            return buffer.value.strip()
        else:
            raise ctypes.WinError(ctypes.get_last_error())
    except Exception as e:
        return f"Erro ao obter nome completo: {str(e)}"


USUARIO_LOGADO = getpass.getuser()
NOME_COMPLETO  = get_full_username()

OPERADOR = f"{USUARIO_LOGADO} – {NOME_COMPLETO}"

# Registra data/hora de início real da execução
INICIO_EXECUCAO = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
NOVA_EXECUCAO = {
    "operador": OPERADOR,
    "ultimaExecucao": datetime.now().isoformat(),   # formato ISO 8601
    "maquina": os.environ.get("COMPUTERNAME", "desconhecido"),
    "script": os.path.basename(__file__)
}

def mostrar_mensagem(mensagem):
    """Exibe uma mensagem de alerta para o usuário usando Tkinter"""
    # Cria uma janela Tkinter oculta e exibe uma caixa de mensagem com a informação fornecida.
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    root.attributes("-topmost", True)  # Garante que fique acima de tudo
    messagebox.showinfo("Aviso", mensagem)
    root.destroy()

def salvar_arquivo_excel(caminho_arquivo_xlsx, df):
    """
    Atualiza os dados no arquivo Excel sem perder formatações, filtros ou proteções.
    """
    # Carrega o workbook existente do arquivo Excel.
    workbook = load_workbook(caminho_arquivo_xlsx)
    sheet = workbook.active  # Supondo que a planilha a ser modificada é a ativa

    # Atualiza as células da planilha com os dados do DataFrame, começando da linha 2 (após o cabeçalho).
    for row_idx, row_data in enumerate(df.itertuples(index=False), start=2):  # Começa na linha 2 (ignorando cabeçalho)
        for col_idx, value in enumerate(row_data, start=1):
            cell = sheet.cell(row=row_idx, column=col_idx)
            cell.value = value

    # Salva as alterações no arquivo Excel e fecha o workbook.
    workbook.save(caminho_arquivo_xlsx)
    workbook.close()


# Função para carregar dados do Excel
def carregar_dados_excel(diretorio):
    # Lista todos os arquivos .xlsx no diretório fornecido.
    arquivos_xlsx = [f for f in os.listdir(diretorio) if f.endswith('.xlsx')]
    if not arquivos_xlsx:
        print("Nenhum arquivo .xlsx encontrado na pasta REGISTROS.")
        return None

    # Seleciona o arquivo mais recente com base na data de modificação.
    nome_arquivo_xlsx = max(arquivos_xlsx, key=lambda f: os.path.getmtime(os.path.join(diretorio, f)))
    print(f"Arquivo mais recente encontrado: {nome_arquivo_xlsx}")
    # Carrega o arquivo Excel em um DataFrame pandas.
    df = pd.read_excel(os.path.join(diretorio, nome_arquivo_xlsx))
    return nome_arquivo_xlsx, df
     
      

# Função para realizar o login no Sisreg
def realizar_login(navegador, usuario, senha):
    # Tenta localizar e preencher os campos de usuário e senha no formulário de login.
    # Nota SISREG: O login é obrigatório e verifica credenciais vinculadas ao CNES do estabelecimento.
    # Regra oficial: Usuários devem ter perfil de regulador ou solicitante hospitalar para acessar módulos de AIH.
    try:
        usuario_input = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, 'usuario')))
        usuario_input.send_keys(usuario)
        senha_input = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, 'senha')))
        senha_input.send_keys(senha)
        botao_login = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.NAME, 'entrar')))
        botao_login.click()
    except TimeoutException:
        print("Erro: Login falhou. Elemento de login não encontrado.")
        return False
    return True

# Função para iniciar o navegador com ou sem interface gráfica
def iniciar_navegador(headless=True):
    # Configura as opções do Chrome, incluindo modo headless se especificado.
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")  # Utiliza o novo modo headless
    else:
        chrome_options.add_argument("--start-maximized")  # Inicia o navegador maximizado
    
    # Adiciona opções para estabilizar o navegador e suprimir logs desnecessários.
    chrome_options.add_argument('--log-level=1')  # Define o nível de log para suprimir mensagens informativas
    chrome_options.add_argument('--no-sandbox')  # Evitar problemas em alguns ambientes
    chrome_options.add_argument('--disable-dev-shm-usage')  # Evitar problemas de memória
    chrome_options.add_argument('--disable-gpu')  # Desabilitar GPU (útil em headless)
    chrome_options.add_argument('--disable-extensions')  # Desabilitar extensões
    chrome_options.add_argument('--window-size=1920,1080')  # Definir tamanho da janela
    chrome_options.add_argument('--disable-blink-features=AutomationControlled') # Evita alguns fingerprints comuns
    # Remove a barra de "Chrome está sendo controlado por..."
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # Opcional: esconde também a extensão de automação (ajuda em alguns casos)
    #chrome_options.add_experimental_option('useAutomationExtension', False)

    # Inicializa o serviço do ChromeDriver e cria uma instância do navegador.
    service = Service('./CONFIG/chromedriver.exe')
    navegador = webdriver.Chrome(service=service, options=chrome_options)
    
    # Define um timeout para o carregamento de páginas.
    navegador.set_page_load_timeout(30)  # Timeout de 30 segundos
    
    return navegador


# Função principal de automação
def processar_automacao(df, usuario, senha, headless=False):

    # Cria diretórios para logs se não existirem.
    os.makedirs("LOGS", exist_ok=True)      
    os.makedirs("LOGS/AUTOMACAO", exist_ok=True)
          
    # Gera um nome de arquivo de log baseado na data e hora atuais.
    log_filename = f"LOGS/AUTOMACAO/automacao_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    log_file = open(log_filename, "w", encoding="utf-8")

    # Cria uma classe para redirecionar a saída padrão e de erro para o arquivo de log e acumular em log_content.
    class LogRedirector:
        def __init__(self, file):
            self.file = file
            self.buffer = []

        def write(self, message):
            self.file.write(message)
            self.buffer.append(message)
            global log_content
            log_content = "".join(self.buffer)

        def flush(self):
            self.file.flush()

    # Redireciona stdout e stderr para o LogRedirector.
    log_redirector = LogRedirector(log_file)
    sys.stdout = log_redirector
    sys.stderr = log_redirector

    print(f"Arquivo aberto para execução: {nome_arquivo_xlsx}")

    # Captura o horário de início da execução e imprime no log.
    hora_inicio = datetime.now()
    print(f"\n🟢 Início da execução: {hora_inicio.strftime('%d/%m/%Y  -  %H:%M:%S')}\n")
    # Opcional: já loga no console/início do robô
    print(f"▶ Iniciando RPA-AIH-SISREG-HOSP V7.2 ")
    print(f"   Operador ...: {OPERADOR}")
    print(f"   Início .....: {INICIO_EXECUCAO}")
    print(f"   Máquina ....: {NOVA_EXECUCAO['maquina']}")
    print("-" * 60)
    print(f"Iniciando processamento - Log salvo em: {log_filename}\n")
       
    # Inicializa o navegador Selenium.
    navegador = iniciar_navegador(headless)
    navegador.get('https://sisregiii.saude.gov.br/')

    
# Verifica o login; se falhar, encerra a automação.
# Nota SISREG: Login obrigatório; sistema valida usuário contra base nacional. Falha pode indicar credenciais inválidas ou problemas de rede.
    if not realizar_login(navegador, usuario, senha):
        print("Falha no login. Encerrando a automação...")
        navegador.quit()
        log_file.close()
        raise Exception("Falha no login. Verifique as credenciais e a conexão com o Sisreg.")    
    
    # Valida as colunas necessárias no DataFrame.
    # Nota SISREG: Colunas como 'nr_cns' e 'nu_consulta' são essenciais; CNS deve ser válido (15 dígitos, checksum correto).
    if not {'nr_cns', 'nu_consulta', 'auditado'}.issubset(df.columns):
        raise ValueError("A planilha Excel está faltando colunas necessárias: 'nr_cns', 'nu_consulta', 'auditado'")

    print("Iniciando processamento de registros...")

    # Carrega o arquivo de config no início (após carregar df e antes do loop while)
    caminho_config = "./CONFIG/configh.txt"  # Ajuste o path se necessário
    config = configparser.ConfigParser()
    if os.path.exists(caminho_config):
        config.read(caminho_config, encoding="utf-8")
        global_section = config['GERAL']
        # Lista de códigos que exigem CID 000
        codigos_multiplas_str = global_section.get('procedimentos_multiplas_cirurgias', '')
        codigos_multiplas = [c.strip() for c in codigos_multiplas_str.split(',') if c.strip()]
        print(f"Procedimentos configurados para CID INEXISTENTE (multiplas cirurgias/politrauma): {codigos_multiplas}")
        print(f"Configurações carregadas de {caminho_config}")
        # URL de webhook adicional do arquivo de config (opcional)
        WEBHOOK_URL_ADDITIONAL = config.get('settings', 'webhook_url', fallback=None)
        
        # Agora, leia o código IBGE/central da unidade do configh.txt (assumindo que está em 'settings' como 'ibge_central')
        ibge_central = config.get('settings', 'ibge_central', fallback=None)  # Ex: '420910' para Joinville
        if not ibge_central:
            raise ValueError("Código IBGE/central da unidade não encontrado no configh.txt! Adicione em [settings] ibge_central=420910")
        
        # Proxies externalizados do arquivo de config (com fallback para vazio se não configurado)
        proxies = {}
        if 'settings' in config:
            proxies = {
                "http": config.get('settings', 'proxies_http', fallback=None),
                "https": config.get('settings', 'proxies_https', fallback=None)
                }
        # Remove entradas None para evitar erros
            proxies = {k: v for k, v in proxies.items() if v is not None}
        
        
    else:
        print(f"Arquivo de config não encontrado: {caminho_config}. Usando defaults.")

     # Nova parte: Carregar webhooks do arquivo binário encriptado
    # Carregue a chave secreta de forma segura (ex: var de ambiente)
    chave_secreta = "Ne-SONoEq58rWn9Fi4DLKSUXdnQyzns03yI-HKcXJw0="  # Defina no ambiente: export CHAVE_WEBHOOK='sua_chave_base64'
    if not chave_secreta:
        raise ValueError("Chave secreta não encontrada! Defina a var de ambiente CHAVE_WEBHOOK.")

    # Caminho do arquivo binário
    caminho_binario = './CONFIG/configh_secure.bin'

    # Leia e decifre
    try:
        with open(caminho_binario, 'rb') as f:
            dados_encriptados = f.read()

        fernet = Fernet(chave_secreta.encode())  # Encode para bytes
        dados_serializados = fernet.decrypt(dados_encriptados)
        webhook_configs = pickle.loads(dados_serializados)

        # Agora pegue o webhook específico para a central/IBGE atual
        if ibge_central in webhook_configs:
            WEBHOOK_URL_ADDITIONAL = webhook_configs[ibge_central]['webhook']
            #print(f"Webhook carregado para central {ibge_central}: {WEBHOOK_URL_ADDITIONAL}")
        else:
            print(f"Aviso: Nenhum webhook encontrado para central {ibge_central}. Usando apenas default.")
            WEBHOOK_URL_ADDITIONAL = None

    except InvalidToken:
        raise ValueError("Chave secreta inválida! Não foi possível decifrar.")
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo binário de webhooks não encontrado!")
    except Exception as e:
        raise RuntimeError(f"Erro ao ler webhooks encriptados: {str(e)}")

    timestamps_execucao = {}  # Armazena os timestamps dos registros processados
    hospitais_processados = set()  #Rastreia hospitais usados na execução

    # Converte colunas específicas para tipos apropriados para consistência.
    df['ds_concat'] = df['ds_concat'].astype('object')
    df['ds_motivo'] = df['ds_motivo'].astype('object')
    df['nr_cns'] = df['nr_cns'].fillna(0).astype(float).astype(int).astype(str)
    df['cpf_solicitante'] = df['cpf_solicitante'].fillna('0').astype(str).str.zfill(11)

    # Loop principal para processar registros onde 'auditado' == 1.
    while (df['auditado'] == 1).any():
        for i, registro in df[df['auditado'] == 1].iterrows():

            tempo_inicio = datetime.now()
            timestamp_execucao = datetime.now().strftime("%H:%M:%S")
            timestamps_execucao[i] = timestamp_execucao  # Salva na memória o índice e o timestamp
            
            try:
                linha_arquivo = registro.name + 1

                # Ignora registros sem 'nu_consulta'.
                # Nota SISREG: 'nu_consulta' refere-se a consulta ambulatorial prévia; obrigatória para internações eletivas.                                                                                                                 
                if pd.isna(registro.get('nu_consulta', None)):
                    print(f"Registro {linha_arquivo} ignorado: nu_consulta não está presente.")
                    df.at[i, 'auditado'] = 0  
                    continue

                print(f"\n Processando registro {linha_arquivo} com nu_consulta {int(registro['nu_consulta'])}")
                df.at[i, 'auditado'] = 0

                # Verifica o estado do navegador antes de acessar a URL.
                print("Verificando estado do navegador antes de acessar a URL...")
                
                try:
                    navegador.title  # Testar se o navegador está funcional
                    print("Navegador está funcional.")
                except WebDriverException as e:
                    print(f"Navegador não está funcional: {str(e)}")
                    df.at[i, 'auditado'] = 2
                    df.at[i, 'ds_motivo'] = f"Erro no navegador: {str(e)}"
                    df.at[i, 'timestamp_execucao'] = timestamp_execucao
                    salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)
                    continue  # Pula o registro se navegador falhar                
                                                                                                
                # Acessa a URL para marcar internação hospitalar.
                print("Acessando a URL do Sisreg para marcar internação...")
                try:
                    navegador.get('https://sisregiii.saude.gov.br/cgi-bin/cadweb50?url=/cgi-bin/marcar_ih')
                    print("URL acessada com sucesso.")
                except Exception as e:
                    print(f"Erro ao acessar a URL: {str(e)}")
                    df.at[i, 'auditado'] = 2
                    df.at[i, 'ds_motivo'] = f"Erro ao acessar URL: {str(e)}"
                    df.at[i, 'timestamp_execucao'] = timestamp_execucao
                    salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)
                    continue
                # Tenta recarregar a página em caso de erro.
                print("Tentando recarregar a página...")
                try:
                    navegador.get('https://sisregiii.saude.gov.br/')
                    navegador.get('https://sisregiii.saude.gov.br/cgi-bin/cadweb50?url=/cgi-bin/marcar_ih')
                    print("URL recarregada com sucesso.")
                except Exception as e2:
                        print(f"Falha ao recarregar a URL: {str(e2)}")
                        raise Exception("Não foi possível acessar a URL após tentativa de recarga.")

                # Obtém o texto do corpo da página para depuração (desabilitado por padrão).
                #print("Estado da página após acessar a URL:")
                try:
                    body_text = navegador.find_element(By.TAG_NAME, 'body').text
                    #print(f"Conteúdo da página (primeiros 100 caracteres): {body_text[:100]}")
                except Exception as e:
                    print(f"Erro ao obter o conteúdo da página: {str(e)}")

                nu_consulta = str(int(registro['nu_consulta'])) if not pd.isna(registro['nu_consulta']) else ''
                df.at[i, 'ds_concat'] = f"Consulta Ambulatorial de Origem nº: {nu_consulta}\n{registro.get('ds_cond_just_internacao', '')}"
                
                nr_cns = str(df.loc[i, "nr_cns"])
                nu_cns = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.NAME, 'nu_cns'))
                )
                nu_cns.clear()
                nu_cns.send_keys(nr_cns)
                print(f"Registro {i + 1} ({nr_cns}) preenchido com sucesso.")

                btn_pesquisar = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.NAME, 'btn_pesquisar'))
                )
                btn_pesquisar.click()            

                # Tratamento de alertas no navegador.
                # Nota SISREG: Alertas podem indicar CNS inválido (regra oficial: CNS deve ser válido e sem óbito associado).                                                                                                                
                try:
                    alert = WebDriverWait(navegador, 5).until(EC.alert_is_present())
                    alert_text = alert.text
                    print(f"Alerta encontrado: {alert_text}")

                    if "O CNS informado nao e valido." in alert_text:
                        raise CNSInvalidoException(f"Erro no CNS: {alert_text}") 

                    alert.accept()
                    df.at[i, 'auditado'] = 2
                    df.at[i, 'ds_motivo'] = alert_text
                    df.at[i, 'timestamp_execucao'] = timestamp_execucao
                    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
                    continue
                except TimeoutException:
                    pass  # Se não houver alerta, continua normalmente

                try:
                # Obtém o texto do corpo da página após a pesquisa.
                    body_text = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body'))
                     ).text

                
                    verificar_cns(nr_cns, body_text)
                except TimeoutException as e:
            # Captura timeout no body_text
                    print(f"Timeout ao carregar body da página: {str(e)}")
                    df.at[i, 'auditado'] = 2
                    df.at[i, 'ds_motivo'] = f"Timeout ao carregar página após pesquisa de CNS: {str(e)}"
                    df.at[i, 'timestamp_execucao'] = timestamp_execucao
                    salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)
                    continue

                except CNSInvalidoException as e:
                    print(f"Erro no CNS para registro:{linha_arquivo} {e}")
                    df.at[i, 'auditado'] = 2
                    df.at[i, 'ds_motivo'] = str(e)
                    df.at[i, 'timestamp_execucao'] = timestamp_execucao
                    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
                    salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)
                    continue
            
            except Exception as e:  # Captura outras exceções inesperadas aqui também
                print(f"Erro inesperado ao verificar CNS/body: {str(e)}")
                df.at[i, 'auditado'] = 2
                df.at[i, 'ds_motivo'] = f"Erro ao verificar CNS: {str(e)}"
                df.at[i, 'timestamp_execucao'] = timestamp_execucao
                salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)
                continue

                # A validação de residência e moradia foi desabilitada conforme solicitação.
                # Nota SISREG: Oficialmente, o sistema verifica se o paciente reside no município regulador (ex.: Joinville-SC).
                # Regra oficial: Bloqueio se residência não for compatível com a central reguladora (Portaria GM/MS nº 1.559/2008).
                # Para tipos de moradia como Nômade, Cigano ou Morador de Rua, o SISREG rejeita automaticamente solicitações eletivas,
                # pois exige residência fixa para vínculo com a rede SUS local.
                # if not verificar_residencia(nr_cns, registro, body_text, df, i, timestamp_execucao):
                #     continue

            print(f"Pesquisa bem-sucedida! Número do Registro: {nr_cns}")


            btn_continuar = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.NAME, 'btn_continuar'))
                )                                        
            btn_continuar.click()

            # Seção para preenchimento de solicitação hospitalar.
            try:
                # Preenche o código do procedimento solicitado.
                # Nota SISREG: O procedimento deve estar habilitado no SIGTAP para o CNES executor.
                # Regra oficial: Sistema verifica habilitação após "Checar"; se não habilitado, alerta e bloqueio.
                                # Seção para preenchimento de solicitação hospitalar.
                try:
                    # Preenche o código do procedimento solicitado
                    cod_proc_solicitado = str(df.loc[i, "cod_proc_solicitado"]).zfill(10)
                    cod_proc_sol = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.NAME, 'pih'))
                    )
                    print(f"Código Procedimento Solicitado: '{cod_proc_solicitado}'")
                    cod_proc_sol.send_keys(cod_proc_solicitado)

                    # Clica em "Checar" para validar o procedimento
                    bnt_checar = WebDriverWait(navegador, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@value='Checar']"))
                    )
                    bnt_checar.click()

                    # Verifica se apareceu alerta após o "Checar"
                    try:
                        alert = WebDriverWait(navegador, 5).until(EC.alert_is_present())
                        alert_text = alert.text
                        print(f"Alerta encontrado após Checar: {alert_text}")
                        alert.accept()

                        if "Procedimento nao habilitado!" in alert_text:
                            print(f"Registro {i + 1}: Procedimento não habilitado")
                            df.at[i, 'auditado'] = 2
                            df.at[i, 'ds_motivo'] = f"Erro no Código do Procedimento {cod_proc_solicitado}: Código não habilitado."
                        else:
                            df.at[i, 'auditado'] = 2
                            df.at[i, 'ds_motivo'] = alert_text

                        df.at[i, 'timestamp_execucao'] = timestamp_execucao
                        print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
                        salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)
                        continue

                    except TimeoutException:
                        print("Nenhum alerta encontrado após 'Checar'. Procedimento válido.")

                except Exception as e:
                    print(f"Erro ao preencher procedimento ou clicar em 'Checar': {e}")
                    df.at[i, 'auditado'] = 2
                    df.at[i, 'ds_motivo'] = f"Erro ao validar procedimento: {str(e)}"
                    df.at[i, 'timestamp_execucao'] = timestamp_execucao
                    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
                    salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)
                    continue

                # Agora seleciona o CID-10
                try:
                    cid_10 = str(df.loc[i, "cd_cid_principal"]).strip()
                    select_cid10 = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.NAME, 'cid10_ih'))
                    )
                    select = Select(select_cid10)

                    # Caso especial: procedimentos múltiplos / politrauma → força CID '000'
                    if cod_proc_solicitado in codigos_multiplas:
                        select.select_by_value('000')
                        print(f"Procedimento {cod_proc_solicitado} → Múltiplas cirurgias/Politrauma. CID ajustado para '000' (INEXISTENTE).")
                        
                        df.at[i, 'auditado'] = 3
                        df.at[i, 'ds_motivo'] = (
                            f"CID alterado para 'CID INEXISTENTE' devido ao procedimento {cod_proc_solicitado} "
                            f"relacionado a CIRURGIA MÚLTIPLAS e/ou Politraumas."
                        )
                        df.at[i, 'timestamp_execucao'] = timestamp_execucao
                        salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)

                    else:
                        # Caso normal: tenta selecionar o CID vindo da planilha
                        try:
                            select.select_by_value(cid_10)
                            print(f"CID {cid_10} selecionado com sucesso.")
                        except Exception as e:
                            print(f"Erro ao selecionar CID {cid_10}: {e}")
                            df.at[i, 'auditado'] = 2
                            df.at[i, 'ds_motivo'] = f"Erro: CID {cid_10} não registrado ou inválido no SISREG."
                            df.at[i, 'timestamp_execucao'] = timestamp_execucao
                            print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
                            salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)
                            continue

                except Exception as e:
                    print(f"Erro geral ao lidar com o campo CID: {e}")
                    df.at[i, 'auditado'] = 2
                    df.at[i, 'ds_motivo'] = f"Erro ao processar seleção de CID: {str(e)}"
                    df.at[i, 'timestamp_execucao'] = timestamp_execucao
                    salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)
                    continue
                                                                                                                                                                                                                                                        
                
                # Seleciona a clínica (valor fixo '03').
                # Nota SISREG: Clínica refere-se ao tipo de especialidade; deve ser compatível com o procedimento.                                                                                                    
                select_clinica = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.NAME, 'clinica'))  
                )
                select = Select(select_clinica)

                try:
                    select.select_by_value('03')  
                except Exception as e:
                    print(f"Ocorreu um erro ao selecionar a opção: {e}")

                # Seleciona o médico solicitante, tentando pelo CPF ou nome, com fallback para valor padrão.
                # Nota SISREG: Médico deve estar cadastrado com CBO válido; sistema verifica vínculo com CNES.                                                                                                 
                select_medico_ih = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.NAME, 'medico_solicitante_ih'))  
                )
                select = Select(select_medico_ih)

                medico_ih = str(df.loc[i, "solicitante"])
                medico_cpf = str(df.loc[i,"cpf_solicitante"])

                try:
                    select.select_by_value(medico_cpf)
                except NoSuchElementException:
                    print(f"O Médico, {medico_ih} não foi localizado no cadastro do SISREG ")
                    try:
                        select.select_by_value('00000000000')
                    except Exception as e:
                        print(f"Ocorreu um erro ao selecionar a opção padrão: {e}")
                    
                    medico_solicitante = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.NAME, 'no_profissional_solicitante'))  
                    )
                    medico_solicitante.send_keys(medico_ih)
                    df.at[i, 'ds_motivo'] = (f"Médico(a) {medico_ih} não cadastrado no SISREG.")

                # Pega o CNES do registro atual
                hosp_exec = str(df.loc[i, "cnes_exe"]).zfill(7).strip()  # Você já tem isso mais abaixo; mova pra cá se preciso
                print(f" CNES {hosp_exec}")
                if hosp_exec in config:
                    section = config[hosp_exec]
                elif 'DEFAULT' in config:
                    section = config['DEFAULT']
                    print(f" CNES {hosp_exec} não encontrado → usando [DEFAULT]")
                    if pd.isna(df.at[i, 'ds_motivo']) or not df.at[i, 'ds_motivo']:
                        df.at[i, 'ds_motivo'] = ""
                    df.at[i, 'ds_motivo'] += f" | CNES {hosp_exec} → DEFAULT"    
                else:
                    raise ValueError(f"CNES {hosp_exec} não configurado e não existe na seção [DEFAULT].")
                    
                    

                # Extrai os valores (com fallback hardcoded se não existir no INI)
                nome_hospital = section.get('nome', 'HOSPITAL NÃO MAPEADO')
                hospitais_processados.add(nome_hospital)
                carater_eletivo = section.get('carater_eletivo', '10')  # Default '10' se não definido
                risco_eletivo = section.get('risco_eletivo', '2')
                carater_urgencia = section.get('carater_urgencia', '11')
                risco_urgencia = section.get('risco_urgencia', '1')
                central_regulacao = section.get('central_regulacao', '420910')
                lesao = section.get('lesao', 'leve')

                # -------------------------------------------------------
                # Determina caráter e risco com base no DataFrame
                # -------------------------------------------------------
                carater_df = int(float(str(df.loc[i, "cd_carater_atendimento"]).strip()))

                if carater_df == 1:           # Eletivo
                    carater_valor = carater_eletivo   # '10'
                    risco_valor   = risco_eletivo     # '2' ou '3' — confirme!!!
                    print(f"Registro {i+1} → Eletivo (caráter {carater_valor}, risco {risco_valor})")
                
                elif carater_df == 2:         # Urgência/Emergência
                    carater_valor = carater_urgencia  # '11'
                    risco_valor   = risco_urgencia    # '1'
                    print(f"Registro {i+1} → Urgência (caráter {carater_valor}, risco {risco_valor})")
                
                else:
                    # Valor inválido ou não informado → fallback para urgência (ou levante erro)
                    carater_valor = carater_urgencia
                    risco_valor   = risco_urgencia
                    print(f"Registro {i+1} → Caráter inválido '{carater_df}' → usando fallback URGÊNCIA")
                    df.at[i, 'ds_motivo'] = df.at[i, 'ds_motivo'] + " | Caráter inválido → usado urgência como fallback"
                
                # Agora seleciona os valores dinâmicos
                # Caráter
                select_carater = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.NAME, 'nu_carater_ih'))
                )
                select = Select(select_carater)
                select.select_by_value(carater_valor)
                
                # Risco / Prioridade
                select_risco = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.NAME, 'risco'))
                )
                select = Select(select_risco)
                select.select_by_value(risco_valor)
                
                # # Seleciona o caráter da internação (valor fixo '11').
                # # Nota SISREG: Caráter '10' indica eletiva;  '11' indica urgência, autorização posterior em até 48h (Portaria GM/MS nº 1.559/2008).                                                                                                                                 
                # select_carater = WebDriverWait(navegador, 10).until(
                #     EC.presence_of_element_located((By.NAME, 'nu_carater_ih'))  
                # )
                # select = Select(select_carater)

                # try:
                #     select.select_by_value('11')  
                # except Exception as e:
                #     print(f"Ocorreu um erro ao selecionar a opção: {e}")

                # # Seleciona o risco (valor fixo '1') no caso de urgencia sempre Amarelo  Prioridade 1.
                # # Nota SISREG: Risco classifica prioridade; sistema usa para regulação de vagas.                                                                                  
                # select_risco = WebDriverWait(navegador, 10).until(
                #     EC.presence_of_element_located((By.NAME, 'risco'))  
                # )
                # select = Select(select_risco)

                # try:
                #     select.select_by_value('1') 
                # except Exception as e:
                #     print(f"Ocorreu um erro ao selecionar a opção: {e}")


                
                # Clica no botão "OK" para prosseguir.
                bnt_ok = WebDriverWait(navegador, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@value='OK']"))
                )
                bnt_ok.click()

                # Seleciona a unidade executora pelo CNES.
                # Nota SISREG: Unidade deve ser habilitada para o procedimento; verificação via CNES/SIGTAP.  
                select_central_executante = WebDriverWait (navegador, 10).until(
                    EC.presence_of_element_located((By.NAME, 'co_municipio_desejado'))  
                )   
                select = Select(select_central_executante)
                select.select_by_value(central_regulacao)
                
                print(f" Central Reguladora:  {central_regulacao}")   
                                                
                select_unidade_exec = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.NAME, 'co_cnes_ups_desejada'))  
                )
                
                select = Select(select_unidade_exec)
                try:
                    select.select_by_value(hosp_exec)
                except Exception as e:
                    print(f"Ocorreu um erro ao selecionar o hospital executante: {e}")
                
                # Preenche os sintomas clínicos.
                # Nota SISREG: Campo obrigatório para justificativa clínica da AIH.                                                                     
                sintomas_clinicos = str(df.loc[i, "ds_sinais_sint_clinicos"])
                ds_sintomas_clinicos = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.NAME, 'ds_sintoma'))  
                )
                ds_sintomas_clinicos.send_keys(sintomas_clinicos)
                #time.sleep(5) #Adiciona tempo caso esteja apresentando timeout  
                #input() #Aguarda informação para continuar 
                # Preenche os resultados de provas diagnósticas.
                # Nota SISREG: Campo obrigatório para comprovação diagnóstica na AIH.                                                                         
                result_provas_diagnosticas = str(df.loc[i, "ds_result_prov_diag"])
                ds_result_prov_diag = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.NAME, 'ds_prova'))  
                )
                ds_result_prov_diag.send_keys(result_provas_diagnosticas)
                #time.sleep(5) #Adiciona tempo caso esteja apresentando timeout  
                #input() #Aguarda informação para continuar 
                # Preenche a justificativa de internação.
                # Nota SISREG: Justificativa deve ser detalhada; usada em auditorias para validar necessidade da internação.                                                                                                              
                justifica_internacao = str(df.loc[i, "ds_concat"])
                ds_justifica_internacao = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.NAME, 'ds_justificativa'))  
                )
                ds_justifica_internacao.send_keys(justifica_internacao)

                # Seleciona o tipo de lesão (leve).
                # Nota SISREG: Campo para classificação de gravidade; afeta prioridade na regulação.                                                                                        
                tplesao = WebDriverWait(navegador, 10).until(
                    #EC.presence_of_element_located((By.XPATH, "//input[@type='radio' and @value='leve']"))
                     EC.presence_of_element_located((By.XPATH, "//input[@type='radio' and @value='" + lesao + "']"))
                )
                
                print(f"Selecionado com sucesso: {lesao}")
                
                tplesao.click()
                
                
                
                # # Clica no botão "Solicitar" para enviar a solicitação.
                # # Nota SISREG: Ao solicitar, sistema verifica duplicidade (não permite AIH pendente para mesmo paciente/procedimento).                                                                                                                       
                bnt_solicitar = WebDriverWait(navegador, 10).until(
                     EC.element_to_be_clickable((By.XPATH, "//input[@value='Solicitar']"))
                 )
                # ## COMENTAR bnt_solicitar.click AO USAR O SIMULADOR
                bnt_solicitar.click()
                #input()

                time.sleep(2) 
                ## Chama função para capturar o número de internação gerado.
                obter_numero_internacao_sisreg(navegador, i, timestamp_execucao)

                tempo_fim = datetime.now()
                tempo_execucao = (tempo_fim - tempo_inicio).total_seconds()
                data_execucao = tempo_inicio.strftime('%d/%m/%y')
                hora_execucao = tempo_inicio.strftime('%H:%M:%S')

                # Atualiza o DataFrame com tempos de execução.
                df.at[i, 'tempo_inicio'] = tempo_inicio
                df.at[i, 'tempo_fim'] = tempo_fim
                df.at[i, 'tempo_execucao'] = tempo_execucao
                df.at[i, 'data_execucao'] = data_execucao
                df.at[i, 'hora_execucao'] = hora_execucao
                #df.at[i, 'timestamp_execucao'] = timestamp_execucao

            except CNSInvalidoException as e:
                print(e)
                df.at[i, 'auditado'] = 2
                df.at[i, 'ds_motivo'] = str(e)
                df.at[i, 'timestamp_execucao'] = timestamp_execucao
                print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
                salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)

                continue

            # A validação de CEP/residência foi desabilitada.
            # except CEPInvalidoException:
            #     if registro.get('residencia') != "JOINVILLE-SC":
            #         df.at[i, 'auditado'] = 2
            #         df.at[i, 'ds_motivo'] = "Erro no CEP: Paciente não registrado como residente de JOINVILLE-SC."
            #         df.at[i, 'timestamp_execucao'] = timestamp_execucao
            #         print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
            #         salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)
                
            #     elif registro.get('categoria') in ["NÔMADE", "MORADOR DE RUA", "CIGANO"]:
            #         df.at[i, 'auditado'] = 2
            #         df.at[i, 'ds_motivo'] = "Paciente não possui residência fixa em JOINVILLE-SC (NÔMADE, MORADOR DE RUA ou CIGANO)."
            #         df.at[i, 'timestamp_execucao'] = timestamp_execucao
            #         print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")

            #         salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)

            except Exception as e:
                print(f"Erro inesperado no registro {linha_arquivo}: {str(e)}")
                df.at[i, 'auditado'] = 2
                df.at[i, 'ds_motivo'] = f"Erro desconhecido: {str(e)}"
                df.at[i, 'timestamp_execucao'] = timestamp_execucao
                print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
                salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)
                continue

    # Captura o horário de fim e calcula tempos totais.
    hora_fim = datetime.now()
    tempo_total_execucao = (hora_fim - hora_inicio).total_seconds()

    registros_processados_indices = list(timestamps_execucao.keys())  # Índices dos registros processados
    registros_processados = df.loc[registros_processados_indices]  # Filtra os registros no DataFrame
    registros_sucesso = registros_processados[registros_processados['auditado'] == 3]
    registros_erros = registros_processados[registros_processados['auditado'] == 2]
    registros_duplicados = registros_processados[registros_processados['auditado'] == 4]

    tempo_total_processamento = registros_processados['tempo_execucao'].sum()
    tempo_medio_por_registro = tempo_total_processamento / len(registros_processados) if len(registros_processados) > 0 else 0


    total_processados = len(registros_processados)
    total_sucesso = len(registros_sucesso)
    total_erros = len(registros_erros)
    total_duplicados = len(registros_duplicados)

    # Função para formatar tempo em segundos para HH:MM:SS.
    def formatar_tempo(segundos):
        tempo = timedelta(seconds=round(segundos))  # Arredonda os segundos
        return str(tempo)  # Converte diretamente para HH:MM:SS

    # Mapeamento de CNES para nomes de hospitais.
    if hospitais_processados:
        if len(hospitais_processados) == 1:
            hospital = list(hospitais_processados)[0]
        else:
            hospital = f"MÚLTIPLOS HOSPITAIS → {', '.join(sorted(hospitais_processados))}"
    else:
        hospital = "NENHUM HOSPITAL PROCESSADO"
    
    
    # Obtém o nome do hospital baseado no CNES.
    # Nota SISREG: CNES deve ser mapeado corretamente; sistema usa para validação de habilitação.                                                                                                 
    
    # Exibe o resultado do mapeamento.
    print(f"Hospital Executante: {hosp_exec} → Hospital: {hospital}")


    # Exibe estatísticas de processamento.
    print("         ")
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    print(f"Total de registros processados: {total_processados}")
    print(f"Total de registros com sucesso: {total_sucesso}")
    print(f"Total de registros com erros: {total_erros}")
    print(f"Total de registros duplicados: {total_duplicados}")

    # Exibe tempos formatados.
    print(f"⏱ Tempo total da execução: {formatar_tempo(tempo_total_execucao)}")
    print(f"⏱ Tempo total do processamento dos registros: {formatar_tempo(tempo_total_processamento)}")
    print(f"⏱ Tempo médio por registro: {formatar_tempo(tempo_medio_por_registro)}")

    # Gera mensagem final de conclusão.
    mensagem = (
        f"Processo concluído com sucesso!\n"
        f"\n"
        f"Hospital: {hospital} \n"
        f"Registros processados: {total_processados}\n"
        f"Registros executados com sucesso: {total_sucesso}\n"
        f"Registros com erros: {total_erros}\n"
        f"Registros duplicados: {total_duplicados}\n"

        f"\n"

        f"Tempo total da execução:  {formatar_tempo(tempo_total_execucao)} segundos.\n"
        f"Tempo médio por registro:  {formatar_tempo(tempo_medio_por_registro)} segundos.\n"
        f"Tempo do processamento dos registros:  {formatar_tempo(tempo_total_processamento)} segundos."
        
    )

    # Caminho para o arquivo de controle de logs.
    caminho_control = "./LOGS/control.txt"

    # Cria ou carrega o parser de configuração para salvar estatísticas.
    control = configparser.ConfigParser()

    if os.path.exists(caminho_control):
        control.read(caminho_control, encoding="utf-8")


    # Adiciona seção com informações de execução ao arquivo de controle.
    control["info_aih"] = {

        "hospital": hospital,

        "total_processados": total_processados,
        "total_sucesso": total_sucesso,
        "total_erros": total_erros,
        "total_duplicados": total_duplicados,
        
        "tempo_total_execucao": formatar_tempo(tempo_total_execucao),
        "tempo_medio_por_registro": formatar_tempo(tempo_medio_por_registro),
        "tempo_total_processamento": formatar_tempo(tempo_total_processamento),
        
        
    }


    # Salva as configurações no arquivo.
    with open(caminho_control, "w", encoding="utf-8") as controlfile:
        control.write(controlfile)


    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    log_file.close()

    try:

        # Exibe resumo final no console.
        print(f"\n🔴 Fim da execução: {control['info_aih']['total_processados']}")
        print(f"✅ Sucesso: {control['info_aih']['total_sucesso']}")
        print(f" X  Erros: {control['info_aih']['total_erros']}")
        print(f"⚠️ Duplicados: {control['info_aih']['total_duplicados']}\n")

        print(f"⏳ Tempo total de execução: {control['info_aih']['tempo_total_execucao']}")
        print(f"⏱ Tempo médio por registro: {control['info_aih']['tempo_medio_por_registro']}")
        print(f"⏳ Tempo total do processamento: {control['info_aih']['tempo_total_processamento']}\n")


        navegador.quit()

        # Exibe mensagem de conclusão via Tkinter.
        mostrar_mensagem(mensagem)

        # Executa um painel de estatísticas externo.
        exe_path = os.path.abspath("CONFIG/rpaStatExecPanel.exe")
        print(f"Verificando caminho: {exe_path}")

        if os.path.exists(exe_path):
            print("Arquivo encontrado! Tentando executar...")
            os.startfile(exe_path)
        else:
            print("ERRO: Arquivo não encontrado!")

        print(f"\n Fim da execução: {hora_fim.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Tempo total de execução: {formatar_tempo(tempo_total_execucao)}\n")
    finally:
       
        # Garante que log_content seja UTF-8 válido.
        global log_content
        log_content = log_content.encode('utf-8', errors='replace').decode('utf-8')

        # URLs de imagens para o card no Google Chat.
        IMAGE_URL_CORRECT = "https://img.icons8.com/?size=100&id=4JmJwTZOPITk&format=png&color=000000"
        IMAGE_URL_ERROR = "https://img.icons8.com/?size=100&id=-rqk5MHCmR3K&format=png&color=000000"

        # Seleciona imagem baseada na presença de erros.
        selected_image_url = IMAGE_URL_ERROR if total_erros > 0 else IMAGE_URL_CORRECT
        print(f"Imagem selecionada: {selected_image_url} (total_erros: {total_erros})")

        # Prepara o payload para o card no Google Chat.
        message_payload = {
            "text": "Log da Automação V7.2 RPA-AIH-SISREG-HOSP - Veja o card abaixo para detalhes",
            "cardsV2": [
                {
                    "cardId": "logCard",
                    "card": {
                        "header": {
                            "title": "Log da Execução - RPA-AIH-SISREG-HOSP V7.2",
                            "subtitle": "Detalhes do processamento",
                            "imageUrl": selected_image_url,
                            "imageType": "CIRCLE"
                        },
                        "sections": [
                            {
                                "header": hospital,
                                "collapsible": True,
                                "uncollapsibleWidgetsCount": 1,
                                "widgets": [
                                    {
                                        "textParagraph": {
                                            "text": "Este é o log gerado pelo script de automação."
                                        }
                                    },
                                    {
                                        "textParagraph": {
                                            "text": log_content
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }

        webhook_urls = [WEBHOOK_URL_DEFAULT]
        if WEBHOOK_URL_ADDITIONAL:
            webhook_urls.append(WEBHOOK_URL_ADDITIONAL)

        # Envia a requisição POST para cada webhook
        for webhook_url in webhook_urls:
            try:
                response = requests.post(
                    webhook_url,
                    json=message_payload,
                    proxies=proxies if proxies else None,  # Usa proxies se configurados, senão None
                    timeout=10
                )
                response.raise_for_status()  # Lança exceção para qualquer código >= 400
        
                #print(f" -> Card enviado para {webhook_url} com sucesso!")
                print(f" -> Card enviado para Gchat com sucesso!")
            except requests.exceptions.HTTPError as http_err:
                #print(f" X - Erro HTTP ao enviar para {webhook_url}: {http_err} - {response.text}")
                print(f" X - Erro HTTP ao enviar para GChat: {http_err} - {response.text}")
            except requests.exceptions.RequestException as req_err:
                #print(f" X - Erro de requisição ao enviar para {webhook_url}: {req_err}")
                print(f" X - Erro de requisição ao enviar para Gchat: {req_err}")
            except Exception as e:
                #print(f" X - Erro inesperado ao enviar para {webhook_url}: {str(e)}")
                print(f" X - Erro inesperado ao enviar para Gchat: {str(e)}")
        # Remove colunas temporárias do DataFrame.
        colunas_para_remover = ['tempo_inicio', 'tempo_fim', 'tempo_execucao', 'timestamp_execucao']
        df.drop(columns=colunas_para_remover, inplace=True, errors='ignore')

        salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)

        print(f"-> Processo concluído. Log salvo em: {log_filename}")

    
def verificar_cns(nr_cns, body_text):
    # Verifica se o CNS está presente no texto da página; levanta exceção se inválido ou não encontrado.
    # Nota SISREG: Regra oficial: CNS deve ser válido (15 dígitos, checksum), cadastrado na base nacional e sem óbito associado (integração com SIM).                                                                                                                                                      
    mensagem_erro = f"O usuario de CNS {nr_cns} não foi encontrado na base local de dados."
    if nr_cns not in body_text or mensagem_erro in body_text:
        if nr_cns not in body_text:
            raise CNSInvalidoException(f"Erro: CNS {nr_cns} pode ter sido alterado.")
        elif mensagem_erro in body_text:
            raise CNSInvalidoException(f"Erro: CNS não cadastrado ou localizado no Sisreg.") #{mensagem_erro}")
# Para checar apenas pacientes de seu municipio, verifique na pagina body_text como ele esta grafado
# Para aplicar o nome da cidade use municipio_residencia_match

    # Verificação adicional para óbito
    # Verifica presença de "dados do obito" ou padrão de data de óbito (ex: DD/MM/AAAA)
    obito_match_tabela = re.search(r'Detalhes do Óbito', body_text, re.IGNORECASE)
    obito_match_data = re.search(r'\b\d{2}/\d{2}/\d{4}\b', body_text)  # Padrão simples de data DD/MM/AAAA; ajuste se necessário
    if obito_match_tabela or (obito_match_data and "óbito" in body_text.lower()):
        raise CNSInvalidoException(f"Erro: Paciente com CNS {nr_cns} consta como óbito no sistema.")
         
def verificar_residencia(nr_cns, registro, body_text, df, i, timestamp_execucao):
    """
    Verifica o Município de Residência e o Tipo de Moradia do paciente.
    Atualiza o dataframe com o status de auditado e motivo, se aplicável.
    
    :param nr_cns: Número CNS do paciente.
    :param body_text: Texto do corpo da página para análise.
    :param df: DataFrame principal.
    :param i: Índice do registro no DataFrame.
    :return: True se a verificação for bem-sucedida (residente em Joinville-SC), False caso contrário.
    """
    # Esta função foi desabilitada; sempre retorna True para ignorar validações de moradia e município.
    return True
    
    # Código original comentado para referência:
    # municipio_residencia_match = re.search(r'Município de Residência:\s*(.*)', body_text)
    # if municipio_residencia_match:
    #     municipio_completo = municipio_residencia_match.group(1).strip()
    #     joinville_match = re.search(r'JOINVILLE\s-\sSC', municipio_completo)

    #     if joinville_match:
    #         print(f"Paciente CNS {nr_cns} é residente em Joinville-SC.")
    #         return True
    #     else:
    #         # Verificar Tipo de Moradia
    #         moradia_match = re.search(r'Tipo de Moradia:\s*(NÔMADE|CIGANO|MORADOR DE RUA)', body_text)
    #         if moradia_match:
    #             df.at[i, 'auditado'] = 2
    #             df.at[i, 'ds_motivo'] = f"Erro: Paciente CNS {nr_cns} cadastrado como {moradia_match.group(1)}, não residente em Joinville-SC."
    #             df.at[i, 'timestamp_execucao'] = timestamp_execucao
    #             print(f"Erro: Paciente CNS {nr_cns} não está cadastrado como residente de Joinville-SC.")
    #             print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")           
    #             salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)

    #         else:
    #             df.at[i, 'auditado'] = 2
    #             df.at[i, 'ds_motivo'] = f"Erro: Paciente CNS {nr_cns} não cadastrado como residente em Joinville-SC."
    #             df.at[i, 'timestamp_execucao'] = timestamp_execucao
    #             print(f"Erro: Paciente CNS {nr_cns} não está cadastrado como residente de Joinville-SC.")
    #             print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")            
    #             salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)

    #         return False
    # else:
    #     df.at[i, 'auditado'] = 2
    #     df.at[i, 'ds_motivo'] = f"Erro: Não foi possível localizar o Município de Joinville / SC no  registro do paciente CNS {nr_cns}."
    #     df.at[i, 'timestamp_execucao'] = timestamp_execucao
    #     print(f"Erro: Paciente CNS {nr_cns} não está cadastrado como residente de Joinville-SC.")
    #     print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖") 
    #     salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)

    #     return False
    
    

# Função para capturar o número de internação gerado pelo Sisreg.
def obter_numero_internacao_sisreg(navegador, i, timestamp_execucao):

    # Captura elementos da página para extrair o número de internação.
    linhas = navegador.find_elements(By.TAG_NAME, "p")

    if len(linhas) >= 1:  # Garantir que exista pelo menos uma linha
        linha_1 = linhas[0].text  # Texto completo da linha 1
        #print(f"Linha 1: {linha_1}")

        # Usa regex para capturar o código de 9 dígitos.
        match = re.search(r'\b\d{9}\b', linha_1)  # Procurar por 9 dígitos consecutivos

        # Salva o valor na variável 'codigo'
        nr_internacao = match.group(0) if match else None

        # Converter nr_internacao para inteiro
        if nr_internacao:
            # Converter nr_internacao para inteiro
            nr_internacao = int(nr_internacao)
            
            # Atualiza o DataFrame com o número de internação e marca como auditado com sucesso.
            df.loc[i, "nu_internacao"] = nr_internacao
            print(f" Nº da internação salvo: {nr_internacao}")
            df.at[i, 'auditado'] = 3
            df.at[i, 'timestamp_execucao'] = timestamp_execucao
            print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
            salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)

        else:
            pass
            # print("Erro: Não foi encontrado um código de internação.")
            # print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    else:
        #print("Erro: A linha 1 não existe na tabela.")
        # Nota SISREG: Detecção de duplicidade; sistema oficial bloqueia se houver AIH pendente para o mesmo paciente/procedimento.                                                                                                                             
        df.at[i, 'auditado'] = 4
        df.at[i, 'ds_motivo'] = f"Erro: O Paciente já possui um código de internação gerado e pendente para o procedimento de internação."
        df.at[i, 'timestamp_execucao'] = timestamp_execucao
        print("Erro: O paciente já possui uma solicitação pendente para o procedimento.")
        print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
        salvar_arquivo_excel(os.path.join(diretorio, nome_arquivo_xlsx), df)

    return 

# Classes de exceções customizadas
class CNSInvalidoException(Exception):
    pass

class CEPInvalidoException(Exception):
    pass

class CIDInvalidoException(Exception):
    pass


# Função para obter credenciais via interface gráfica Tkinter.
def obter_credenciais_gui():
    def confirmar(event=None):  # Aceita o evento "Enter"
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        root.credentials = (usuario, senha)
        root.destroy()  # Fecha a janela após capturar os dados

    # Configura a janela principal da GUI.
    
    root = tk.Tk()
    root.title(f"RPA-AIH-SISREG-HOSPITALAR")
    root.geometry("350x250")  # Define o tamanho da janela (largura x altura)
    root.resizable(False, False)  # Impede redimensionamento

    # Adiciona ícone à janela.
    try:
        root.iconbitmap(r"./IMG/AIH-PRONT.ico")  # Substitua pelo caminho do seu ícone .ico
    except Exception as e:
        print(f"Erro ao carregar ícone: {e}")

    # Adiciona labels e entradas para usuário e senha.
    tk.Label(root, text="AUTOMAÇÃO DE AUTORIZAÇÃO \n DE INTERNAÇÃO HOSPITALAR", font=("Helvetica", 10, "bold")).pack(pady=10)

    tk.Label(root, text="Digite o usuário:", font=("Arial", 12)).pack(pady=10)
    entry_usuario = tk.Entry(root, font=("Arial", 12), width=30)
    entry_usuario.pack()

    tk.Label(root, text="Digite a senha:", font=("Arial", 12)).pack(pady=10)
    entry_senha = tk.Entry(root, font=("Arial", 12), width=30, show="*")   
    entry_senha.pack()


    # Botão de confirmação.
    btn_confirmar = tk.Button(root, text="Confirmar", font=("Arial", 12), command=confirmar, width=10, height=1)
    btn_confirmar.place(x=125, y=206)

    # Rótulo para versão, clicável para abrir tela de versão.
    lbl_versao = tk.Label(root, text="Versão 7.2", font=("Arial", 10, "bold"), fg="blue", cursor="hand2")
    lbl_versao.place(x=270, y=225)
    lbl_versao.bind("<Button-1>", lambda e: abrir_tela_versao())  # Vincula o clique apenas ao rótulo

    # Bind para "Enter" ativar o botão.
    root.bind("<Return>", confirmar)

    # Centraliza a janela.
    root.eval('tk::PlaceWindow . center')

    # Inicia o loop da janela
    root.credentials = None
    root.mainloop()

    return root.credentials

def abrir_tela_versao():
    # Abre uma nova janela com informações de versão.
    nova_janela = tk.Tk()
    nova_janela.title("Informação da Versão")
    nova_janela.geometry("300x150")  # Define o tamanho da nova janela
    nova_janela.resizable(False, False)  # Impede redimensionamento

    # Adiciona ícone à nova janela.
    try:
        nova_janela.iconbitmap(r"./IMG/AIH-PRONT.ico")  # Substitua pelo caminho do seu ícone .ico
    except Exception as e:
        print(f"Erro ao carregar ícone: {e}")


    # Adiciona labels com informações de versão.
    tk.Label(nova_janela, text="Versão 7.2", font=("Helvetica", 10, "bold"), fg="blue").pack(padx=10, pady=10)
    tk.Label(nova_janela, text="Desenvolvido por:", font=("Helvetica", 10,"bold" )).place(x=10, y=45)
    tk.Label(nova_janela, text="Núcleo de Tecnologia da Informação\nda Área da Saúde de Joinville/SC", font=("Helvetica", 10)).place(x=45, y=75)
    tk.Label(nova_janela, text="2026", font=("Helvetica", 10, "bold")).place(x=130, y=120)

# Execução principal
if __name__ == "__main__":
    try:
        # Define o diretório e carrega os dados do Excel.
        diretorio = Path('LOTES')
        nome_arquivo_xlsx, df = carregar_dados_excel(diretorio)

        # Define se usa GUI para credenciais.
        usar_gui = True #Altere para True para usar a interface gráfica

        if usar_gui:
            usuario, senha = obter_credenciais_gui()
            headless = False  # Executa com interface gráfica
        else:
            usuario = 'usuario'  # Substitua pelo seu usuário
            senha = 'senha'      # Substitua pela sua senha
            headless = False  # Executa com interface gráfica

        lote_df = processar_automacao(df, usuario, senha, headless)

        # Salva as alterações no arquivo Excel.
        caminho_arquivo = os.path.join(diretorio, nome_arquivo_xlsx)


        salvar_arquivo_excel(caminho_arquivo, df)

    except Exception as erro:
        print(f"Erro na execução: {str(erro)}")
