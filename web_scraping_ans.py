import os
import requests
import zipfile
from bs4 import BeautifulSoup
from tqdm import tqdm

# URL do site
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Criar pasta para armazenar os PDFs
pasta_downloads = "anexos_ans"
os.makedirs(pasta_downloads, exist_ok=True)

# Fazer a requisição para obter o HTML da página
response = requests.get(url)
if response.status_code != 200:
    print("Erro ao acessar a página:", response.status_code)
    exit()

# Analisar o HTML
soup = BeautifulSoup(response.text, "html.parser")

# Encontrar todos os links que contêm 'Anexo I' e 'Anexo II'
links_pdf = []
for link in soup.find_all("a", href=True):
    href = link["href"]
    if "Anexo" in href and href.endswith(".pdf"):
        links_pdf.append(href)

# Baixar os arquivos
arquivos_baixados = []
for link in links_pdf:
    nome_arquivo = os.path.join(pasta_downloads, link.split("/")[-1])
    
    # Fazer o download com barra de progresso
    with requests.get(link, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get("content-length", 0))
        with open(nome_arquivo, "wb") as f, tqdm(
            desc=nome_arquivo,
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
                bar.update(len(chunk))

    arquivos_baixados.append(nome_arquivo)

# Criar um arquivo ZIP com os PDFs baixados
zip_filename = "anexos_ans.zip"
with zipfile.ZipFile(zip_filename, "w") as zipf:
    for arquivo in arquivos_baixados:
        zipf.write(arquivo, os.path.basename(arquivo))

print(f"\nDownload concluído! Arquivos compactados em '{zip_filename}'")