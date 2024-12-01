from crewai_tools import PDFSearchTool, tool,FileWriterTool
from crewai import Agent, Crew, Task, LLM
from dotenv import load_dotenv
from datetime import datetime
from constants import MY_FIIS
from custom_tools.ReportDownloadTool import ReportDownloadTool
from custom_tools.DirectoryListTool import DirectoryListTool
from custom_tools.SaveMdTool import SaveMdTool
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
write_tool = SaveMdTool()


report_getter = Agent(
    llm=llm,
    role='Buscador de Relatorio',
    goal=""""
    - Verifique se há um pdf com o relatório na pasta.
    - Caso não existir, tente fazer o download
    Se mesmo assim não for possivel encontrar o relatório, no report final para este ativo, diga que não foi encontrado.
    
    Pode ser que para alguns ativos exista o pdf e outros nao, saiba determinar qual falta para fazer o download se precisar.
    A ferramente download sempre espera uma lista de ativos, mesmo que exista epenas um.
    """,
    backstory="Organizador de relatórios",
    verbose=True,
    tools=[directory_list_tool, report_downloader]
)

analyst = Agent(
    llm=llm,
    role='Analista de mercado',
    goal="Responder exatamente o que foi pedido na tarefa",
    backstory="Expert analista de mercado",
    verbose=True,
    tools=[pdf_search,write_tool]
)


get_report = Task(
    description="""
    Para cada ativo: {input}, pode haver um pdf com o caminho reports/NOME_ATIVO.pdf
    Verifique se todos os arquivos existem, use o Directory List Tool.
    Caso não exista, use o tool Report Download Tool para baixar os pdfs inexistentes.
    """,
    expected_output="Ter certeza de que todos os relatorios dos fiis solicitados estao disponiveis",
    agent=report_getter,
    tools=[directory_list_tool, report_downloader],
)

research = Task(
    description="""
    Para cada ativo: {input}, faca a analise e responda as seguintes perguntas:
    A informacao pode ser encontrada nos pdfs disponiveis na pasta reports
    Cada ativo contem um relatorio, exemplo:
    reports/NOME_ATIVO.pdf
    
    - Ativo possui vacancia fisica e/ou financeira, quanto?
    - Qual o WAULT ou tempo médio dos contratos?
    - Há inadimplencia?

    Por fim use o SaveMdTool para salvar as respostas em um arquivo markdown no arquivo outputs/NOME_DO_FII.md
    Deve criar um arquivo por ativo
    """,
    expected_output="Responder exatamente o que foi pedido na tarefa",
    agent=analyst,
    tools=[pdf_search,write_tool],
    
)



crew = Crew(
    agents=[
       # report_getter,
        analyst,
    ],
    tasks=[
        #get_report,
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
