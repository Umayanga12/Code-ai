import os

class FileCRUD:
    def __init__(self, file_path):
        self.file_path = file_path

    def create(self, content):
        with open(self.file_path, 'w') as file:
            file.write(content)

    def read(self):
        with open(self.file_path, 'r') as file:
            return file.read()

    def update(self, content):
        with open(self.file_path, 'w') as file:
            file.write(content)

    def delete(self):
        os.remove(self.file_path)

    def list_files(self):
        return os.listdir(os.path.dirname(self.file_path))

    def search(self, keyword):
        with open(self.file_path, 'r') as file:
            content = file.read()
            return keyword in content
