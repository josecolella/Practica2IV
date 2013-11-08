#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2013  Jose Miguel Colella
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Para interactuar con Github
# Modulo encontrado en https://github.com/michaelliao/githubpy
from github import *
# Para obtener parametros de la linea de comando
import sys


class IVIssues:

    """
    Clase que interactua con las APIs de Github para crear issues
    en el repositorio de la asignatura (GII-2013)
    """

    def __init__(self, username, password):
        """
        El constructor de la clase, en el cual se
        autentifica el usuario con sus credenciales de github

        @param1 username Nombre de usuario de github
        @param2 password Codigo Cifrado de github
        """
        self.username = username
        self.password = password
        # Nos autentificamos en el sistema
        self.gh = GitHub(username=self.username, password=self.password)

    def createIssue(self, titulo, cuerpo, assignee=None, labels=None):
        """
        Metodo usado para crear un issue en el repositorio de
        la asignatura IV (GII-2013)

        Para crear un issue se requiere dos parametros: el titulo
        y el cuerpo. Opcionalmente se puede asignar a un usuario con
        un tercer parametro

        El parametro details puede contener información sobre a quien esta asignado
        la label
        Ejemplo de uso:
        python IVIssues user userpassword "create" "Problema" "El ejecutable esta mal"
        """
        if assignee is None and labels is None:
            # Crea un issue en el repositorio
            self.gh.repos('IV-GII')('GII-2013').issues.post(
                title=titulo, body=cuerpo)
        else:
            self.gh.repos('IV-GII')('GII-2013').issues.post(
                title=titulo,
                body=cuerpo,
                assignee=assignee,
                labels=labels)

    def editIssue(self, titulo, cuerpo, assignee=None):
        """
        Metodo usado para editar un issue en el repositorio de
        la asignatura IV (GII-2013)

        Para editar un issue se requiere dos parametros: el titulo
        y el cuerpo. Opcionalmente se puede asignar a un usuario con
        un tercer parametro

        Ejemplo de uso:
        python IVIssues user userpassword "edit" "Problema con make" "make esta mal hecho"
        """
        issue = self.gh.repos('IV-GII')('GII-2013').issues.get()
        issueNum = issue[0]['number']
        if assignee is not None:
            self.gh.repos('IV-GII')('GII-2013').issues(
                issueNum).patch(title=titulo, body=cuerpo)
        else:
            self.gh.repos('IV-GII')('GII-2013').issues(
                issueNum).patch(title=titulo, body=cuerpo, assignee=assignee)

    def getOpenIssues(self):
        """
        Metodo usado para visualizar los issues abiertos
        del repositorio de la asignatura (GII-2013)

        Ejemplo de uso:
        python IVIssues user userpassword "get"
        """
        listJSON = self.gh.repos('IV-GII')(
            'GII-2013').issues.get(state="open")
        issueList = []
        for i in listJSON:
            issueList.append([i['title'], i['body']])
        return issueList

if __name__ == '__main__':
    # try:
        iv = IVIssues(sys.argv[1], sys.argv[2])
        if sys.argv[3] == "create":
            if len(sys.argv) == 8:
                iv.createIssue(
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
            else:
                iv.createIssue(sys.argv[4], sys.argv[5])
        elif sys.argv[3] == "edit":
            if len(sys.argv) == 7:
                iv.editIssue(sys.argv[4], sys.argv[5], sys.argv[6])
            else:
                iv.editIssue(sys.argv[4], sys.argv[5])
        elif sys.argv[3] == "get":
            if len(sys.argv) == 5:
                print(iv.getOpenIssues(sys.argv[4]))
            else:
                print(iv.getOpenIssues())
    #except Exception:
    #    print("Error: Numero de argumentos invalido")
    #    print(u"Example: python IVissue[nombre de usuario][contraseña][get | create | edit][args]")
