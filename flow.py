from crewai.flow.flow import Flow, listen, start
from constants import MY_FIIS
from scrape_reports import FIIReportScraper
from fii_report_analyser import fiiCrew


class FiiFlow(Flow):

    @start()
    def grabFiiReports(self):
        scraper = FIIReportScraper()
        return scraper.process_fiis(MY_FIIS)

    @listen(grabFiiReports)
    def processFiiReports(self):
        for fii in MY_FIIS:
            fiiCrew.kickoff(inputs={'input': fii})


flow = FiiFlow()
response = flow.kickoff()

print(response)
