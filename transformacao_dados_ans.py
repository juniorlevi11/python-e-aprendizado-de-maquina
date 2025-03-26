import os
import zipfile
import pdfplumber
import pandas as pd

# Caminho atualizado do PDF
pdf_path = "anexos_ans/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"

# Lista para armazenar os dados extraídos
dados_tabela = []

# Abrir o PDF e extrair a tabela
with pdfplumber.open(pdf_path) as pdf:
    for pagina in pdf.pages:
        tabelas = pagina.extract_tables()
        for tabela in tabelas:
            for linha in tabela:
                dados_tabela.append(linha)

# Criar um DataFrame Pandas
colunas = dados_tabela[0]  # Primeira linha como cabeçalho
dados_tabela = dados_tabela[1:]  # Demais linhas são os dados

df = pd.DataFrame(dados_tabela, columns=colunas)

# Substituir abreviações de OD e AMB pela descrição completa
substituicoes = {
    "OD": "Odontologia",
    "AMB": "Ambulatorial"
}

df.replace(substituicoes, inplace=True)

# Salvar em CSV
csv_path = "Rol_Procedimentos.csv"
df.to_csv(csv_path, index=False, encoding="utf-8")

# Compactar o CSV em um arquivo ZIP
zip_filename = "Teste_Levi_Alves.zip"
with zipfile.ZipFile(zip_filename, "w") as zipf:
    zipf.write(csv_path, os.path.basename(csv_path))

print(f"Processo concluído! Arquivo ZIP salvo como '{zip_filename}'")
