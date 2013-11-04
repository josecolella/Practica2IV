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

var http = require('http'),
    util = require('util'),
    fs = require('fs'),
    url = require('url'),
    qs = require('querystring'),
    GitHubApi = require("github");

var server = http.createServer(function (req,res){

    var url_parts = url.parse(req.url,true);
    //console.log(url_parts);

    var body = '';
    if(req.method === 'POST'){
       // res.end('post');
       console.log('Request found with POST method');
        req.on('data', function (data) {
            body += data;
            console.log('got data:'+data);
        });
        req.on('end', function () {

            var POST = qs.parse(body);
            // use POST
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
              username: POST.name,
              password: POST.password
            });

            //Cambiamos el lugar usando update
            github.user.update({
              location: "Granada"
            }, function(err) {
              console.log("Cambio Hecho!");
            });
            res.end("Cambio hecho para indicar ubicación en Granada");

        });


    } else {
    console.log('Request found with GET method');
    req.on('data',function(data){ res.end(' data event: '+data);});
    if(url_parts.pathname == '/')

    fs.readFile('./form.html',function(error,data){
    console.log('Serving the page form.html');
    res.end(data);
    });

    else if(url_parts.pathname == '/getData'){
         console.log('Serving the Got Data.');
        getData(res,url_parts);
    }
        }

});
server.listen(8080);
console.log('Server listening on http://localhost/8080');



function  getData(res,url_parts){

 console.log("Data submitted by the user name:"+url_parts.query.name+" and age:"+url_parts.query.password);
        res.end("Data submitted by the user name:"+url_parts.query.name+" and age:"+url_parts.query.password);

}