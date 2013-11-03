#!/usr/bin/env node

// Copyright (C) 2013  Jose Miguel Colella
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
//(at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.


//Importo el modulo para interactuar con github
//https://github.com/ajaxorg/node-github
var GitHubApi = require("github");

var github = new GitHubApi({
    // required
    version: "3.0.0",
    // optional
    timeout: 5000
  });

//El usuario se autentifica con los
//nombre de usuario de github y contraseña
github.authenticate({
  type: "basic",
  username: process.argv[2],
  password: process.argv[3]
});

//Cambiamos el lugar usando update
github.user.update({
  location: "Granada"
}, function(err) {
  console.log("Cambio Hecho!");
});