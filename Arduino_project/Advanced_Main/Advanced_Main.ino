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

#define armoneup 89 //85
#define armonepos 77
#define armonedown 112
#define armtwoup 115 //120
#define armtwopos 123
#define armtwodown 80
#define stretchout 130
#define stretchin 0

int t = 1;
String comdata = "";
String com = "";
int n = 0;
int c[10] = {0};
int sita = 0;

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

void PointPose()
{
  arm1.attach(ARM1);
  arm2.attach(ARM2);
  
  arm1.write(armonepos);
  arm2.write(armtwopos);
  delay(500);
//  arm1.detach();
  arm2.detach();
}

void swirl(int Step)
{
  digitalWrite(EN3, HIGH);
  digitalWrite(DIR3, LOW);
  for (int i = 0; i < Step; i++)
  {
    digitalWrite(STP3, HIGH);
    delayMicroseconds(SWR);
    digitalWrite(STP3, LOW);
    delayMicroseconds(SWR);
    sita++;
  }
}

void CheckBase()
{
  t = digitalRead(BASE);
}

void Point()
{
  push.attach(PUSH);
  for (int i = stretchin; i < stretchout; i++)
  {
    push.write(i);
    delay(5);
  }
  for (int i = stretchout; i > stretchin; i--)
  {
    push.write(i);
    delay(2);
  }
  push.detach();
}

void Rec()
{
  c[10] = {0};
  while(1)
  {
   // read data from serial port
    int con = 0;
    int i = 0;
    int j = 0;
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
      for (i = 0; i < con; i++)
      {
        if (comdata[i] == ':')
        {
          for (j = i + 1; j < con; j++)
          {
            if (comdata[j] == '!') break;
            com += comdata[j];
          }
          break;
        }
      }
//      Serial1.print("Serial.readString:");
//      Serial1.println(com);
//      Serial1.println(j - i - 1);
      Serial.print("Serial.readString:");
      Serial.println(com);
//      Serial.println(j - i - 1);
      String str = "09";
      n = com[0] - str[0];
      int k = 0;
//      c[10] = {0};
      int m = 1;
      while(k < n)
      {
        int s = 0;
        while (com[m] >= str[0] && com[m] <= str[1])
        {
          s = s * 10 + (com[m] - str[0]);
          m++;
        }
        if (s != 0)
        {
          c[k] = s;
          k++;
        }
        m++;
      }
      for (int i = 0; i < n; i++)
      {
        Serial.print(c[i]);
        Serial.print("   ");
      }
      break;
    }
    while(Serial1.read()>= 0){} //clear serialbuffer
  }
}

void sort()
{
  int temp = 0;
  for (int i = 0; i < n; i++)
  {
    for (int j = i + 1; j < n; j++)
    {
      if (c[j] < c[i])
      {
        temp = c[j];
        c[j] = c[i];
        c[i] = temp;
      }
    }
  }
}

void Acture()
{
  int flag = 0;
  for (int i = 0; i < n; i++)
  {
    if (flag == 0)
    {
      flag = 1;
      swirl(int(c[i] * 8.889));
      Point();
    }
    else
    {
      swirl(int((c[i] - c[i - 1]) * 8.889));
      Point();
    }
    
  }
}

void setback()
{
  digitalWrite(EN3, HIGH);
  digitalWrite(DIR3, HIGH);
  for (int i = sita; i > 0; i--)
  {
    digitalWrite(STP3, HIGH);
    delayMicroseconds(SWR);
    digitalWrite(STP3, LOW);
    delayMicroseconds(SWR);
    sita--;
  }
}

//-----------------------------------------------------------------------

void loop() {
  Serial1.println("1");
  Uphands();
  delay(1000);
  int count = 0;
  while(count < 12)
  {
    GoAhead(1);
    CheckBase();
    if (t == 0)
    {
      GoAhead(2);
      CheckBase();
      if (t == 0)
      { 
        delay(1000);
        Serial1.println("1");
        delay(500);
        PointPose();
        Rec();
        sort();
        Acture();
        setback();
        Uphands();
        
        count++;
        GoAhead(2000);
      }
    }
  }
}
