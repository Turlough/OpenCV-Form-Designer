from src.models.form_page import FormPage

json_file = r"C:\_PV\forms\SKM_C250i2408161348002.json"


def load_json(path):
    with open(path, 'r') as file:
        content = file.read()
        page: FormPage = FormPage.from_json(content)
        for a in page.answers:
            print(a.name)


if __name__ == '__main__':
    load_json(json_file)


