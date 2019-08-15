import requests
import bs4


class WebParser:

    @staticmethod
    def find_csrf(html,
                  logs=False):
        soup = bs4.BeautifulSoup(html, "lxml")
        csrf = soup.find(type='hidden')['value']  # finding csrf token
        if logs:
            print("CSRF successfully found: {}".format(str(csrf)))
        return csrf

    @staticmethod
    def authentication(url="http://torrentov.pythonanywhere.com",
                       login='parser',
                       password='parse',
                       logs=False):
        s = requests.Session()
        csrf = WebParser.find_csrf(s.get(url).text, logs=logs)

        s.post(url, {"login": login, "pass": password, "csrfmiddlewaretoken": csrf})  # authentication

        if logs:
            print("Authentication completed...")

        return s

    @staticmethod
    def upload_file(path,
                    session,
                    file,
                    url="http://torrentov.pythonanywhere.com",
                    logs=False):
        upload_url = url + "/files/upload?folder=needed_files/" + path
        csrf = WebParser.find_csrf(session.get(upload_url).text, logs=logs)
        with open(file, 'rb') as file:
            data = {"csrfmiddlewaretoken": csrf}
            session.post(upload_url, data=data, files={'docfile': file})

        if logs:
            print("File successfully uploaded...")

    @staticmethod
    def delete_file(session,
                    path,
                    url="http://torrentov.pythonanywhere.com",
                    logs=False):
        delete_url = url + "/files/delete_file/file_remove?delete=needed_files/" + path

        session.get(delete_url)

        if logs:
            print("File successfully deleted...")

    @staticmethod
    def delete_folder(session,
                      path,
                      url="http://torrentov.pythonanywhere.com",
                      logs=False):

        delete_url = url + "/files/delete_folder/folder_remove?delete=/" \
                           "home/Torrentov/file_server/files/static/needed_files/" + path

        session.get(delete_url)

        if logs:
            print("Folder successfully deleted...")

    @staticmethod
    def create_folder(session,
                      name,
                      path,
                      url="http://torrentov.pythonanywhere.com",
                      logs=False):
        create_url = url + "/files/mkdir?folder=/home/Torrentov/file_server/files/static/needed_files/" + path
        csrf = WebParser.find_csrf(session.get(create_url).text, logs=logs)
        data = {"csrfmiddlewaretoken": csrf, "folder": name}
        session.post(create_url, data=data)

        if logs:
            print("File successfully uploaded...")

    @staticmethod
    def rename(session,
               name,
               path,
               url="http://torrentov.pythonanywhere.com",
               logs=False):

        create_url = url + "/files/rename?current_name=/home/Torrentov/" \
                           "file_server/files/static/needed_files/" + path
        csrf = WebParser.find_csrf(session.get(create_url).text, logs=logs)
        data = {"csrfmiddlewaretoken": csrf, "name": name}
        s = session.post(create_url, data=data)
        print(s.text)

        if logs:
            print("File successfully uploaded...")

    @staticmethod
    def download_file(session,
                      path,
                      url="http://torrentov.pythonanywhere.com",
                      logs=False):
        download_url = url + '/static/needed_files/' + path


