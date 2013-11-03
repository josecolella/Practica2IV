#!/usr/bin/env python
# Author: Jose Miguel Colella


# Para interactuar con Github
from github import *
# Para obtener parametros de la linea de comando
import sys


class IVIssues:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # Nos autentificamos en el sistema
        self.gh = GitHub(username=self.username, password=self.password)

    def createIssue(self, titulo, cuerpo, assignee=None):
        if not assignee:
            # Crea un issue en el repositorio
            self.gh.repos('IV-GII')('GII-2013').issues.post(
                title=titulo, body=cuerpo)
        else:
            self.gh.repos('IV-GII')('GII-2013').issues.post(
                title=titulo, body=cuerpo, assignee=assignee)

    def editIssue(self, titulo, cuerpo, assignee=None):
        issue = self.gh.repos('IV-GII')('GII-2013').issues.get()
        issueNum = issue[0]['number']
        if not assignee:
            self.gh.repos('IV-GII')('GII-2013').issues(
                issueNum).patch(title=titulo, body=cuerpo)
        else:
            self.gh.repos('IV-GII')('GII-2013').issues(
                issueNum).patch(title=titulo, body=cuerpo, assignee=assignee)

    def getIssues(self):
        listJSON = self.gh.repos('IV-GII')(
            'GII-2013').issues.get(state="open")
        issueList = []
        for i in listJSON:
            issueList.append([i['title'], i['body']])
        return issueList

if __name__ == '__main__':
        iv = IVIssues(sys.argv[1], sys.argv[2])
        if sys.argv[3] == "create":
            if len(sys.argv) == 7:
                iv.createIssue(sys.argv[4], sys.argv[5], sys.argv[6])
            else:
                iv.createIssue(sys.argv[4], sys.argv[5])
        elif sys.argv[3] == "edit":
            if len(sys.argv) == 7:
                iv.editIssue(sys.argv[4], sys.argv[5], sys.argv[6])
            else:
                iv.editIssue(sys.argv[4], sys.argv[5])
        elif sys.argv[3] == "get":
            if len(sys.argv) == 5:
                print(iv.getIssues(sys.argv[4]))
            else:
                print(iv.getIssues())
