from crewai_tools import BaseTool
from typing import List
import os


class DirectoryListTool(BaseTool):
    name: str = "Directory List Tool"
    description: str = "Le o conteudo de todos os arquivos no diretório reports, quando o diretorio estiver vazio, uma mensagem de diretorio vazio"

    def _run(self, *args, **kwargs) -> str:
        directory = os.listdir('reports')
        if len(directory) == 0:
            return 'Diretório vazio'
        return '\n'.join(directory)
