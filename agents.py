from crewai_tools import WebsiteSearchTool
from crewai import Agent, Crew, Task, LLM
from dotenv import load_dotenv
from datetime import datetime


import os
load_dotenv()

ativos = ['RZTR11', 'XPLG11']
llm = LLM(
    model="gemini/gemini-1.5-flash",
    # api_key=os.getenv('GEMINI_API_KEY')
)

# llm = LLM(
#     model="gpt-4o-mini",
#     api_key=os.getenv('OPENAI_API_KEY')
# )


scrape = WebsiteSearchTool()


researcher = Agent(
    llm=llm,
    role="Buscador de indicadores",
    goal="Encontrar os indicadores solicitados de um FII",
    backstory="Especialista em juntar dados da internet",
    verbose=True
)


analyst = Agent(
    llm=llm,
    role='Analista de mercado',
    goal="Resumir um relatorio gerencial",
    backstory="Expert analista de mercado",
    verbose=True
)

research = Task(
    description="""
    Buscar os dados mais atualizados possiveis dos indicadores, a data de hoje é: {current_date}
    Os seguintes ativos devem ser pesquisados: {input}

    Confirme se os dados estao corretos e atualizado usando pelo menos duas fontes, como...
    https://statusinvest.com.br/fundos-imobiliarios/NOME_DO_ATIVO
    https://investidor10.com.br/fiis/NOME_DO_ATIVO


    Obrigatoriamente é necessario encontrar os seguintes dados:
        - Cotaçao atual
        - P/VP
        - Vacancia
        - Ultimo Dividendo
    """,
    expected_output="Obter indicadores atualizados do ativo solicitado",
    agent=researcher,
    tools=[scrape]
)


write = Task(
    description='Fazer um breve relatorio sobre os Fiis bem formatado em markdown dos seguintes ativos: {input} ',
    expected_output=f""" Deve gerar um texto onde cada linha represente um ativo do FII com os seguintes dados:
        - Cotaçao atual
        - P/VP
        - Vacancia
        - Ultimo Dividendo,
        - Link do site consultado
        Sem adição de qualquer dado adicional, como observações, traga apenas o que foi pedido.
    """,
    agent=analyst,
    context=[research],
    output_file='report.md',
)

crew = Crew(
    agents=[
        researcher,
        analyst,
    ],
    tasks=[
        research,
        write
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
