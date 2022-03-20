import os

from pathlib import Path
from exceptions import ExistsSessionException

class SessionHandler:

    def __init__(self):
        home = str(Path.home())
        self._path = f'{home}/.prometeorc'
        self._session_key = 'PROMETEO_SESSION'


    def _create_file(self):
        home = str(Path.home())
        try:
            file = open(self._path, 'x')
            file.close()
        except Exception as e:
            print(e)


    def _exists_file(self):
        try:
            with open(self._path) as a:
                return True
        except FileNotFoundError:
            return False

    def _open_file_x(self):
        return open(self._path)

    def _open_file_w(self):
        return open(self._path, 'w')

    def _open_file_r(self):
        return open(self._path, 'r')


    def _create_file_if_not_exists(self):
        if not self._exists_file():
           return self._create_file();

    def exists_session(self) -> bool:
        if self._exists_file():
            try:
                with self._open_file_r() as fs:
                    lines = fs.readlines()
                    line = lines[0]
                    (key, session) = line.split('=')
                    return key == self._session_key
            except Exception:
                print('File exists but no session registered')
                return False

        return False


    def create_session(self, value):
        if self.exists_session():
            raise ExistsSessionException('')

        try:
            self._create_file_if_not_exists()
            with self._open_file_w() as fs:
                fs.write(f'{self._session_key}={value}')
        except Exception as e:
            pass

    def end_session(self):
        session = self.retrieve_session()
        os.remove(self._path)
        return session



    def retrieve_session(self):
        with self._open_file_r() as fs:
            lines = fs.readlines()
            line = lines[0]
            (key, session) = line.split('=')
            assert key == self._session_key
            return session


