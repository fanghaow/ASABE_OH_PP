#include <Servo.h>

#define DIR1 46
#define STP1 44
#define EN1  42
#define DIR2 49
#define STP2 51
#define EN2  53
#define DIR3 4
#define STP3 5
#define EN3  7

#define ARM1 A2
#define ARM2 2
#define PUSH 3

#define BASE A11

#define SPD 100
#define SWR 600

Servo arm1;
Servo arm2;
Servo push;

#define armoneup 85
#define armonedown 112
#define armtwoup 120
#define armtwodown 135
#define stretchout 160
#define stretchin 0

int t = 1;
String comdata = "";
String com = "";

void setup() {
  pinMode(DIR1, OUTPUT);
  pinMode(STP1, OUTPUT);
  pinMode(EN1, OUTPUT);
  pinMode(DIR2, OUTPUT);
  pinMode(STP2, OUTPUT);
  pinMode(EN2, OUTPUT);
  pinMode(DIR3, OUTPUT);
  pinMode(STP3, OUTPUT);
  pinMode(EN3, OUTPUT);
  digitalWrite(EN3, HIGH);
  
  pinMode(ARM1, OUTPUT);
  pinMode(ARM2, OUTPUT);
  pinMode(PUSH, OUTPUT);
  pinMode(BASE, INPUT);
  Serial1.begin(9600);
  Serial.begin(9600);
  while(Serial1.read()>= 0){} //clear serialbuffer

//  arm2.attach(ARM2);
//  push.attach(PUSH);
//  arm2.write(armtwodown);
//  push.write(0);
}

void GoAhead(int Step)//向前
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, LOW);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, HIGH);
    delayMicroseconds(SPD);
    digitalWrite(STP1, LOW);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD);
  }
}

void Uphands()
{
  arm1.attach(ARM1);
  arm2.attach(ARM2);
  
  arm1.write(armoneup);
  arm2.write(armtwoup);
  delay(500);
//  arm1.detach();
  arm2.detach();
}

void Downhands()
{
  arm1.attach(ARM1);
  arm2.attach(ARM2);
  arm1.write(armonedown);
  arm2.write(armtwodown);
  delay(500);
//  arm1.detach();
  arm2.detach();
}

void swirl(int Step)
{
  digitalWrite(EN3, HIGH);
  digitalWrite(DIR3, HIGH);
  for (int i = 0; i < Step; i++)
  {
    digitalWrite(STP3, HIGH);
    delayMicroseconds(SWR);
    digitalWrite(STP3, LOW);
    delayMicroseconds(SWR);
  }
}

void CheckBase()
{
  t = digitalRead(BASE);
}

void point()
{
  push.attach(PUSH);
  for (int i = stretchin; i < stretchout; i++)
  {
    push.write(i);
    delay(5);
  }
  push.detach();
}

void Rec()
{
  int i = 0;
  int j = 0;
  int con = 0;
  while(1)
  {
    // read data from serial port
    con = 0;
    i = 0;
    j = 0;
    comdata = "";
    com = "";
    while(Serial1.available())
    {
      comdata += char(Serial1.read());
      delay(2);
      con++;
    }
    if (comdata != "")
    {
      for (i = 0; i < 100; i++)
      {
        if (comdata[i] == ':')
        {
          for (j = i + 1; j < 100; j++)
          {
            if (comdata[j] == '!') break;
            com += comdata[j];
          }
          break;
        }
      }
      Serial1.print("Serial.readString:");
      Serial1.println(com);
      Serial1.println(j - i - 1);
      Serial.print("Serial.readString:");
      Serial.println(com);
//    Serial.println(j - i - 1);
    }
    while(Serial1.read()>= 0){} //clear serialbuffer
  }
}

//-----------------------------------------------------------------------

void loop() {

  Serial1.println("1");
  Uphands();
  delay(1000);

  while(1)
  {
    GoAhead(1);
    CheckBase();
    if (t == 0)
    {
      GoAhead(10);
      CheckBase();
      if (t == 0)
      { 
        delay(500);
        Serial1.println("1");
        


        
        GoAhead(2000);
      }
    }
  }
}
