from crewai_tools import PDFSearchTool
from crewai import Agent, Crew, Task, LLM, Process
from dotenv import load_dotenv
from datetime import datetime
from constants import MY_FIIS
from custom_tools.SaveMdTool import SaveMdTool
import os
load_dotenv()

ativos = MY_FIIS

llm = LLM(
    model="gpt-4o-mini",  # model="gemini/gemini-1.5-flash",
    api_key=os.getenv('OPENAI_API_KEY')  # api_key=os.getenv('GEMINI_API_KEY')
)

pdf_search = PDFSearchTool()
write_tool = SaveMdTool()

analyst = Agent(
    llm=llm,
    role='Analista de mercado',
    goal="Obter informacoes de fundos imobiliarios",
    backstory="Sabe encontrar indicadores de fundos imobiliarios e determinar se estão bons ou não",
    verbose=True,
    tools=[pdf_search, write_tool]
)

analyse = Task(
    description="""
    Para o ativo: {input}, faca a analise e responda as seguintes perguntas:
    A informacao pode ser encontrada no pdf em reports/{input}.pdf
    Caso não consiga encontrar o pdf, ignore o ativo.

    - Ativo possui vacancia fisica e/ou financeira, quanto?
    - Qual o WAULT ou tempo médio dos contratos?
    - Há inadimplencia se sim, quanto?
    """,
    expected_output="Responder exatamente o que foi pedido na tarefa, deve apenas usar informações contidas nos textos, sem inventar",
    agent=analyst,
    tools=[pdf_search],
)

writer = Agent(
    llm=llm,
    role='Escritor de markdown',
    goal="Ira escrever em um markdown bem formatado uma analise feita por outro agente",
    backstory="Sabe escrever markdown de forma clara",
    verbose=True,
)

write = Task(
    description="""
    Use o SaveMdTool para salvar as respostas em um arquivo markdown no arquivo outputs/{input}.md
    Deve criar um arquivo por ativo
    """,
    expected_output="Escrever o markdown de forma bem simplificada, com o fii como titulo, e a lista de perguntas e respostas",
    agent=writer,
    context=[analyse],
    tools=[write_tool],
)


fiiCrew = Crew(
    manager_llm=llm,
    agents=[
        # report_getter,
        analyst,
        writer
    ],
    tasks=[
        # get_report,
        analyse,
        write
    ],
    verbose=True,
    process=Process.sequential
)
