#include <Servo.h>
#define numOfValsRec 3
#define digitsPerValRec 3
int valsRec[numOfValsRec];
int stringLength=numOfValsRec*digitsPerValRec+1;
int counter =0;
bool counterStart=false;
String receivedString;

String myS="123,456";
int flag=1;




Servo myservo_red;
Servo myservo_blue;
void setup() {
valsRec[0]=000;
valsRec[1]=111;
valsRec[2]=222;
Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);

myservo_red.attach(9); 
myservo_blue.attach(10); 
myservo_red.write(0);  
myservo_blue.write(0);  
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


void loop() {



if(flag==1){
myS="";
//Serial.println(__LINE__);
myS=String(valsRec[0]+','+valsRec[1]+','+valsRec[2]);
Serial.print(valsRec[0]);
Serial.print(",");
Serial.print(valsRec[1]);
Serial.print(",");
Serial.println(valsRec[2]);
Serial.flush();
flag=0;

  }

receiveData();

//-----------------------------do something -------------------------------


//-----------------------------end do something -------------------------------
}
