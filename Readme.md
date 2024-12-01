# Crew Agents Fii Analyzer

![image](https://github.com/user-attachments/assets/586fcf5f-a4fb-4c03-b670-bff611fc489c)


A tool to help analyze mutual fii fund reports.
AI agents will download management reports from mutual funds and answer questions about them.

## Requirements

You shuld add a .env file with OPENAI_API_KEY before use it.

## How to use

1. Install the dependencies with `pip install -r requirements.txt`
2. Add the codes of the FIIs you want to analyze to the `constants.py` file
3. Run the script with `python fii_report_analyser.py`
4. The script will download the reports of the FIIs and save them in the `reports` folder
5. The script will generate a `final_report.md` file with the results of the analysis

## Example output

O arquivo `final_report.md` terá o seguinte formato:

1. **RZTR11**

   - **Dividend Yield Anual:** 0,99%
   - **Vacância:** 15,24%
   - **WAULT:** 15,24 anos

2. **XPLG11**
   - **Dividend Yield Anual:** 7,18%
   - **Vacância:** 9,1%
   - **WAULT:** 5,7 anos
