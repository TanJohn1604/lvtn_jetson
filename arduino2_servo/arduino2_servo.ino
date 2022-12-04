/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep
*/

#include <Servo.h>

Servo myservo9; 
Servo myservo10;
// create servo object to control a servo
// twelve servo objects can be created on most boards
int counter_servo10=0;
int counter_servo9=0;



int input4;
int pre_input4;

int input5;
int pre_input5;

void setup() {
  myservo9.attach(9); 
    myservo10.attach(10); 

    TCCR0A = 0;// set entire TCCR0A register to 0
  TCCR0B = 0;// same for TCCR0B
  TCNT0  = 0;//initialize counter value to 0
  // set compare match register for 2khz increments
  OCR0A = 249;// = (16*10^6) / (249 + 1)*64  (must be <256)
  // turn on CTC mode
  TCCR0A |= (1 << WGM01);
  // Set CS01 and CS00 bits for 64 prescaler
  TCCR0B |= (1 << CS01) | (1 << CS00);   
  // enable timer compare interrupt
//  TIMSK0 |= (1 << OCIE0A);

  TCCR2A = 0;// set entire TCCR2A register to 0
  TCCR2B = 0;// same for TCCR2B
  TCNT2  = 0;//initialize counter value to 0
  // set compare match register for 8khz increments
  OCR2A = 249;// = (16*10^6) / (249 + 1)*64  (must be <256)
  // turn on CTC mode
  TCCR2A |= (1 << WGM21);
  // Set CS21 bit for 8 prescaler
  TCCR2B |= (1 << CS22);   
  // enable timer compare interrupt
//  TIMSK2 |= (1 << OCIE2A);



 myservo9.write(0);
   myservo10.write(0);
  pinMode(4, INPUT);
  pinMode(5, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);

}

ISR(TIMER0_COMPA_vect){
 counter_servo9++;
}

ISR(TIMER2_COMPA_vect){
counter_servo10++;
}

void loop() {
  
input4=digitalRead(4);
if(pre_input4== 0 && input4==1){
  myservo9.write(60);
  TCNT0  = 0;
  TIMSK0 |= (1 << OCIE0A);
}
pre_input4=input4;

input5=digitalRead(5);
if(pre_input5== 0 && input5==1 ){
  myservo10.write(60);
  TCNT2=0;
   TIMSK2 |= (1 << OCIE2A);
    digitalWrite(LED_BUILTIN,1);
}
pre_input5=input5;




//if(counter_servo10== 1000){
//  myservo10.write(60);
//  digitalWrite(LED_BUILTIN, 1);
// 
//}

if(counter_servo10== 1000){
 myservo10.write(0);
  TIMSK2 &=~ (1 << OCIE2A);
  counter_servo10=0;
  digitalWrite(LED_BUILTIN, 0);
}



//if(counter_servo9== 1000){
// myservo9.write(60);
//}

if(counter_servo9== 1000){
myservo9.write(0);
  TIMSK0 &= ~(1 << OCIE0A);
  counter_servo9=0;
}

  
}
