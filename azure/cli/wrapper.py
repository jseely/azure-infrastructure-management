#!/usr/bin/env python3
import os

from azure.cli.core.application import APPLICATION, Configuration
from azure.cli.core._session import ACCOUNT, CONFIG, SESSION
from azure.cli.core._environment import get_config_dir
from azure.cli.core.util import CLIError

def initialize_client():
    azure_folder = get_config_dir()
    if not os.path.exists(azure_folder):
        os.makedirs(azure_folder)
    ACCOUNT.load(os.path.join(azure_folder, 'azureProfile.json'))
    CONFIG.load(os.path.join(azure_folder, 'az.json'))
    SESSION.load(os.path.join(azure_folder, 'az.sess'), max_age=3600)

    APPLICATION.initialize(Configuration())

def execute(command):
    try:
        ex_result = APPLICATION.execute(command)
        return {
            'result': ex_result.result,
            'error': None
        }
    except CLIError as err:
        return {
            'result': None,
            'error': err.args
        }

initialize_client()
