#!/usr/bin/env python
# coding: utf-8

import json
import os

import requests
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict


class _MissingRequiredParameter(Exception):

    def __init__(self,
                 arg_name,
                 env_var_name,
                 object_type,
                 message='Missing a required Parameter'):
        self.arg_name = arg_name
        self.env_var_name = env_var_name
        self.message = message
        self.object_type = object_type
        super().__init__(self.message)

    def __str__(self):
        return f'Missing a valid {self.arg_name.replace("_", " ")}! Either ' \
        f'pass it to the {self.object_type} as: `{self.arg_name}=...`, or ' \
        f'set it as an environment variable: `{self.env_var_name}`.'


class Gotify:

    def __init__(self,
                 host_address=None,
                 fixed_token=None,
                 fixed_priority=None):
        self.host_address = host_address
        self.fixed_token = fixed_token
        self.fixed_priority = fixed_priority

    @staticmethod
    def _headers():
        headers = CaseInsensitiveDict()
        headers['Content-type'] = 'application/json'
        return headers

    def _get_host_address(self):
        host_address = self.host_address
        if not host_address and not os.getenv('GOTIFY_HOST_ADDRESS'):
            raise _MissingRequiredParameter('host_address',
                                            'GOTIFY_HOST_ADDRESS',
                                            'class instance')
        else:
            if not host_address:
                host_address = os.getenv('GOTIFY_HOST_ADDRESS')
        if 'http' not in host_address:
            raise TypeError(
                'Missing a valid scheme in the host address (e.g., `http://`)!'
            )
        return host_address

    def create_app(self, admin_username, admin_password, app_name, desc=None):
        host_address = self._get_host_address()
        url = f'{host_address}/application'
        data = json.dumps({'name': app_name, 'description': desc})
        auth = HTTPBasicAuth(admin_username, admin_password)
        resp = requests.post(url,
                             headers=self._headers(),
                             data=data,
                             auth=auth)
        return resp.json()

    def push(self, title, message, token=None, priority=2):

        if not token:
            token = self.fixed_token
            if not token:
                token = os.getenv('GOTIFY_APP_TOKEN')
        host_address = self.host_address

        if self.fixed_priority:
            priority = self.fixed_priority

        data = {'title': title, 'message': message, 'priority': priority}

        if not token and not os.getenv('GOTIFY_APP_TOKEN'):
            raise _MissingRequiredParameter('token', 'GOTIFY_APP_TOKEN',
                                            'method')

        host_address = self._get_host_address()

        url = f'{host_address}/message?token={token}'
        resp = requests.post(url,
                             headers=self._headers(),
                             data=json.dumps(data))

        try:
            return resp.json()
        except json.decoder.JSONDecodeError as e:
            logger.exception(e)
        except requests.exceptions.ConnectionError as e:
            logger.exception(e)
