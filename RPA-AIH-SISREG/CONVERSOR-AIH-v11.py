###################################################################################################
# Desenvolvido por Ricardo Dias Lemos dos Santos
# Atualizado 2026
# V.22.7 - Abre o último arquivo XLSX gerado no aplicativo padrão ao final do processamento
# SES-CAC-NTI
# Comandos para compilação
# pip install pyinstaller
# pyinstaller --onefile --windowed --icon=IMG/CSV-to-XLSX.ico CONVERSOR-AIH.py
# pyinstaller --onedir --windowed --icon=IMG/CSV-to-XLSX.ico CONVERSOR-AIH.py
# pyinstaller --onefile --windowed --icon=IMG/CSV-to-XLSX.ico --clean --noupx --hidden-import=openpyxl CONVERSOR-AIH-COR11.py
###################################################################################################

import pandas as pd
pd.options.mode.chained_assignment = None
import re
import os
import shutil
import csv
import sys
import tkinter as tk
import warnings
import string
from datetime import datetime
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Protection, Alignment, PatternFill
from openpyxl.worksheet.protection import SheetProtection
from openpyxl.formatting.rule import FormulaRule
from tkinter import scrolledtext
from tkinter import Tk, messagebox
from tkinter import ttk

warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

# Diretório do lock
lock_file_path = Path("./processo_em_execucao.lock")

# Contador de arquivos processados
contador_arquivos = [0]

# Nome do arquivo de log
log_filename = f"LOGS/EXTRACAO/extracao_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

# Variável para guardar o último arquivo XLSX salvo com sucesso
ultimo_arquivo_salvo = None

# Variável global para controle da janela de progresso
janela_progresso = None
barra_progresso = None
label_progresso = None
terminal_logs = None

def abrir_janela_progresso(total_arquivos):
    global janela_progresso, barra_progresso, label_progresso
    
    janela_progresso = tk.Tk()
    janela_progresso.title("Conversor RPA-AIH-SISREG-HOSP -> Processando Arquivos")
    janela_progresso.geometry("500x250")
    janela_progresso.resizable(False, False)
    janela_progresso.attributes("-topmost", True)  # fica sempre no topo
    
    # Centralizar a janela
    largura_tela = janela_progresso.winfo_screenwidth()
    altura_tela = janela_progresso.winfo_screenheight()
    x = (largura_tela - 500) // 2
    y = (altura_tela - 250) // 2
    janela_progresso.geometry(f"+{x}+{y}")
    
    tk.Label(janela_progresso, text="Convertendo arquivos CSV para XLSX...", font=("Arial", 12)).pack(pady=15)
    
    barra_progresso = ttk.Progressbar(janela_progresso, orient="horizontal", length=380, mode="determinate")
    barra_progresso.pack(pady=10)
    barra_progresso['maximum'] = total_arquivos
    
    label_progresso = tk.Label(janela_progresso, text=f"Processando arquivo 0 de {total_arquivos}", font=("Arial", 10))
    label_progresso.pack(pady=5)
    
    # Impedir fechamento manual (opcional, mas melhora UX)
    janela_progresso.protocol("WM_DELETE_WINDOW", lambda: None)
    
    # Atualizar interface imediatamente
    janela_progresso.update()

def atualizar_progresso(arquivo_atual, total_arquivos, nome_arquivo=""):
    if janela_progresso and janela_progresso.winfo_exists():
        barra_progresso['value'] = arquivo_atual
        texto = f"Processando arquivo {arquivo_atual} de {total_arquivos}"
        if nome_arquivo:
            texto += f" - {nome_arquivo}"
        label_progresso.config(text=texto)
        janela_progresso.update()

def fechar_janela_progresso():
    global janela_progresso, terminal_logs, barra_progresso, label_progresso
    if janela_progresso and janela_progresso.winfo_exists():
        janela_progresso.destroy()
    janela_progresso = None
    terminal_logs = None
    barra_progresso = None
    label_progresso = None

def log_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg_completa = f"[{timestamp}] {message}\n"

    # Escreve no arquivo de log
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write(msg_completa)
    
    print(msg_completa.strip())

# Mostra na janela de progresso, se ela estiver aberta
    try:
        if (terminal_logs is not None and 
            hasattr(terminal_logs, 'winfo_exists') and 
            terminal_logs.winfo_exists() and 
            janela_progresso is not None and 
            janela_progresso.winfo_exists()):
            terminal_logs.insert(tk.END, msg_completa)
            terminal_logs.see(tk.END)
            janela_progresso.update_idletasks()
    except:
        pass  # ignora silenciosamente se a janela já foi destruída

# Nova função para criar a janela de progresso com mini terminal
def abrir_janela_progresso(total_arquivos):
    global janela_progresso, barra_progresso, label_progresso, terminal_logs
    
    janela_progresso = tk.Tk()
    janela_progresso.title("Processando Arquivos")
    janela_progresso.geometry("600x400")  # aumentei a altura para caber o terminal
    janela_progresso.resizable(False, False)
    janela_progresso.attributes("-topmost", True)
    
    # Centralizar
    largura_tela = janela_progresso.winfo_screenwidth()
    altura_tela = janela_progresso.winfo_screenheight()
    x = (largura_tela - 600) // 2
    y = (altura_tela - 400) // 2
    janela_progresso.geometry(f"+{x}+{y}")
    
    # Ícone (se quiser manter)
    try:
        janela_progresso.iconbitmap("IMG/CSV-to-XLSX.ico")
    except:
        pass
    
    tk.Label(janela_progresso, text="Convertendo arquivos CSV para XLSX...", font=("Arial", 12, "bold")).pack(pady=10)
    
    barra_progresso = ttk.Progressbar(janela_progresso, orient="horizontal", length=550, mode="determinate")
    barra_progresso.pack(pady=5)
    barra_progresso['maximum'] = total_arquivos
    
    label_progresso = tk.Label(janela_progresso, text=f"Processando arquivo 0 de {total_arquivos}", font=("Arial", 10))
    label_progresso.pack(pady=5)
    
    # Mini terminal (área de logs rolável)
    tk.Label(janela_progresso, text="Logs em tempo real:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10,0))
    
    terminal_logs = scrolledtext.ScrolledText(
        janela_progresso,
        width=70,
        height=12,
        font=("Consolas", 10),
        state="normal",
        wrap=tk.WORD,
        bg="#1e1e1e",
        fg="#d4d4d4"
    )
    terminal_logs.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    # Impedir fechamento manual
    janela_progresso.protocol("WM_DELETE_WINDOW", lambda: None)
    
    # Atualizar interface
    janela_progresso.update()


def mostrar_mensagem(mensagem):
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo("Conversor RPA-AIH-SISREG-HOSP", mensagem)
    root.destroy()

def clean_cod_proc_solicitado(value):
    try:
        return str(int(float(value)))
    except (ValueError, TypeError):
        return '0'

# Verifica lock
if lock_file_path.exists():
    log_message("Conversão em execução. Aguarde finalizar o processo.")
    mostrar_mensagem("Conversão em execução. Aguarde finalizar o processo.")
    sys.exit()

try:
    lock_file_path.touch()

    diretorio_csv = Path("./")
    diretorio_xlsx = Path("./")
    diretorio_csv_registros = Path("LOTES/BKP")
    diretorio_xlsx_registros = Path("LOTES")

    diretorio_xlsx.mkdir(exist_ok=True)
    diretorio_csv_registros.mkdir(parents=True, exist_ok=True)
    diretorio_xlsx_registros.mkdir(parents=True, exist_ok=True)

    os.makedirs("LOGS/EXTRACAO", exist_ok=True)

    def detectar_delimitador(arquivo, encoding="utf-8"):
        try:
            with open(arquivo, "r", encoding=encoding, errors="replace") as f:
                primeira_linha = f.readline()
            return ';' if primeira_linha.count(';') > primeira_linha.count(',') else ','
        except:
            return ';'

    def chave_ordenacao_natural(texto):
        partes = re.split(r'(\d+)', texto)
        return [int(p) if p.isdigit() else p for p in partes]

    def converter_xls_para_xlsx(pasta):
        for arquivo in pasta.glob("*.xls"):
            try:
                df = pd.read_excel(arquivo)
                novo = arquivo.with_suffix('.xlsx')
                df.to_excel(novo, index=False)
                log_message(f"Convertido: {arquivo.name} → {novo.name}")
                os.remove(arquivo)
            except Exception as e:
                log_message(f"X - Erro ao converter {arquivo.name}: {e}")

    converter_xls_para_xlsx(diretorio_csv)

    def processar_arquivo(caminho_arquivo):
        global ultimo_arquivo_salvo
        contador_arquivos[0] += 1
        nome = caminho_arquivo.name
        log_message(f" -> Processando arquivo: {nome} (total: {contador_arquivos[0]})")

        try:
            if caminho_arquivo.suffix.lower() == '.csv':
                encodings = ['utf-8-sig', 'windows-1252', 'utf-8', 'latin1', 'iso-8859-1']
                df = None

                for enc in encodings:
                    try:
                        delim = detectar_delimitador(caminho_arquivo, enc)
                        df = pd.read_csv(
                            caminho_arquivo,
                            encoding=enc,
                            sep=delim,
                            on_bad_lines='warn',
                            quoting=csv.QUOTE_ALL,
                            low_memory=False,
                            dtype=str,
                            encoding_errors='replace'
                        )
                        log_message(f" Lido com encoding {enc} | {len(df)} linhas")
                        break
                    except Exception as e:
                        log_message(f" -> Falha com {enc}: {e}")
                        continue

                if df is None:
                    log_message(f" -> FALHA TOTAL NA LEITURA DO CSV: {nome}")
                    return None

                # Remover BOM se ainda presente
                df = df.apply(lambda x: x.str.lstrip('\ufeffï»¿') if x.dtype == "object" else x)

            elif caminho_arquivo.suffix.lower() in ('.xlsx', '.xls'):
                df = pd.read_excel(caminho_arquivo, dtype=str, engine='openpyxl')
                log_message(f" Arquivo Excel lido | {len(df)} linhas")
            else:
                log_message(f" -> Formato não suportado: {nome}")
                return None

        except Exception as e:
            log_message(f" X Erro ao ler {nome}: {e}")
            return None

        # Padronizar colunas
        df.columns = [col.strip().lower() for col in df.columns]

        if 'cod_proc_solicitado' not in df.columns:
            log_message(f" X Campo 'cod_proc_solicitado' não encontrado em {nome}")
            return df

        # Validação de erros
        df['erros_validacao'] = ''
        # Colunas obrigatórias
        essenciais = ['cod_proc_solicitado', 'cpf_solicitante', 'dt_solicitacao']
        faltando = [c for c in essenciais if c not in df.columns]
        if faltando:
            msg = f"X Colunas obrigatórias ausentes: {', '.join(faltando)}"
            log_message(f"X ERRO CRÍTICO: {msg}")
            df['erros_validacao'] += msg + '; '

        # CPF inválido
        if 'cpf_solicitante' in df.columns:
            df['cpf_solicitante'] = df['cpf_solicitante'].astype(str).str.strip()
            mask_invalido = (
                df['cpf_solicitante'].isin(['', '0', '00', '00000000000']) 
                #|~df['cpf_solicitante'].str.match(r'^\d{11}$')
            )
            if mask_invalido.any():
                qtd = mask_invalido.sum()
                log_message(f"{qtd} linhas com CPF inválido")
                df.loc[mask_invalido, 'erros_validacao'] += 'CPF inválido; '

        # Data inválida
        if 'dt_solicitacao' in df.columns:
            df['dt_temp'] = pd.to_datetime(df['dt_solicitacao'], dayfirst=True, errors='coerce')
            mask_invalida = df['dt_temp'].isna()
            if mask_invalida.any():
                qtd = mask_invalida.sum()
                log_message(f" -> {qtd} linhas com data inválida")
                df.loc[mask_invalida, 'erros_validacao'] += 'Data inválida; '
            df = df.drop(columns=['dt_temp'])

        # Tratamento do código solicitado
        df['cod_proc_solicitado'] = df['cod_proc_solicitado'].apply(clean_cod_proc_solicitado)
        df['cod_proc_solicitado'] = df['cod_proc_solicitado'].astype(str).str.zfill(10)

        antes = len(df)
        df = df[df['cod_proc_solicitado'].str.startswith("04", na=False)]
        depois = len(df)
        log_message(f" <i> Total de Linhas no arquivo {antes} | Total de linhas c/ Procedimentos '04'→ {depois}")
        if depois == 0:
            log_message(" X TODAS linhas descartadas no filtro de códigos '04'")

        df['cpf_solicitante'] = df['cpf_solicitante'].fillna('0').astype(str).str.zfill(11)

        if 'tipo_atendimento' not in df.columns:
            df['tipo_atendimento'] = ''

        # Reordenação
        if 'dt_solicitacao' in df.columns:
            dt = df.pop('dt_solicitacao')
            df.insert(1, 'dt_solicitacao', dt)

        if 'tipo_atendimento' in df.columns:
            ta = df.pop('tipo_atendimento')
            df.insert(2, 'tipo_atendimento', ta)

        # Novas colunas
        df.insert(3, 'nu_consulta', '')
        df.insert(4, 'auditado', '0')
        df.insert(5, 'nu_internacao', '')
        df.insert(6, 'ds_motivo', '')

        df['data_execucao'] = 'data'
        df['hora_execucao'] = 'hora'
        df['ds_concat'] = ''

       # Converte as colunas para texto, garantindo consistência
        df['nu_consulta'] = df['nu_consulta'].astype(str)
        df['auditado'] = df['auditado'].astype(str)
        df['nu_internacao'] = df['nu_internacao'].astype(str)
        df['ds_concat'] = df['ds_concat'].astype(str)
        df['ds_motivo'] = df['ds_motivo'].astype(str)
        df['data_execucao']= df['data_execucao'].astype(str)
        df['hora_execucao']= df['hora_execucao'].astype(str)
        df['cpf_solicitante']= df['cpf_solicitante'].astype(str)
         
        # Remover tabs
        for campo in ['ds_sinais_sint_clinicos', 'ds_result_prov_diag', 'ds_cond_just_internacao']:
            if campo in df.columns:
                df[campo] = df[campo].astype(str).str.replace('\t', ' ')

        # Preparar saída
        nome_saida = f"{caminho_arquivo.stem}.xlsx"
        caminho_saida = diretorio_xlsx_registros / nome_saida

        with pd.ExcelWriter(caminho_saida, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='LOTE')

        wb = load_workbook(caminho_saida)
        ws = wb.active

        # Alinhamento e formato numérico
        for letra in ['B', 'C', 'D', 'E']:
            for celula in ws[letra][2:]:
                celula.alignment = Alignment(horizontal='center')
                if letra == 'E':
                    celula.number_format = '0'

        # Largura das colunas
        for idx, col in enumerate(df.columns, 1):
            try:
                max_len = max(len(str(col)), df[col].astype(str).str.len().max())
            except:
                max_len = len(str(col))
            max_len += 2
            ws.column_dimensions[ws.cell(1, idx).column_letter].width = max_len

        # Forçar texto em colunas de data
        colunas_texto = ['data_execucao', 'hora_execucao', 'dt_solicitacao']
        for col in colunas_texto:
            if col in df.columns:
                idx = list(df.columns).index(col) + 1
                letra = ws.cell(1, idx).column_letter
                for celula in ws[letra]:
                    celula.number_format = '@'

        # Proteção
        todas = list(string.ascii_uppercase) + [f"A{ch}" for ch in string.ascii_uppercase[:18]]
        bloqueadas = [c for c in todas if c not in ['C', 'D', 'E', 'O', 'AE']]
        ws.protection = SheetProtection(sheet=True, password="aihv2")

        for c in bloqueadas:
            for celula in ws[c]:
                celula.protection = Protection(locked=True)

        for c in ['C', 'D', 'E', 'O', 'AE']:
            for celula in ws[c]:
                celula.protection = Protection(locked=False)

        # Formatação condicional auditado
        if 'auditado' in df.columns:
            faixa = "E2:E1048576"
            cores = {"1": "F0E68C", "2": "FF6347", "3": "2E8B57", "4": "87CEFA"}
            for val, cor in cores.items():
                regra = FormulaRule(formula=[f'E2={val}'],
                                  fill=PatternFill(start_color=cor, end_color=cor, fill_type="solid"))
                ws.conditional_formatting.add(faixa, regra)

        # Filtro automático
        cols_filtro = ['auditado', 'dt_solicitacao']
        refs = [ws.cell(1, list(df.columns).index(c) + 1).column_letter
                for c in cols_filtro if c in df.columns]
        if refs:
            ws.auto_filter.ref = f"{refs[0]}1:{refs[-1]}1"
            log_message(f"Filtro aplicado: {refs[0]}1:{refs[-1]}1")

        # Pintar linhas com erro
        if 'erros_validacao' in df.columns:
            amarelo = PatternFill(start_color="FFFF99", end_color="FFFF99", fill_type="solid")
            for idx, row in df.iterrows():
                if pd.notna(row['erros_validacao']) and row['erros_validacao'].strip():
                    for col_idx in range(1, ws.max_column + 1):
                        ws.cell(row=idx + 2, column=col_idx).fill = amarelo

        # Remover coluna erros_validacao APENAS se não houver erros
        if 'erros_validacao' in df.columns:
            tem_erros = df['erros_validacao'].str.strip().str.len().gt(0).any()
            if not tem_erros:
                df = df.drop(columns=['erros_validacao'])
                log_message("Coluna 'erros_validacao' removida (sem erros detectados)")
            else:
                log_message("Coluna 'erros_validacao' mantida (há erros para revisão)")

        wb.save(caminho_saida)
        wb.close()

        # Atualiza o último arquivo salvo
        ultimo_arquivo_salvo = caminho_saida
        log_message(f"Arquivo XLSX gerado: {caminho_saida}")

        # Mover original
        destino = diretorio_csv_registros / caminho_arquivo.name
        shutil.move(str(caminho_arquivo), destino)
        log_message(f" -> Arquivo movido para backup: {destino}")
        
        return df

    # Listar e ordenar arquivos ANTES de qualquer processamento
    arquivos_para_processar = [
        p for p in diretorio_csv.glob("*")
        if p.suffix.lower() in (".csv", ".xlsx")
    ]
    arquivos_para_processar.sort(key=lambda p: chave_ordenacao_natural(p.name))

    total_arquivos = len(arquivos_para_processar)
    
    if total_arquivos == 0:
        mostrar_mensagem("Nenhum arquivo *.CSV ou *.XLS ou *.XLSX encontrado para conversão!")
        log_message("Nenhum arquivo encontrado para processar.")
    else:
        # Abrir janela de progresso
        abrir_janela_progresso(total_arquivos)
    
    
    dfs_processados = []
    ultimo_arquivo_salvo = None
    
    #log_message(f"Encontrados {len(arquivos_para_processar)} arquivos para processar")

    for idx, caminho_arquivo in enumerate(arquivos_para_processar, 1):
            atualizar_progresso(idx, total_arquivos, caminho_arquivo.name)
            
            df = processar_arquivo(caminho_arquivo)
            if df is not None:
                dfs_processados.append(df)
                # Atualiza último arquivo salvo (dentro de processar_arquivo você já seta globalmente)
        
        # Fechar janela de progresso
    fechar_janela_progresso()

  
    # Resultado final
    if not dfs_processados:
        msg = " X - Nenhum arquivo convertido com sucesso!"
        log_message(msg)
        mostrar_mensagem(msg)
    else:
        df_final = pd.concat(dfs_processados, ignore_index=True)
        total = df_final.shape[0]
        amb = df_final[df_final.get('cd_carater_atendimento', pd.Series()) == '1'].shape[0]
        urg = df_final[df_final.get('cd_carater_atendimento', pd.Series()) == '2'].shape[0]

        msg = (
            f"Processo concluído!\n"
            f"Arquivos processados: {contador_arquivos[0]}\n"
            f"Total registros: {total}\n"
            f"Ambulatoriais: {amb}\n"
            f"Urgência/Emergência: {urg}"
        )

        log_message(msg)
        mostrar_mensagem(msg)

        # Salvar controle
        caminho_control = "./LOGS/control.txt"
        import configparser
        config = configparser.ConfigParser()
        if os.path.exists(caminho_control):
            config.read(caminho_control, encoding="utf-8")

        config["info_conversor"] = {
            "arquivos_processados": str(contador_arquivos[0]),
            "total_registros": str(total),
            "total_ambulatorial": str(amb),
            "total_urgencia": str(urg),
            "ultima_execucao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(caminho_control, "w", encoding="utf-8") as f:
            config.write(f)

        log_message(f"Log final salvo em: {log_filename}")

        # Abrir o último arquivo XLSX gerado no aplicativo padrão
        if ultimo_arquivo_salvo and ultimo_arquivo_salvo.exists():
            log_message(f"Abrindo automaticamente o último arquivo gerado: {ultimo_arquivo_salvo}")
            try:
                import time
                time.sleep(2)
                os.startfile(str(ultimo_arquivo_salvo))
            # Nova janela de orientação após abrir o Excel
                root_aviso = Tk()
                root_aviso.withdraw()  # esconde a janela raiz
                root_aviso.attributes("-topmost", True)
                
                aviso_texto = (
                    "ATENÇÃO - AUDITORIA NECESSÁRIA\n\n"
                    f"A última planilha processada foi aberta para auditoria:\n"
                    f"{ultimo_arquivo_salvo.name}\n\n"
                    "Favor realizar as seguintes ações manualmente:\n\n"
                    "1. Preencher a coluna 'nu_consulta' com o numero da consulta de origem ou de porta\n"
                    "2. Para cada registro auditado, adicionar o valor 1 na coluna 'auditado'\n\n"
                    "Após finalizar a auditoria, salve o arquivo.\n\n"
                    "O RPA-AIH-SISREG-HOSP só processará os registros que tiverem 'auditado' = 1.\n\n"
                    "Clique OK para continuar."
                )
                
                messagebox.showwarning("Auditoria Necessária", aviso_texto, parent=root_aviso)
                root_aviso.destroy()
                                       
            except Exception as e:
                log_message(f"Não foi possível abrir o arquivo automaticamente: {e}")
                mostrar_mensagem(f"Processo concluído, mas não foi possível abrir o último arquivo:\n{ultimo_arquivo_salvo}\n\n{e}")
        else:
            log_message("Nenhum arquivo XLSX foi gerado com sucesso para abrir automaticamente.")

finally:
    if lock_file_path.exists():
        lock_file_path.unlink()
    log_message("Processo finalizado. Lock removido.")