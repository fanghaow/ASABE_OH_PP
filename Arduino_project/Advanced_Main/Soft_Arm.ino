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

#define BASE 9

#define SPD 100
#define SWR 300

Servo arm1;
Servo arm2;
Servo push;

#define armoneup 89 //watchpos
#define armonepos 79
#define armonedown 168
#define armtwoup 108 //watchpos
#define armtwopos 122
#define armtwodown 53

#define stretchleaf 130
#define stretchflower 80
#define stretchin 0

class DATA
{
  public:
  int sita = 0;
  char kind = 'c';
};

int t = 1;
String comdata = "";
String com = "";
int n = 0;
DATA c[10];
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
  arm1.write(armonedown);
  arm2.write(armtwodown);
  int i = armonedown;
  int j = armtwodown;
  while(i > armonedown - 20)
  {
    arm1.write(i);
    i--;
    delay(20);
  }
  while(i > armoneup || j < armtwoup)
  {
    if (i > armoneup)
    {    
      i--;
      arm1.write(i);
    }
    if (j < armtwoup)
    {
      j++;
      arm2.write(j);
    }
    delay(20);
  }
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
  
  int i, j = 0;
  for (i = armoneup, j = armtwoup; i > armonepos, j < armtwopos; i--, j++)
  {
    arm1.write(i);
    arm2.write(j);
    delay(20);
  }
  for (i = armoneup - (armtwopos - armtwoup); i > armonepos; i--)
  {
    arm1.write(i);
    delay(20);
  }
//  arm1.detach();
  arm2.detach();
}

void WatchPose()
{
  arm1.attach(ARM1);
  arm2.attach(ARM2);
  
  int i, j = 0;
  for (i = armonepos, j = armtwopos; i < armoneup, j > armtwoup; i++, j--)
  {
    arm1.write(i);
    arm2.write(j);
    delay(20);
  }
  for (i = armonepos + (armtwopos - armtwoup); i < armoneup; i++)
  {
    arm1.write(i);
    delay(20);
  }
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

void PointLeaf()
{
  push.attach(PUSH);
  for (int i = stretchin; i < stretchleaf; i++)
  {
    push.write(i);
    delay(5);
  }
  for (int i = stretchleaf; i > stretchin; i--)
  {
    push.write(i);
    delay(2);
  }
  push.detach();
}

void PointFlower()
{
  push.attach(PUSH);
  for (int i = stretchin; i < stretchflower; i++)
  {
    push.write(i);
    delay(5);
  }
  for (int i = stretchflower; i > stretchin; i--)
  {
    push.write(i);
    delay(2);
  }
  push.detach();
}

void Rec()
{
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
      Serial.println(com);
//      Serial1.print("Serial.readString:");
//      Serial1.println(com);
//      Serial1.println(j - i - 1);
//      Serial.print("Serial.readString:");
//      Serial.println(com);
//      Serial.println(j - i - 1);
      String str = "09";
      n = com[0] - str[0];
      int k = 0;
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
          c[k].sita = s;
          while (1)
          {
            if (com[m] == 'a' || com[m] == 'b')
            {
              c[k].kind = com[m];
              break;
            }
            m++;
          }
          k++;
        }
        m++;
      }
      for (int i = 0; i < n; i++)
      {
        Serial.print(c[i].sita);
        Serial.print(c[i].kind);
        Serial.print("   ");
      }
      Serial.println("");
      break;
    }
    while(Serial1.read()>= 0){} //clear serialbuffer
  }
}

void sort()
{
  int temp = 0;
  char ts;
  for (int i = 0; i < n; i++)
  {
    for (int j = i + 1; j < n; j++)
    {
      if (c[j].sita < c[i].sita)
      {
        temp = c[j].sita;
        ts = c[j].kind;
        c[j].sita = c[i].sita;
        c[j].kind = c[i].kind;
        c[i].sita = temp;
        c[i].kind = ts;
      }
    }
  }
}

void Acture()
{
  int flag = 0; //first
  for (int i = 0; i < n; i++)
  {
    if (flag == 0)
    {
      flag = 1;
      swirl(int(c[i].sita * 8.889));
      if (c[i].kind == 'a') PointLeaf();
      else if (c[i].kind == 'b') PointFlower();
    }
    else
    {
      swirl(int((c[i].sita - c[i - 1].sita) * 8.889));
      if (c[i].kind == 'a') PointLeaf();
      else if (c[i].kind == 'b') PointFlower();
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
  while(1){}
  push.attach(PUSH);
  push.write(stretchin);
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
        GoAhead(150);
        delay(800);
        Serial1.println("1");
        delay(500);
        PointPose();
        Rec();
        sort();
        Acture();
        setback();
        WatchPose();
        
        count++;
        GoAhead(2000);
      }
    }
  }
}
