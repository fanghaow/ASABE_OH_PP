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

#define T1 22
#define T2 47
#define high1 26
#define low1 24
#define high2 50
#define low2 48

#define ARM1 A2
#define ARM2 2
#define PUSH 3

#define BASE A11
#define RES 34

#define SPD 100
#define SWR 300

Servo arm1;
Servo arm2;
Servo push;

#define armoneup 107 //watchpos
#define armonepos 87
#define armonedown 164
#define armtwoup 97 //watchpos
#define armtwopos 108
#define armtwodown 65

#define stretchbegin 40
#define stretchleaf 145
#define stretchflower 170
#define stretchin 80

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
int t1, t2 = 0; //循迹变量
int indexf = 0;

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
  
  pinMode(high1, OUTPUT);//接触开关
  digitalWrite(high1, HIGH);
  pinMode(high2, OUTPUT);
  digitalWrite(high2, HIGH);
  pinMode(low1, OUTPUT);
  digitalWrite(low1, LOW);
  pinMode(low2, OUTPUT);
  digitalWrite(low2, LOW);
  pinMode(T1, INPUT);
  pinMode(T2, INPUT);
  
  pinMode(ARM1, OUTPUT);
  pinMode(ARM2, OUTPUT);
  pinMode(PUSH, OUTPUT);
  pinMode(BASE, INPUT);
  Serial1.begin(9600);
  Serial.begin(9600);
  while(Serial1.read()>= 0){} //clear serialbuffer
  
}

void GoAhead(int Step)  //向前
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

void SlowAhead(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, LOW);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, HIGH);
    delayMicroseconds(SPD * 2);
    digitalWrite(STP1, LOW);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD * 2);
  }
}

void GoBack(int Step)  //向后
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, LOW);
  digitalWrite(DIR2, HIGH);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, HIGH);
    delayMicroseconds(SPD);
    digitalWrite(STP1, LOW);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD);
  }
}

void SlowBack(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, LOW);
  digitalWrite(DIR2, HIGH);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, HIGH);
    delayMicroseconds(SPD * 2);
    digitalWrite(STP1, LOW);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD * 2);
  }
}

void TrackLeft(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, LOW);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, HIGH);
    delayMicroseconds(SPD / 2);
    digitalWrite(STP1, LOW);
    delayMicroseconds(SPD / 2);
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD / 2);
    digitalWrite(STP1, LOW);
    delayMicroseconds(SPD / 2);
  }
}

void TrackRight(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, LOW);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, HIGH);
    delayMicroseconds(SPD / 2);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD / 2);
    digitalWrite(STP2, HIGH);
    digitalWrite(STP1, LOW);
    delayMicroseconds(SPD / 2);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD / 2);
  }
}

void TrackLeftBack(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, LOW);
  digitalWrite(DIR2, HIGH);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, HIGH);
    delayMicroseconds(int(SPD / 2));
    digitalWrite(STP1, LOW);
    delayMicroseconds(int(SPD / 2));
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, LOW);
    delayMicroseconds(int(SPD / 2));
    digitalWrite(STP1, LOW);
    delayMicroseconds(int(SPD / 2));
  }
}

void TrackRightBack(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, LOW);
  digitalWrite(DIR2, HIGH);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, HIGH);
    delayMicroseconds(int(SPD / 2));
    digitalWrite(STP2, LOW);
    delayMicroseconds(int(SPD / 2));
    digitalWrite(STP2, HIGH);
    digitalWrite(STP1, LOW);
    delayMicroseconds(int(SPD / 2));
    digitalWrite(STP2, LOW);
    delayMicroseconds(int(SPD / 2));
  }
}

void AheadLeft(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, LOW);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP2, HIGH);
    delayMicroseconds(SPD);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD);
  }
}

void AheadRight(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, LOW);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP1, HIGH);
    delayMicroseconds(SPD);
    digitalWrite(STP1, LOW);
    delayMicroseconds(SPD);
  }
}

void QuickLeft(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, LOW);
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

void QuickRight(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, HIGH);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, HIGH);
    delayMicroseconds(SPD);
    digitalWrite(STP1, LOW);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD);
  }
}

void BackLeft(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, LOW);
  digitalWrite(DIR2, HIGH);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP1, HIGH);
    delayMicroseconds(SPD);
    digitalWrite(STP1, LOW);
    delayMicroseconds(SPD);
  }
}

void BackRight(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  digitalWrite(DIR1, LOW);
  digitalWrite(DIR2, HIGH);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP2, HIGH);
    delayMicroseconds(SPD);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD);
  }
}

void Trackcheck()
{
  t1 = digitalRead(T1);
  t2 = digitalRead(T2);
}

void Trackgo(int Step)
{
  for (int i = 0; i < Step; i++){
    Trackcheck();
    if (t1 == 0 && t2 == 0) GoAhead(1);
    else if (t1 == 1 && t2 == 0)
    {
      indexf++;
      if (indexf == 4)
      {
        indexf = 0;
        TrackLeft(1);
      }
      else
      {
        GoAhead(1);
      }
    }
    else TrackRight(1);
  }
}

void TrackgoBack(int Step)
{
  for (int i = 0; i < Step; i++){
    Trackcheck();
    if (t1 == 0 && t2 == 0) GoBack(1);
    else if (t1 == 0 && t2 == 1) TrackLeftBack(1);
    else TrackRightBack(1);
  }
}

void Makeaturn()
{
  TrackRight(2000);
  GoAhead(2000);
  QuickLeft(7000);
  GoBack(3000);
  GoAhead(10500);
  QuickRight(8500);
  GoAhead(2000);
  TrackRightBack(1000);
  GoBack(8000);
//  TrackgoBack(5000);
//  Trackgo(3000);
//  TrackgoBack(8000);
}

void Uphands()
{
  arm1.attach(ARM1);
  arm2.attach(ARM2);
  int i = armonedown;
  int j = armtwodown;
  arm1.write(i);
  arm2.write(j);
  while(i > armonedown - 30)
  {
    i--;
    arm1.write(i);
    delay(20);
  }
  
  while(i > armonepos || j < armtwopos)
  {
    if (i > armonepos)
    {
      i--;
      arm1.write(i);
    }
    if (j < armtwopos)
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
  int i, j = 0;
  for (i = armoneup, j = armtwoup; i < armonedown, j > armtwodown; i++, j--)
  {
    arm1.write(i);
    arm2.write(j);
    delay(20);
  }
  for (i = armoneup - (armtwodown - armtwoup); i < armonedown; i++)
  {
    arm1.write(i);
    delay(20);
  }
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

void swirl1(int Step)
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

void setback1()
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

void swirl2(int Step)
{
  digitalWrite(EN3, HIGH);
  digitalWrite(DIR3, HIGH);
  for (int i = 0; i < Step; i++)
  {
    digitalWrite(STP3, HIGH);
    delayMicroseconds(SWR);
    digitalWrite(STP3, LOW);
    delayMicroseconds(SWR);
    sita--;
  }
}

void setback2()
{
  digitalWrite(EN3, HIGH);
  digitalWrite(DIR3, LOW);
  for (int i = sita; i < 0; i++)
  {
    digitalWrite(STP3, HIGH);
    delayMicroseconds(SWR);
    digitalWrite(STP3, LOW);
    delayMicroseconds(SWR);
    sita++;
  }
}

void Reset()
{
  digitalWrite(EN3, HIGH);
  digitalWrite(DIR3, HIGH);
  while(1)
  {
    if (digitalRead(RES) == 1) break;
    digitalWrite(STP3, HIGH);
    delayMicroseconds(int(SWR));
    digitalWrite(STP3, LOW);
    delayMicroseconds(int(SWR));
  }
  digitalWrite(DIR3, LOW);
  for (int i = 0; i < 24; i++)
  {
    digitalWrite(STP3, HIGH);
    delayMicroseconds(int(SWR));
    digitalWrite(STP3, LOW);
    delayMicroseconds(int(SWR));
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
//      Serial.println(com);
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
//      for (int i = 0; i < n; i++)
//      {
//        Serial.print(c[i].sita);
//        Serial.print(c[i].kind);
//        Serial.print("   ");
//      }
//      Serial.println("");
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
  if(c[0].sita < 360 - c[n - 1].sita)
  {
    for (int i = 0; i < n; i++)
    {
      if (flag == 0)
      {
        flag = 1;
        swirl1(int(c[i].sita * 8.889));
        if (c[i].kind == 'a') PointLeaf();
        else if (c[i].kind == 'b') PointFlower();
      }
      else
      {
        swirl1(int((c[i].sita - c[i - 1].sita) * 8.889));
        if (c[i].kind == 'a') PointLeaf();
        else if (c[i].kind == 'b') PointFlower();
      }
    }
    setback1();
  }
  
  else
  {
    for (int i = n - 1; i >= 0; i--)
    {
      if (flag == 0)
      {
        flag = 1;
        swirl2(int((360 - c[i].sita) * 8.889));
        if (c[i].kind == 'a') PointLeaf();
        else if (c[i].kind == 'b') PointFlower();
      }
      else
      {
        swirl2(int((c[i + 1].sita - c[i].sita) * 8.889));
        if (c[i].kind == 'a') PointLeaf();
        else if (c[i].kind == 'b') PointFlower();
      }
    }
    setback2();
  }
}



//-----------------------------------------------------------------------

void loop() {
  Makeaturn();
  while(1){}
  Serial1.println("1");
  Uphands();
  push.attach(PUSH);
  push.write(stretchbegin);
  Reset();
  push.write(stretchin);
  delay(200);
  int count = 0;
  while(count < 9)
  {
    Trackgo(1);
    CheckBase();
    if (t == 1)
    {
      Trackgo(2);
      CheckBase();
      if (t == 1)
      { 
        SlowAhead(450);
        delay(200);
        Serial1.println("1");
        delay(50);
//        PointPose();
//        push.attach(PUSH);
//        push.write(stretchin);
        Rec();
        sort();
        Acture();
//        push.attach(PUSH);
//        push.write(stretchbegin);
//        WatchPose();
        count++;
        SlowAhead(1000);
        if (count != 9) Trackgo(5000);
      }
    }
  }
  Makeaturn();
  count = 0;
  while (count < 5)
  {
    TrackgoBack(1);
    CheckBase();
    if (t == 1)
    {
      TrackgoBack(2);
      CheckBase();
      if (t == 1)
      { 
        SlowBack(450);
        delay(200);
        Serial1.println("1");
        delay(50);
//        PointPose();
//        push.attach(PUSH);
//        push.write(stretchin);
        Rec();
        sort();
        Acture();
//        push.attach(PUSH);
//        push.write(stretchbegin);
//        WatchPose();
        count++;
        SlowBack(1000);
        TrackgoBack(5000);
      }
    }
  }
  swirl1(1600);
  Downhands();
  while(1){}
}
