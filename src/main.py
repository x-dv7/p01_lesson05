"""Main модуль приложения lesson05."""

import argparse
from pathlib import Path
from mod_lesson05.module05_1 import scan_directory
from mod_lesson05.module05_1 import generate_json_report
from mod_lesson05.module05_1 import generate_csv_report
from mod_lesson05.module05_1 import generate_xlsx_report
from mod_lesson05.module05_1 import generate_docx_report
from mod_lesson05.module05_1 import generate_pdf_report

def main():
    """Main функция приложения lesson05."""
    # Парсинг аргументов
    parser = argparse.ArgumentParser(description="Генератор отчёта о структуре файлов и папок")
    parser.add_argument("--path", 
                        type=str, 
                        default="D:/project/_tmp_dir", 
                        required= False, 
                        help="Путь к анализируемой папке")
    parser.add_argument("--report", 
                        type=str, 
                        default="./report.pdf", 
                        required=False, 
                        help="Путь к файлу отчёта (с расширением)")

    args = parser.parse_args()

    # Получение аргументов
    report_path = Path(args.report)
    print(f"Путь к отчету '{report_path}'.")
    output_format = report_path.suffix.lower()[1:]  # Расширение без точки. 
    print(f"Формат отчета '{output_format}'.")
    # Проверка формата
    allowed_formats = {'json', 'csv', 'xlsx', 'docx', 'pdf'}
    if output_format not in allowed_formats:
        print(f"Ошибка: формат '{output_format}' не поддерживается. Поддерживаемые: {', '.join(allowed_formats)}")
        return
    # Проверка пути сканируемой папки
    source_path = Path(args.path)
    if not source_path.exists():
        print(f"Ошибка: путь '{source_path}' не существует.")
        return

    print(f"Сканирование папки: {source_path}")
    # Сканирование папки
    data = scan_directory(source_path, source_path)
    # Генерация отчета
    print(f"Генерация отчёта в формате: {output_format}")
    if output_format == 'json':
        generate_json_report(data, report_path)
    elif output_format == 'csv':
        generate_csv_report(data, report_path)
    elif output_format == 'xlsx':
        generate_xlsx_report(data, report_path)
    elif output_format == 'docx':
        generate_docx_report(data, report_path)
    elif output_format == 'pdf':
        generate_pdf_report(data, report_path)

    print(f"Отчёт сохранён: {report_path}")

if __name__ == "__main__":
    main()
