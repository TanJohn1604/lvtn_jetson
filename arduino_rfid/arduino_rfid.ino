#include <SPI.h>
#include <MFRC522.h>

 
#define RST_PIN         9
#define SS_PIN          10

#define numOfValsRec 1
#define digitsPerValRec 3
int valsRec[numOfValsRec];
int stringLength=numOfValsRec*digitsPerValRec+1;
int counter =0;
bool counterStart=false;
String receivedString;
int flag=1;

unsigned char UID[4];
 int a=0;
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() 
{
//   pinMode(LED_BUILTIN, 3);
    Serial.begin(9600);   

    SPI.begin();    
    mfrc522.PCD_Init();
//    cli();//stop interrupts
//
// 
//    TCCR1A = 0;// set entire TCCR1A register to 0
//  TCCR1B = 0;// same for TCCR1B
//  TCNT1  = 0;//initialize counter value to 0
//  // set compare match register for 1hz increments
//  OCR1A = 15624;// = (16*10^6) / (1*1024) - 1 (must be <65536)
//  // turn on CTC mode
//  TCCR1B |= (1 << WGM12);
//  // Set CS12 and CS10 bits for 1024 prescaler
//  TCCR1B |= (1 << CS12) | (1 << CS10);  
//  // enable timer compare interrupt
//  TIMSK1 |= (1 << OCIE1A);
//
//  
//  sei();//allow interrupts

}
//ISR(TIMER1_COMPA_vect){//timer1 interrupt 1Hz toggles pin 13 (LED)
//
//  digitalWrite(3, a=!a); 
//}
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
Serial.flush();
flag=0;

  }

endloop2:;
receiveData();

//-----------------------------do something -------------------------------

}
