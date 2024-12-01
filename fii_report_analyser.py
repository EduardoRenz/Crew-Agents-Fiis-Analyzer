from crewai_tools import PDFSearchTool, tool
from crewai import Agent, Crew, Task, LLM
from dotenv import load_dotenv
from datetime import datetime
from constants import MY_FIIS
from custom_tools.ReportDownloadTool import ReportDownloadTool
from custom_tools.DirectoryListTool import DirectoryListTool
import os
load_dotenv()

ativos = MY_FIIS
# llm = LLM(
#     model="gemini/gemini-1.5-flash",
#     # api_key=os.getenv('GEMINI_API_KEY')
# )

llm = LLM(
    model="gpt-4o-mini",
    api_key=os.getenv('OPENAI_API_KEY')
)

pdf_search = PDFSearchTool()
directory_list_tool = DirectoryListTool()
report_downloader = ReportDownloadTool()

report_getter  = Agent(
    llm=llm,
    role='Buscador de Relatorio',
    goal=""""Garantir que exista os relatorios para o analista de mercado, ira checar o diretorio se existe o pdf, caso nao ache, vai baixar.
    
    Pode ser que para alguns ativos exista o pdf e outros nao, saiba determinar qual falta para fazer o download se precisar.

    A ferramente download sempre espera uma lista de ativos, mesmo que exista epenas um.

    """,
    backstory="Organizador de relatórios",
    verbose=True,
    tools=[directory_list_tool,report_downloader]
)
get_report = Task(
    description="""
    Para cada ativo: {input}, pode haver um pdf com o caminho reports/NOME_ATIVO.pdf
    Verifique se todos os arquivos existem, use o Directory List Tool.
    Caso não exista, use o tool Report Download Tool para baixar os pdfs inexistentes.
    """,
    expected_output="Ter certeza de que todos os relatorios dos fiis solicitados estao disponiveis",
    agent=report_getter,
    tools=[directory_list_tool,report_downloader],
)

analyst = Agent(
    llm=llm,
    role='Analista de mercado',
    goal="Responder exatamente o que foi pedido na tarefa",
    backstory="Expert analista de mercado",
    verbose=True,
    tools=[pdf_search]
)



research = Task(
    description="""
    Para cada ativo: {input}, faca a analise e responda as seguintes perguntas:
    A informacao pode ser encontrada nos pdfs disponiveis na pasta reports
    Cada ativo contem um relatorio, exemplo:
    reports/NOME_ATIVO.pdf

    ## NOME_DO_ATIVO
    Pergunta: Qual o Dividend Yield anual do ativo?:
    Pergunta: Ativo possui vacancia, qual percentual?
    Pergunta: Qual o WAULT ou tempo médio dos contratos?


    """,
    expected_output="Obter indicadores atualizados do ativo solicitado",
    agent=analyst,
    tools=[pdf_search],
    output_file='final_report.md',
)


crew = Crew(
    agents=[
        report_getter,
        analyst,
    ],
    tasks=[
        get_report,
        research,
    ],
    verbose=True,
)


foreach_inputs = []

for ativo in ativos:
    foreach_inputs.append({
        'input': ativo,
        'current_date': datetime.now().strftime('%d/%m/%Y')
    })

# Execute tasks
crew.kickoff(
    inputs={'input': ativos, 'current_date': datetime.now().strftime('%d/%m/%Y')})
