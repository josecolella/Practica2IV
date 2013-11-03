#!/usr/bin/env node
/**
* Author: Jose Miguel Colella
*/

var GitHubApi = require("github");

var github = new GitHubApi({
    // required
    version: "3.0.0",
    // optional
    timeout: 5000
});

github.authenticate({
    type: "basic",
    username: process.argv[2],
    password: process.argv[3]
});

github.user.update({
    location: "Granada"
}, function(err) {
    console.log("done!");
});
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                 
