from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import requests
from pathlib import Path
import re
from datetime import datetime
from typing import List, Tuple, Optional
from constants import MY_FIIS


class FIIReportScraper:
    source_base_url = 'https://fiis.com.br'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/pdf,*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': source_base_url
    }

    def __init__(self, output_dir: str = "reports"):
        """
        Inicializa o scraper de relatórios de FIIs.

        Args:
            output_dir: Diretório onde os relatórios serão salvos
        """
        self.output_dir = Path(output_dir)
        self.driver = None

    def setup_driver(self) -> None:
        """Configura o driver do Chrome em modo headless."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)

    def _is_pdf(self, content: bytes) -> bool:
        return content.startswith(b'%PDF')

    def _is_html(self, content: bytes) -> bool:
        text_content = content.decode('utf-8', errors='ignore')
        return '<html' in text_content or '<!DOCTYPE' in text_content

    def save_pdf(self, content: bytes, save_path: Path) -> bool:
        with open(save_path, 'wb') as f:
            f.write(content)
        return True

    def download_pdf(self, url: str, save_path: Path) -> bool:
        """
        Baixa um PDF de uma URL e salva no caminho especificado.

        Args:
            url: URL do PDF
            save_path: Caminho onde o PDF será salvo

        Returns:
            bool: True se o download foi bem sucedido, False caso contrário
        """
        try:
            print(f"\nBaixando PDF de: {url}")

            verify = False if 'bmfbovespa.com.br' in url else True
            if not verify:
                import urllib3
                urllib3.disable_warnings(
                    urllib3.exceptions.InsecureRequestWarning)

            response = requests.get(url, headers=self.headers, verify=verify)

            if response.status_code == 200:
                content = response.content
                if self._is_pdf(content):
                    return self.save_pdf(content, save_path)

                if self._is_html(content):
                    pdf_match = re.search(
                        r'href=[\'"]([^\'"]*\.pdf)[\'"]', content.decode('utf-8', errors='ignore'))
                    pdf_url = pdf_match.group(1)
                    return self.download_pdf(pdf_url, save_path)

                print(f"❌ Erro ao baixar PDF. Status: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Erro ao baixar {url}: {str(e)}")
            if 'content' in locals():
                print(f"Primeiros bytes recebidos: {content[:100]}")
            return False

    def get_report_links(self, fii_code: str) -> List[Tuple[str, str]]:
        """
        Obtém os links dos relatórios gerenciais de um FII.

        Args:
            fii_code: Código do FII (ex: XPLG11)

        Returns:
            List[Tuple[str, str]]: Lista de tuplas (data, url) dos relatórios
        """
        url = f'{self.source_base_url}/{fii_code.lower()}'
        print(f"\nAcessando {url}")
        self.driver.get(url)

        time.sleep(2)

        try:
            relatorios_link = self.driver.find_element(
                By.XPATH, "//a[normalize-space(text())='Relatórios, Relatório Gerencial']")
            print("✓ Encontrado link 'Relatórios, Relatório Gerencial'")

            href = relatorios_link.get_attribute('href')
            if href and 'fnet.bmfbovespa.com.br/fnet/publico/' in href:
                date = datetime.now().strftime('%d/%m/%Y')
                print(f"✓ Encontrado link do relatório gerencial: {href}")
                return [(date, href)]
            else:
                print("❌ Link encontrado não é um PDF da B3/FNET")

        except Exception as e:
            print(f"❌ Erro ao buscar relatório gerencial: {str(e)}")

        return []

    def process_fii(self, fii: str) -> List[Tuple[str, Path]]:
        """
        Processa um FII, baixando seus relatórios gerenciais.

        Args:
            fii: Código do FII (ex: XPLG11)

        Returns:
            List[Tuple[str, Path]]: Lista de tuplas (data, caminho) dos relatórios baixados
        """
        print(f'\n{"="*50}')
        print(f'Processando {fii}...')
        print(f'{"="*50}')

        downloaded_reports = []
        links = self.get_report_links(fii)

        print(f'Encontrados {len(links)} relatórios para {fii}')

        for i, (date, link) in enumerate(links, 1):
            print(f'\n[{i}/{len(links)}] Processando relatório de {date}')

            # Salvar com o nome do FII
            pdf_path = self.output_dir / f"{fii}.pdf"

            if self.download_pdf(link, pdf_path):
                downloaded_reports.append((date, pdf_path))
                print(f'✓ Relatório {i}/{len(links)} processado com sucesso')
            else:
                print(f'❌ Falha ao processar relatório {i}/{len(links)}')

        print(f'\nResumo para {fii}:')
        print(f'Total de relatórios encontrados: {len(links)}')
        print(f'Total de relatórios baixados: {len(downloaded_reports)}')
        print(f'{"="*50}\n')

        return downloaded_reports

    def process_fiis(self, fiis: List[str]) -> dict:
        """
        Processa uma lista de FIIs, baixando os relatórios de cada um.

        Args:
            fiis: Lista de códigos de FIIs

        Returns:
            dict: Dicionário com os resultados do processamento de cada FII
        """
        try:
            self.setup_driver()
            results = {}

            for fii in fiis:
                downloaded_reports = self.process_fii(fii)
                results[fii] = downloaded_reports

            return results

        finally:
            if self.driver:
                self.driver.quit()


def main():
    fiis = MY_FIIS
    scraper = FIIReportScraper()
    results = scraper.process_fiis(fiis)
    print('Pdfs salvos')


if __name__ == '__main__':
    main()
