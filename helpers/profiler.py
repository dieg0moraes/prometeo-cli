import os
import configparser

from pathlib import Path
from exceptions import ProviderNotFound

class Profiler():

    def __init__(self):
        home = str(Path.home())
        self._directory = f'{home}/.prometeo'
        self._config_path = f'{self._directory}/configuration.ini'
        self._credentials_path = f'{self._directory}/credentials.ini'

    def initialize(self):
        if not self._exists_directory():
            self._create_directory()

        if not self._exists_configurations():
            self._create_config_file()

        if not self._exists_profile_file():
            self._create_profile_file()

    def _exists_directory(self):
        return os.path.isdir(self._directory)

    def _create_directory(self):
        os.mkdir(self._directory)

    def _exists_configurations(self):
        return os.path.isfile(self._config_path)

    def _create_config_file(self):
        with open(self._config_path, 'a') as fs:
            fs.write('[example]\n')
            fs.write('api_key=12345\n')

    def _exists_profile_file(self):
        return os.path.isfile(self._credentials_path)


    def _create_profile_file(self):
        with open(self._credentials_path, 'a') as fs:
            fs.write('[test]\n')
            fs.write('username=1234\n')
            fs.write('password=12345\n')

    def get_credentials(self, provider):
        config = configparser.ConfigParser()
        config.read(self._credentials_path)
        if provider not in config.sections():
            raise ProviderNotFound(f'{provider} not found configuration for this provider')

        return (config[provider]['username'], config[provider]['password'])

    def get_configuration(self, profile):
        config = configparser.ConfigParser()
        config.read(self._config_path)
        if profile not in config.sections():
            raise Exception(profile, 'Does not exists')

        return config[profile]['api_key']




