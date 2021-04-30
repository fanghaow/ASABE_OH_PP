#include <Servo.h>

#define DIR1 46
#define STP1 44
#define EN1  42
#define DIR2 4
#define STP2 5
#define EN2  7
#define DIR3 49
#define STP3 51
#define EN3  53

#define T1 22
#define T2 47
#define high1 26
#define low1 24
#define high2 50
#define low2 48

#define plantplace 12
#define catpic 13
#define picdeal 15

int t1, t2 = 0; //循迹变量

const int SPD = 55;
const int RET = 50;
//const int UPCAMERA = 83;

int p = 0;
int i = 0;

void setup()  
{
  pinMode(DIR1, OUTPUT); //步进电机
  pinMode(STP1, OUTPUT);
  pinMode(EN1, OUTPUT);
  pinMode(DIR2, OUTPUT); //步进电机
  pinMode(STP2, OUTPUT);
  pinMode(EN2, OUTPUT);
  pinMode(DIR3, OUTPUT); //步进电机
  pinMode(STP3, OUTPUT);
  pinMode(EN3, OUTPUT);
  
  pinMode(high1, OUTPUT);//接触开关
  digitalWrite(high1, HIGH);
  pinMode(high2, OUTPUT);
  digitalWrite(high2, HIGH);
  pinMode(low1, OUTPUT);
  digitalWrite(low1, LOW);
  pinMode(low2, OUTPUT);
  digitalWrite(low2, LOW);
  
  pinMode(plantplace, INPUT);
  pinMode(catpic, OUTPUT);
  digitalWrite(catpic, LOW);
  pinMode(picdeal, INPUT);
  
  Serial.begin(9600);
  Serial1.begin(9600);
}

void GoAhead(int Step)//向前
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

void TrackLeft(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);
  
  digitalWrite(DIR1, LOW);
  digitalWrite(DIR2, HIGH);
  for (int x = 0; x < Step; x++)
  {
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, HIGH);
    delayMicroseconds(SPD);
    digitalWrite(STP1, LOW);
    delayMicroseconds(SPD);
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD);
    digitalWrite(STP1, LOW);
    delayMicroseconds(SPD);
  }
}

void TrackRight(int Step)
{
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);
  
  digitalWrite(DIR1, LOW);
  digitalWrite(DIR2, HIGH);
  for (int x = 0; x < Step; x++)
  {
    digitalWrite(STP2, HIGH);
    digitalWrite(STP1, HIGH);
    delayMicroseconds(SPD);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD);
    digitalWrite(STP2, HIGH);
    digitalWrite(STP1, LOW);
    delayMicroseconds(SPD);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD);
  }
}
void Left(int Step)
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

void GoBack(int Step)//向后
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

void Trackcheck()
{
  t1 = digitalRead(T1);
  t2 = digitalRead(T2);
}

void Trackgo(int Step)
{
    Trackcheck();
    if (t2 == 0 && t1 == 0) //撞到为0
    {
      GoAhead(1);
    }
    else if (t2 == 0 && t1 == 1)
    {
//      TrackLeft(1);
      GoAhead(1);
    }
    else
    {
//      TrackRight(1);
      GoAhead(1);
    }
}

void cameraup(int Step)//向前
{
  digitalWrite(EN3, HIGH);
  digitalWrite(DIR3, HIGH);
  for (int i = 0; i < Step; i++) {
    digitalWrite(STP3, HIGH);
    delayMicroseconds(100);
    digitalWrite(STP3, LOW);
    delayMicroseconds(100);
  }
}

void Checkplant()
{
  p = digitalRead(plantplace);
}

void loop()  
{
  Serial1.println("1");
  cameraup(3000);
  GoAhead(6000);
  while(i < 12)
  {
    while(Serial1.read()>= 0){} //clear serialbuffer
    Trackgo(1);
    Checkplant();
    if(p == 1)
    {
      Trackgo(10);
      Checkplant();
      if(p == 1)
      {
//        while(1)
//        {
//          if (digitalRead(picdeal) == 1)
//          {
//            break;
//          }
//        }
//        delay(100);
//        for(int k = 0; k < 500; k++)
//        {
//          Serial1.println("1");
////          digitalWrite(catpic, HIGH);
//          delay(1);
//        }
        Trackgo(400);
        delay(300);
        Serial1.println("1234");
//        int ti = 0;
//        while(1)
//        {
//          if (Serial1.read() > 0) break;
//        }
        delay(300);
        GoAhead(5000);
        i++;
        }
    }
  }
  GoAhead(6000);
  
  while(1){}
  
}  
