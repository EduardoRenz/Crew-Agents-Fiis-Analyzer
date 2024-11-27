from scrape_reports import FIIReportScraper
from typing import List, Dict
import json
from pathlib import Path

fiis = [
    # FIIs de Logística
    "XPLG11",  # XP Log
    # FIIs de Recebíveis
    "RZTR11",  # Riza Terrax
]

class CrewInvestorFlow:
    def __init__(self):
        """Inicializa o flow do Crew Investor."""
        self.scraper = FIIReportScraper()
        Path("reports").mkdir(exist_ok=True)
    
    def step1_download_reports(self) -> Dict:
        """
        Passo 1: Download dos relatórios gerenciais dos FIIs.
        
        Returns:
            Dict: Dicionário com os resultados do download para cada FII
        """
        print("\n=== Passo 1: Download dos Relatórios Gerenciais ===")
        results = self.scraper.process_fiis(fiis)
        return results

def main():
    """Função principal que executa o flow do Crew Investor."""
    flow = CrewInvestorFlow()
    
    # Passo 1: Download dos relatórios
    results = flow.step1_download_reports()
    
    print("\n=== Flow Completo ===")
    print("Relatórios salvos em reports/")

if __name__ == "__main__":
    main()
