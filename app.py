from scrape_reports import FIIReportScraper
from typing import List, Dict
import json
from pathlib import Path

class CrewInvestorFlow:
    def __init__(self):
        """Inicializa o flow do Crew Investor."""
        self.fiis = [
            # FIIs de Logística
            "XPLG11",  # XP Log
            "VILG11",  # Vinci Logística
            "HGLG11",  # CSHG Logística
            
            # FIIs de Tijolo Comercial
            "RBRP11",  # RBR Properties
            "HGRE11",  # CSHG Real Estate
            "VIUR11",  # Vinci Imóveis Urbanos
            
            # FIIs de Recebíveis
            "RZTR11",  # Riza Terrax
            "KNIP11",  # Kinea Índice de Preços
            "KNCR11",  # Kinea Rendimentos
        ]
        self.scraper = FIIReportScraper()
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)
    
    def step1_download_reports(self) -> Dict:
        """
        Passo 1: Download dos relatórios gerenciais dos FIIs.
        
        Returns:
            Dict: Dicionário com os resultados do download para cada FII
        """
        print("\n=== Passo 1: Download dos Relatórios Gerenciais ===")
        results = self.scraper.process_fiis(self.fiis)
        
        # Salvar os resultados em markdown
        self.scraper.save_to_markdown(results)
        
        # Salvar metadados dos downloads
        metadata = {
            fii: [{"date": date, "path": str(path)} for date, path in reports]
            for fii, reports in results.items()
        }
        
        with open(self.results_dir / "reports_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        return results

def main():
    """Função principal que executa o flow do Crew Investor."""
    flow = CrewInvestorFlow()
    
    # Passo 1: Download dos relatórios
    results = flow.step1_download_reports()
    
    print("\n=== Flow Completo ===")
    print("Resultados salvos em:")
    print("- reports/: PDFs dos relatórios")
    print("- reports/reports_links.md: Links dos relatórios")
    print("- results/reports_metadata.json: Metadados dos downloads")

if __name__ == "__main__":
    main()
