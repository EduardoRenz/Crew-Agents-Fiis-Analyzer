from crewai_tools import BaseTool
from scrape_reports import FIIReportScraper
from typing import List

class ReportDownloadTool(BaseTool):
    name: str = "Report Download Tool"
    description: str = """Faz o download dos pdfs dado uma lista de códigos de FIIs, exemplo: ['XPTO11', 'XPTI11'].
        Só é possivel enviar uma lista com o códigio dos fiis
    """

    def _run(self, fiis: List[str]) -> None:
        scraper = FIIReportScraper()
        results = scraper.process_fiis(fiis)
        print('Pdfs salvos')
