import os
import re
import pdfplumber
from PyPDF2 import PdfWriter, PdfReader

# Caminhos
pdf_path = r"C:\Users\trank\Documents\Estudos\python\divergencias\documento_original.pdf"
output_dir = r"C:\Users\trank\Documents\Estudos\python\divergencias\sessoes"
os.makedirs(output_dir, exist_ok=True)

# Expressão para capturar nomes de sessão (ex: DESENVOLVIMENTO HUMANO - SELEÇÃO E CAPACITAÇÃO)
padrao_sessao = re.compile(r"[A-ZÇÁÉÍÓÚÃÕÂÊÎÔÛÜ ]{5,} - [A-ZÇÁÉÍÓÚÃÕÂÊÎÔÛÜ ]{3,}")

# Função para limpar nomes inválidos para salvar como arquivo
def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', '', nome).strip()

# Identificação de páginas por sessão
sessoes_paginas = {}
sessao_atual = None

with pdfplumber.open(pdf_path) as plumber_pdf:
    total_paginas = len(plumber_pdf.pages)
    for i, page in enumerate(plumber_pdf.pages):
        print(f"🔍 Processando página {i + 1} de {total_paginas}...")

        texto = page.extract_text() or ""

        # Ignorar páginas em branco
        if not texto.strip():
            print(f"⛔ Página {i + 1} ignorada (em branco)")
            continue

        # Ignorar páginas com 'FCMS - Sorocaba' ou 'HSL - Sorocaba'
        if "FCMS - Sorocaba" in texto or "HSL - Sorocaba" in texto:
            print(f"⛔ Página {i + 1} ignorada (contém 'FCMS - Sorocaba' ou 'HSL - Sorocaba')")
            continue

        # Detectar nova sessão, se existir
        encontrados = padrao_sessao.findall(texto)
        if encontrados:
            sessao_atual = encontrados[0]
            print(f"📌 Nova sessão detectada: {sessao_atual}")

        # Adiciona a página à sessão atual (se existir)
        if sessao_atual:
            nome_limpo = limpar_nome(sessao_atual)
            if nome_limpo not in sessoes_paginas:
                sessoes_paginas[nome_limpo] = []
            sessoes_paginas[nome_limpo].append(i)

# Salvar PDFs por sessão
with open(pdf_path, "rb") as f:
