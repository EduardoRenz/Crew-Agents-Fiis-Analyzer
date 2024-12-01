from crewai_tools import BaseTool


class SaveMdTool(BaseTool):
    name: str = "SaveMdTool"
    description: str = "Salva o conteudo de texto em um arquivo, parametros: output, output_file"

    def _run(self, output: str, output_file: str) -> None:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
