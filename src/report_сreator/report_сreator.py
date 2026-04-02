import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

class CreateExelReport:

    def create_report(self, rows: list):
        yesterday = datetime.now() - timedelta(days=1)
        file_name = f"отчет_открытых_вакансий_за_{yesterday.day}d_{yesterday.month}m_{yesterday.year}y.xlsx"
        return self._save_to_excel(file_name, rows)

    def _save_to_excel(self, file_name: str, rows: list) -> str:
        df = pd.DataFrame(rows)
        df = df.sort_values(by="Зарплата от", ascending=False)

        tmp_dir = Path("tmp")
        tmp_dir.mkdir(exist_ok=True)
        file_path = tmp_dir / file_name

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")

            worksheet = writer.sheets["Sheet1"]

            for col in worksheet.columns:
                max_length = 0
                col_letter = col[0].column_letter

                for cell in col:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass

                adjusted_width = max_length + 2
                worksheet.column_dimensions[col_letter].width = adjusted_width

        return file_path