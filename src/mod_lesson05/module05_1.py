"""Основной модуль приложения lesson05."""

def scan_directory(path, base_path):
    """
    Рекурсивно сканирует директорию и возвращает список словарей с информацией о файлах и папках.
    """
    entries = []
    path = Path(path)

    for item in path.rglob('*'):
        if item.is_symlink():
            continue

        relative_path = item.relative_to(base_path).as_posix()
        stat = item.stat()
        mod_time = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

        if item.is_file():
            size = stat.st_size
            entries.append({
                "name": relative_path,
                "type": "file",
                "size": size,
                "modified": mod_time
            })
            # Если это ZIP-архив, извлекаем его содержимое во временный каталог
            if item.suffix.lower() == '.zip':
                with tempfile.TemporaryDirectory() as tmp_dir:
                    try:
                        with zipfile.ZipFile(item, 'r') as z:
                            z.extractall(tmp_dir)
                            # Рекурсивно сканируем извлечённое содержимое
                            entries.extend(scan_directory(tmp_dir, Path(tmp_dir)))
                    except zipfile.BadZipFile:
                        pass  # Игнорируем повреждённые архивы
        elif item.is_dir():
            entries.append({
                "name": relative_path,
                "type": "folder",
                "size": "FOLDER",
                "modified": mod_time
            })

    return entries

def generate_json_report(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_csv_report(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Type", "Size", "Modified"])
        for entry in 
            writer.writerow([entry["name"], entry["type"], entry["size"], entry["modified"]])


def generate_xlsx_report(data, output_path):
    if not XLSX_AVAILABLE:
        raise ImportError("openpyxl не установлен. Установите его командой: pip install openpyxl")

    wb = Workbook()
    ws = wb.active
    ws.title = "File Report"
    ws.append(["Name", "Type", "Size", "Modified"])
    for entry in 
        ws.append([entry["name"], entry["type"], entry["size"], entry["modified"]])
    wb.save(output_path)


def generate_docx_report(data, output_path):
    if not DOCX_AVAILABLE:
        raise ImportError("python-docx не установлен. Установите его командой: pip install python-docx")

    doc = Document()
    doc.add_heading('Отчёт о структуре файлов', 0)

    table = doc.add_table(rows=1, cols=4)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Name'
    hdr_cells[1].text = 'Type'
    hdr_cells[2].text = 'Size'
    hdr_cells[3].text = 'Modified'

    for entry in 
        row_cells = table.add_row().cells
        row_cells[0].text = entry["name"]
        row_cells[1].text = entry["type"]
        row_cells[2].text = str(entry["size"])
        row_cells[3].text = entry["modified"]

    doc.save(output_path)


def generate_pdf_report(data, output_path):
    if not PDF_AVAILABLE:
        raise ImportError("reportlab не установлен. Установите его командой: pip install reportlab")

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    title = Paragraph("Отчёт о структуре файлов", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Заголовки
    header_data = [["Name", "Type", "Size", "Modified"]]
    table_data = header_data + [[entry["name"], entry["type"], str(entry["size"]), entry["modified"]] for entry in data]
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)