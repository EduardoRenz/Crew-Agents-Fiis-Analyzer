from crewai_tools import PDFSearchTool
from crewai import Agent, Crew, Task, LLM
from dotenv import load_dotenv
from datetime import datetime

import os
load_dotenv()

ativos = ['PVBI11']
# llm = LLM(
#     model="gemini/gemini-1.5-flash",
#     # api_key=os.getenv('GEMINI_API_KEY')
# )

llm = LLM(
    model="gpt-4o-mini",
    api_key=os.getenv('OPENAI_API_KEY')
)

pdf_search = PDFSearchTool()

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
    Para cada ativo: {input}, há um pdf com o caminho reports/NOME_ATIVO.pdf
    Gere um markdown com o seguinte formato:

    # Relatório de {current_date}
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
        analyst,
    ],
    tasks=[
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
