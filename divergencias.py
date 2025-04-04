import os
import re
import pdfplumber
from PyPDF2 import PdfWriter, PdfReader

# Caminhos
pdf_path = r"C:\Users\trank\Desktop\divergencias.pdf"
output_dir = r"C:\Users\trank\Documents\Estudos\python\divergencias\sessoes"
os.makedirs(output_dir, exist_ok=True)

# Expressão para capturar nomes de sessão (em maiúsculo com hífen)
padrao_sessao = re.compile(r"[A-ZÇÁÉÍÓÚÃÕÂÊÎÔÛÜ ]{5,} - [A-ZÇÁÉÍÓÚÃÕÂÊÎÔÛÜ ]{3,}")

# Função para limpar nomes inválidos de arquivos
def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', '', nome).strip()

# Leitura do PDF
with open(pdf_path, "rb") as f:
    pdf = PdfReader(f)

    sessoes_paginas = {}  # {'nome_sessao': [lista_de_paginas]}
    sessao_atual = None

    with pdfplumber.open(pdf_path) as plumber_pdf:
        for i, page in enumerate(plumber_pdf.pages):
            texto = page.extract_text() or ""
            encontrados = padrao_sessao.findall(texto)

            if encontrados:
                sessao_atual = encontrados[0]

            if sessao_atual:
                nome_limpo = limpar_nome(sessao_atual)
                if nome_limpo not in sessoes_paginas:
                    sessoes_paginas[nome_limpo] = []
                sessoes_paginas[nome_limpo].append(i)

# Criação dos PDFs por sessão
for nome_sessao, paginas in sessoes_paginas.items():
    writer = PdfWriter()
    for p in paginas:
        writer.add_page(pdf.pages[p])
    output_path = os.path.join(output_dir, f"{nome_sessao}.pdf")
    with open(output_path, "wb") as out_f:
        writer.write(out_f)
    print(f"✅ Sessão '{nome_sessao}' salva com {len(paginas)} páginas")

print(f"\n🏁 Finalizado! Total de sessões unificadas: {len(sessoes_paginas)}")
