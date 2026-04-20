import pandas as pd

class DataUtil:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_excel(self, sheet_name=0):
        data = pd.read_excel(self.file_path, sheet_name=sheet_name)
        return data.to_dict(orient='records')

    def read_csv(self):
        data = pd.read_csv(self.file_path)
        return data.to_dict(orient='records')