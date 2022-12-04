#include <Servo.h>
#define numOfValsRec 3
#define digitsPerValRec 3
int valsRec[numOfValsRec];
int PrevalsRec[numOfValsRec];
int stringLength=numOfValsRec*digitsPerValRec+1;
int counter =0;
bool counterStart=false;
String receivedString;

String myS="123,456";
int flag=1;




Servo myservo_chai;
Servo myservo_can;
void setup() {
PrevalsRec[0]=valsRec[0]=000;
PrevalsRec[1]=valsRec[1]=111;
PrevalsRec[2]=valsRec[2]=222;
Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);
pinMode(4, OUTPUT);
pinMode(5, OUTPUT);
digitalWrite(4, 0); 
digitalWrite(5, 0); 
myservo_chai.attach(9); 
myservo_can.attach(10); 
myservo_chai.write(0);  
myservo_can.write(0);  
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


digitalWrite(4, valsRec[0]==1 ); 
digitalWrite(5, valsRec[0]==2);

//-----------------------------end do something -------------------------------
}
