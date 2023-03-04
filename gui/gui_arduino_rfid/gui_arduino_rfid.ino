#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
 
#define RST_PIN         9
#define SS_PIN          10

#define numOfValsRec 3
#define digitsPerValRec 1

Servo servo_roi;//94 to 10
Servo servo_huong;//90 to 170



int valsRec[numOfValsRec]={};
int stringLength=numOfValsRec*digitsPerValRec+1;
int counter =0;
bool counterStart=false;
String receivedString;
int flag=1;

unsigned char UID[4];
 int a=0;
MFRC522 mfrc522(SS_PIN, RST_PIN);
int buttonState=0;
void setup() 
{
pinMode(2, INPUT);
servo_roi.attach(3); 


servo_roi.write(94);
delay(5000);
servo_huong.attach(5);
servo_huong.write(90);



    Serial.begin(9600);   

    SPI.begin();    
    mfrc522.PCD_Init();


}

void receiveData(){
if(flag==0){
 
  while (Serial.available()){
    //Serial.println(__LINE__);
    char c = Serial.read();
    if (c=='$'){
      counterStart=true;
    }
    if (counterStart){
      if(counter<stringLength){
        receivedString=String(receivedString+c);
      counter++;
      }
      if(counter>=stringLength){
       for (int i=0;i<numOfValsRec;i++){
        int num=(i*digitsPerValRec)+1;
        valsRec[i]=receivedString.substring(num,num+digitsPerValRec).toInt();
       }
       receivedString="";
       counter=0;
       counterStart=false;
      }
    }
    flag=1;
  }
  Serial.flush();

  }
}


void loop() 
{  
  buttonState = digitalRead(2);


  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  { 
//    return;
    goto endloop;
  }
  
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {  
//    return;
    goto endloop;
  }
  
//  Serial.print("UID của thẻ: ");   
  
  for (byte i = 0; i < 4; i++) 
  { 
//    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
       
    UID[i] = mfrc522.uid.uidByte[i];
  }

 
  if(flag==1){

Serial.print(UID[0]);
Serial.print(",");
Serial.print(UID[1]);
Serial.print(",");
Serial.print(UID[2]);
Serial.print(",");
Serial.println(UID[3]);
//Serial.print(",");
//Serial.println(buttonState);
Serial.flush();
flag=0;

  }

  
  mfrc522.PICC_HaltA();  
  mfrc522.PCD_StopCrypto1();
goto endloop2;
  
endloop:;

if(flag==1){

Serial.print(0);
Serial.print(",");
Serial.print(0);
Serial.print(",");
Serial.print(0);
Serial.print(",");
Serial.println(0);
//Serial.print(",");
//Serial.println(buttonState);
Serial.flush();
flag=0;

  }

endloop2:;
receiveData();

//-----------------------------do something -------------------------------
//
//
if(valsRec[0] == 1){
 servo_huong.write(90);
}
else{
 servo_huong.write(170);
}


if(valsRec[1] == 1){
 servo_roi.write(10);
}
else{
 servo_roi.write(94);
}



}
