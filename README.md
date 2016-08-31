# AsianWordAnalyzer 
[![Build Status](https://travis-ci.org/jbfiot/AsianWordAnalyzer.svg?branch=master)](https://travis-ci.org/jbfiot/AsianWordAnalyzer) 
[![Coverage Status](https://coveralls.io/repos/github/jbfiot/AsianWordAnalyzer/badge.svg?branch=master)](https://coveralls.io/github/jbfiot/AsianWordAnalyzer?branch=master)

Tool to "hack" Asian languages and discover related words. 

Designed by language learners for language learners.

Supported languages: 

* Korean
* Thai


## Installation notes for developers

Here is an example to install local version of the AsianWordAnalyzer.

* Git clone `AsianWordAnalyzer`

* Install `apache2`, activate `cgi`, configure (typical configuration below, `/etc/apache2/sites-enabled/000-default.conf` on linux), and restart


```
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /home/jbfiot/source/AsianWordAnalyzer/asian_word_analyzer
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

<Directory /home/jbfiot/source/AsianWordAnalyzer/asian_word_analyzer/>
    Options +ExecCGI
    IndexOptions +Charset=UTF-8
    AddHandler cgi-script .py
    Require all granted
</Directory>
```

* Install python and required packages

## Run

* Open `http://localhost/awa.py` in your browser

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/jbfiot/AsianWordAnalyzer.git)
