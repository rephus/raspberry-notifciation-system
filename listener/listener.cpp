/*
Description:
  NRF24L01 server
  
Dependency: 
  RF24 for raspberry PI : https://github.com/TMRh20/RF24/tree/master/RPi
  Install using make && sudo make install
  
Documentation:
  RF24: https://github.com/TMRh20/RF24
  Example: http://hack.lenotta.com/arduino-raspberry-pi-switching-light-with-nrf24l01/
  Onefinestay example: https://github.com/onefinestay/looserver
  
How to run: 
  g++ -L/usr/local/lib/ -lstdc++ -lrt -lrf24-bcm rf24.cpp -o rf24.out
  
Harware configuration:

  NRF24L01:
  __________________
  |_1_| 2         ~ |
  | 3 | 4  [_]    ~ |
  | 5 | 6         ~ |
  | 7 | 8  (   )  ~ |
  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ 
  Raspberry PI:
  
  1 -> 3.3v
  2 -> GND
  3 -> 22
  4 -> CS0
  5 -> SCLK
  6 -> MOSI
  7 -> MISO
  
*/

#include <iostream> //for usleep
#include <time.h> //for CLOCK_REALTIME
#include <RF24/RF24.h> //for radio
#include <stdio.h> //for printf

#include <sqlite3.h>
#include <string>

using namespace std;

// Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 8Mhz
RF24 radio(RPI_V2_GPIO_P1_15, RPI_V2_GPIO_P1_24, BCM2835_SPI_SPEED_8MHZ);

// Radio pipe addresses for the 2 nodes to communicate.
const uint8_t pipes[][6] = {"1Node","2Node"};

static int callback(void *NotUsed, int argc, char **argv, char **azColName){
   return 0;
}

string toString(int number){
  if (number == 0) return "0";
  string temp="";
  string returnvalue="";
  while (number>0) {
      temp+=number%10+48;
      number/=10;
  }
  for (int i=0;i<temp.length();i++)
      returnvalue+=temp[temp.length()-i-1];
  return returnvalue;
}

int main(int argc, char** argv){
  
  printf("Starting rf24 server with sqlite3");
          
  timespec time;
  // for some reason read() reads 8 bytes, not 1, so make sure we allocate
  // enough memory; otherwise it scribbles over other memory
  int paylad[8];
  sqlite3 *db;
  int rc;
  char *zErrMsg = 0;
  string sql;
  
  radio.begin();
  radio.setChannel(1);
  radio.setRetries(15,15);
  radio.printDetails();

  radio.openWritingPipe(pipes[1]);
  radio.openReadingPipe(1,pipes[0]);
  radio.startListening();

  rc = sqlite3_open("/var/sqlite/rf24.db", &db);

   if( rc ){
      fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
   } else{
      printf( "Opened database successfully\n");
      sql = "CREATE TABLE IF NOT EXISTS readings ("  \
         "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL," \
         "timestamp NUMERIC NOT NULL," \
         "value NUMERIC NOT NULL," \
         "device TEXT);";
   
      rc = sqlite3_exec(db, sql.c_str(), callback, 0, &zErrMsg);
      if( rc != SQLITE_OK ){
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
      }else{
        printf( "Schema initialized successfully\n");
      }

   }
   
  while (1) {

    if ( radio.available() ) {      

      radio.read( paylad, sizeof(int) );
      int value = paylad[0];
      clock_gettime(CLOCK_REALTIME, &time);
       printf("Received: %i at %i.%i \n",value,time.tv_sec,time.tv_nsec);
      
      sql = "INSERT INTO readings (timestamp, value) "  \
         "VALUES ("+toString(time.tv_sec)+", "+toString(value) +"); ";
      rc = sqlite3_exec(db, sql.c_str(), callback, 0, &zErrMsg);
      if( rc != SQLITE_OK ){
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
      }else{
        printf( "Reading stored successfully\n");
      }
    }
    usleep(100 * 1000);
  } 
  
  sqlite3_close(db);
}