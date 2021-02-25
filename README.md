cloudinn
=========

Pre-interview technical assessment task!
:License: MIT

Project Description
^^^^^^^^^^^^^^^^^^^^^

Using Python or Golang write a command line program which takes an Age of Empires || unit
name as a user input and search for information about this unit then render this unit’s data to
the user.
Use this API endpoint to retrieve the age of empires || units data
https://tasks.cloudinn.net/docs/
All the data retrieved from the API endpoint should be stored locally in a database of your
choosing to minimize the amount of requests made to the API.
The code should be delivered on a public github repository. Undocumented code will be
disregarded. Along with the code you must include a guide on how to setup and use the
application.


Project Setup
^^^^^^^^^^^^^

To run the project on local machine you have to setup python3 and postgresql first::

    $ sudo -u postgres psql
    $ postgres=# create database cloudinndb;
    $ postgres=# create user cloudinnuser with encrypted password 'password';
    $ postgres=# grant all privileges on database mydb to cloudinnuser;
    $ postgres=# \q
    $ git clone https://github.com/AbdelrahmanRabiee/cloudinn-task.git
    $ mkdir venv/
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ python cloudinn.py



