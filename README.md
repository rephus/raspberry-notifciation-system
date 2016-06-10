This repo contains all you need to build a Raspberry PI notification system 
using RF24 readings.

The project is splitted in 3 different scripts:

## listener.cpp

Reads from the RF24 radio and store the values in sqlite.

### Dependencies

TODO

### Usage

* Compile

    make 

* Run

    ./listener.out
    
## notify.py

Run in background, periodically check if sensor values are valid and home is not empty,
send emails otherwise.

## web.py

Webserver in flask, show values stores in database.

### Dependencies

    sudo apt-get install nmap

    pip install -r requirements.txt

* / : Show latest values and MAC's phone status
* /graphs : Show graphs of the latest readings


