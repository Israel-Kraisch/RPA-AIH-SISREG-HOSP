# pyinstaller --onefile --windowed --icon=IMG/AIH-PRONT.ico MENUV7.2.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# Caminhos configuráveis
pasta_raiz = Path(".")
pasta_lotes = Path("LOTES")
pasta_bkp = Path("LOTES/BKP")
pasta_logs_extracao = Path("LOGS/EXTRACAO")
pasta_logs_automacao = Path("LOGS/AUTOMACAO")  # Assumindo pasta para logs do RPA
manual_pdf_path = Path("MANUAL/manual.pdf")  # Caminho para o manual PDF

# Scripts externos
conversor_exe = "CONVERSOR-AIH-v11.exe"  # Nome do script do conversor
rpa_exe = "RPA-AIH-SISREG-HOSPv7.2.exe"  # Nome do script do RPA principal

botao_conversor = None  # será definido na criação dos botões

def verificar_arquivos_disponiveis():
    """Verifica se há arquivos válidos na pasta raiz e habilita botão do conversor"""
    arquivos = [p for p in pasta_raiz.glob("*") if p.suffix.lower() in (".csv", ".xls", ".xlsx")]
    if arquivos and botao_conversor:
        botao_conversor.config(state=tk.NORMAL)
        messagebox.showinfo(f"Existem arquivos pendentes",f"Arquivos para conversão detectados ({len(arquivos)})")
    else:
        if botao_conversor:
            botao_conversor.config(state=tk.DISABLED)
        messagebox.showinfo("Arquivo indisponível", f"Nenhum arquivo válido para conversão \n encontrado na pasta raiz")

def subir_arquivo():
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione arquivo para conversão",
        filetypes=[("Arquivos suportados", "*.csv *.xls *.xlsx")]
    )
    if caminho_arquivo:
        destino = pasta_raiz / Path(caminho_arquivo).name
        try:
            shutil.copy(caminho_arquivo, destino)
            messagebox.showinfo("Upload Concluído", f"Arquivo copiado: {destino.name}")
            # Após copiar, verifica e habilita o botão do conversor
            verificar_arquivos_disponiveis()
        except Exception as e:
            messagebox.showerror("Erro no Upload", f"Falha ao copiar arquivo:\n{e}")

def executar_conversor():
    if not Path(conversor_exe).exists():
        messagebox.showerror("Erro", f"Executável do Conversor não encontrado:\n{conversor_exe}")
        return

    try:
        subprocess.run([conversor_exe], check=True)
        messagebox.showinfo("Conversor", "Conversor executado com sucesso!")
        # Após conversor, habilita o RPA (se quiser manter essa lógica)
        botao_rpa.config(state=tk.NORMAL)
        # Atualiza verificação (caso o conversor tenha movido arquivos)
        verificar_arquivos_disponiveis()
    except Exception as e:
        messagebox.showerror("Erro no Conversor", f"Falha ao executar:\n{e}")


def executar_rpa():
    if not Path(rpa_exe).exists():
        messagebox.showerror("Erro", f"Executável do RPA não encontrado: {rpa_exe}")
        return

    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo XLSX auditado",
        initialdir=pasta_lotes,
        filetypes=[("Excel files", "*.xlsx")]
    )
    if not caminho:
        return

    try:
        # Chama o .exe e passa o caminho do arquivo como argumento (se o RPA aceitar)
        # Se o RPA NÃO aceitar argumentos, remova o "caminho" da lista
        subprocess.run([rpa_exe, caminho], check=True)
        messagebox.showinfo("RPA", "RPA executado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro no RPA", f"Falha ao executar RPA:\n{e}")

def ver_logs(tipo):
    pasta = pasta_logs_extracao if tipo == "extracao" else pasta_logs_automacao
    if pasta.exists():
        os.startfile(str(pasta))
    else:
        messagebox.showerror("Erro", "Pasta de logs não encontrada!")

def abrir_manual():
    if manual_pdf_path.exists():
        os.startfile(str(manual_pdf_path))
    else:
        messagebox.showerror("Erro", "Manual PDF não encontrado!")

# Janela principal do menu
root = tk.Tk()
root.title("Menu Interativo RPA-AIH-SISREG-HOSP - v7.2")
root.geometry("500x400")
root.resizable(False, False)

tk.Label(root, text="Menu Interativo RPA-AIH-SISREG-HOSP v7.2", font=("Arial", 14, "bold")).pack(pady=20)

botao_subir = tk.Button(root, text="💾 1. Buscar arquivo para Conversão", command=subir_arquivo)
botao_subir.pack(pady=10, fill=tk.X, padx=50)

botao_conversor = tk.Button(root, text="🔄️ 2. Executar Conversor", command=executar_conversor, state=tk.DISABLED)
botao_conversor.pack(pady=10, fill=tk.X, padx=50)

botao_rpa = tk.Button(root, text="🤖 3. Executar RPA-AIH-SISREG-HOSP", command=executar_rpa, state=tk.DISABLED)
botao_rpa.pack(pady=10, fill=tk.X, padx=50)

tk.Button(root, text="4. Ver Logs de Conversão / Extração", command=lambda: ver_logs("extracao")).pack(pady=10, fill=tk.X, padx=50)

tk.Button(root, text="5. Ver Logs de Automação / Execução do RPA", command=lambda: ver_logs("automacao")).pack(pady=10, fill=tk.X, padx=50)

tk.Button(root, text="6. Abrir Manual PDF", command=abrir_manual).pack(pady=10, fill=tk.X, padx=50)

# Botão extra opcional: Atualizar manualmente
tk.Button(root, text="Atualizar lista de arquivos", command=verificar_arquivos_disponiveis).pack(pady=5)

# Verificação inicial ao abrir o menu
verificar_arquivos_disponiveis()

root.mainloop()