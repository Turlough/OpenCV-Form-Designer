import csv
import os.path
from src.tools.pdf_page_extractor import PdfExtractor


class IndexFileManager:
    input_csv: str
    export_folder: str
    rows: list
    row_number: int = 0
    page_number: int = 0
    page_start_indexes: list[int]
    extractor: PdfExtractor

    def __init__(self, input_csv, start_indexes):
        self.input_csv = input_csv
        self.export_folder = os.path.dirname(input_csv)
        self.rows = list()
        self.page_start_indexes = start_indexes

    def read_all(self):
        self.rows.clear()
        with open(self.input_csv, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.rows.append(row)
        self.new_pdf()

    def write_all(self):
        with open(self.input_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.rows)

    def save_page_indexes(self, values):
        start = self.page_start_indexes[self.page_number]
        for i, value in enumerate(values):
            row = self.rows[self.row_number]
            # Add one because col 1 is an image path
            col = 1 + start + i
            row[col] = value
        self.write_all()

    def load_index_value(self, local_col_num):
        # Add one, because first index is path
        col = 1 + local_col_num + self.page_start_indexes[self.page_number]
        return self.rows[self.row_number][col]

    def get_page_image(self):
        return self.extractor.get_page(self.page_number)

    def next_row(self):
        self.row_number += 1
        self.page_number = 0
        self.new_pdf()

    def new_pdf(self):
        row = self.rows[self.row_number]
        pdf = row[0]
        path = os.path.join(self.export_folder, pdf)
        self.extractor = PdfExtractor(path)

    def prev_page(self):
        self.page_number -= 1

    def next_page(self):
        self.page_number += 1

    def get_start_indexes(self, template_folder):
        pass

