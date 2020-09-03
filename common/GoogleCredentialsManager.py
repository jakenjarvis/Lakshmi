#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from google.oauth2 import service_account
import googleapiclient.discovery

class GoogleCredentialsManager():
    def __init__(self, json_data, scopes):
        self.__json_data = json_data
        self.__scopes = scopes

        self.__credentials = None
        self.__services = {}

    @property
    def credentials(self):
        return self.__credentials

    @property
    def services(self):
        return self.__services

    def getCredentials_FromServiceAccount(self):
        # Service Account 認証
        self.__credentials = service_account.Credentials.from_service_account_info(self.__json_data, scopes=self.__scopes)
        return self

    def getService(self, serviceName, version):
        apiId = serviceName + ":" + version
        if apiId in self.__services:
            service = self.__services[apiId]
        else:
            service = googleapiclient.discovery.build(serviceName, version, credentials=self.__credentials)
            self.__services[apiId] = service
        return service
