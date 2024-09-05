import csv


class IndexFileManager:
    input_csv: str
    rows: list
    row_number: int = 0
    page_number: int = 0
    page_start_indexes: list[int]
    image_path: str

    def __init__(self, input_csv):
        self.input_csv = input_csv
        self.rows = list()
        self.page_start_indexes = [0, 13]  # TODO

    def read_all(self):
        self.rows.clear()
        with open(self.input_csv, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.rows.append(row)

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

    def load_page_indexes(self, num_fields):
        start = self.page_start_indexes[self.page_number]
        row = self.rows[self.row_number]
        result = list()
        for i in range(num_fields):
            col = start + i
            value = row[col]
            result.append(value)
        return result

    def load_index_value(self, local_col_num):
        # Add one, because first index is path
        col = 1 + local_col_num + self.page_start_indexes[self.page_number]
        return self.rows[self.row_number][col]
