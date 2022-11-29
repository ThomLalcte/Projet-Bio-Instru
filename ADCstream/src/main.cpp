#include <Arduino.h>
#include <WiFi.h>
#include <driver/timer.h>

#define AP

#ifndef AP
  const char* ssid     = "";
  const char* password = "";
#else
  const char *ssid = "HP2545 printer";
#endif

WiFiServer server(12345);

hw_timer_t * timer = NULL;
uint8_t sampleFlag = 0;
#define fs 1000
#define ledPin GPIO_NUM_13
uint8_t ledFlag = 0;

#define qteBuffers 3
#define buffersSize 32
uint8_t currentBuffer = 0;
uint8_t currentSample = 0;
uint16_t buffers[qteBuffers][buffersSize];
uint16_t* readiedBuffer = nullptr;

void IRAM_ATTR onTimer(){
  sampleFlag++;
}

void sampleRoutine(){
  buffers[currentBuffer][currentSample] = analogRead(34);
  currentSample++;
  if (currentSample>=buffersSize) readiedBuffer = buffers[currentBuffer];
  currentBuffer+=currentSample>=buffersSize;
  currentSample*=currentSample<buffersSize;
  currentBuffer*=currentBuffer<qteBuffers;
  sampleFlag--;
}

void setup()
{
    Serial.begin(115200);
    
    timer = timerBegin(0, 80, true);
    timerAttachInterrupt(timer, &onTimer, true);
    timerAlarmWrite(timer, 1000000/fs, true);

    pinMode(ledPin,OUTPUT);

    #ifndef AP
      Serial.println();
      Serial.println();
      Serial.print("Connecting to ");
      Serial.println(ssid);
      WiFi.begin(ssid, password);
      while (WiFi.status() != WL_CONNECTED) {
          delay(500);
          Serial.print(".");
      }
      Serial.println("");
      Serial.println("WiFi connected");
      Serial.println("IP address: ");
      Serial.println(WiFi.localIP());
    #else
      WiFi.mode(WIFI_AP);
      WiFi.softAP(ssid);
      IPAddress myIP = WiFi.softAPIP();
      Serial.print("AP IP address: ");
      Serial.println(myIP);
    #endif

    server.begin();
    timerAlarmEnable(timer);
}


void loop() {

  // digitalWrite(ledPin,1);
  WiFiClient client = server.available();
 
  if (client) {
    Serial.println("Client connected");
    while (client.connected()) {
      if (sampleFlag>0) sampleRoutine();

      if (readiedBuffer!=nullptr) {
        client.write((char*)readiedBuffer,2*buffersSize);
        readiedBuffer=nullptr;
        ledFlag+=(micros()%250)==0;
        digitalWrite(ledPin,ledFlag>0);
      }
 
    }
    digitalWrite(ledPin,0);
    client.stop();
    Serial.println("Client disconnected");
 
  }
}