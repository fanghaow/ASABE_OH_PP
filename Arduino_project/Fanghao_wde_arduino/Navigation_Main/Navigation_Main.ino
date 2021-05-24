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

//#define SPD 100
#define SWR 300

Servo arm1;
Servo arm2;
Servo push;

#define armoneup 89 //watchpos
#define armonepos 79
#define armonedown 156
#define armtwoup 118 //watchpos
#define armtwopos 122
#define armtwodown 80
#define stretchleaf 130
#define stretchflower 80
#define stretchin 0

//
# define dist A1
# define dist_b A0
float dis;
float dis_b;
//

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

void GoAhead(int Step, int SPD=50)//向前
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

void GoBack(int Step, int SPD=50)//向后
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

void Turn(int Dir=-1, int SPD=100, int Ratio=1)
{
  int Step = 1; 
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);
  if(Dir == 1) // Turn Right Circle!!!
  {
    digitalWrite(DIR1, HIGH);
    digitalWrite(DIR2, HIGH);
  }
  else if(Dir == -1) // Turn Left Circle!!!
  {
    digitalWrite(DIR1, LOW);
    digitalWrite(DIR2, LOW);
  }
  else if(Dir == 0) // GoAhead
  {  
    digitalWrite(DIR1, HIGH);
    digitalWrite(DIR2, LOW);
  }
  else if(Dir == -2) // GoBackward
  {  
    digitalWrite(DIR1, LOW);
    digitalWrite(DIR2, HIGH);
  }
  if(Ratio > 0) // Trun Left
  {
    for (int i = 0; i < Step; i++) {
      for(int j = 0; j < Ratio; j++)
      {
        digitalWrite(STP2, HIGH); // 2号轮是右轮
        digitalWrite(STP2, LOW);
        delayMicroseconds(SPD);
      }
      digitalWrite(STP1, HIGH);
      digitalWrite(STP1, LOW);
      delayMicroseconds(SPD);
    }
  }
  else
  {
    Ratio = -Ratio;
    for (int i = 0; i < Step; i++) {
      for(int j = 0; j < Ratio; j++)
      {
        digitalWrite(STP1, HIGH); // 2号轮是右轮
        digitalWrite(STP1, LOW);
        delayMicroseconds(SPD);
      }
      digitalWrite(STP2, HIGH);
      digitalWrite(STP2, LOW);
      delayMicroseconds(SPD);
    }
  }
}

void SpeedUp(int SPD){ // Back
  int Step = 1;
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);
  digitalWrite(DIR1, LOW);
  digitalWrite(DIR2, HIGH);
  for(int i=0; i<Step; i++)
  {
    digitalWrite(STP1, HIGH);
    digitalWrite(STP2, HIGH);
    delayMicroseconds(SPD);
    digitalWrite(STP1, LOW);
    digitalWrite(STP2, LOW);
    delayMicroseconds(SPD);
  }
}

void Measure_Dis()
{
  float distance;
  float dis_mean;
  float dis_sum=0;
  int read_time = 3;
  for(int i=0; i<read_time; i++)
  {
    distance = analogRead(dist);
    dis_sum += distance;
    Serial.print("Distance : ");
    Serial.println(distance);
    delay(1);
  }
  dis_mean = dis_sum / read_time;
  Serial.print("Mean Forward Distance is : ");
  Serial.println(dis_mean);
  dis = dis_mean;
}

void Measure_Dis_b()
{
  float distance;
  float dis_mean;
  float dis_sum=0;
  int read_time = 3;
  for(int i=0; i<read_time; i++)
  {
    distance = analogRead(dist_b);
    dis_sum += distance;
    Serial.print("Distance : ");
    Serial.println(distance);
    delay(1);
  }
  dis_mean = dis_sum / read_time;
  Serial.print("Mean Backward Distance is : ");
  Serial.println(dis_mean);
  dis_b = dis_mean;
}

int rounding(float value)
{
  float small = value - int(value);
  if(small < 0.5)
  {
    return int(value);
  }
  else
  {
    return (int(value) + 1);
  }
}
//-----------------------------------------------------------------------

void loop() {
// 开环换垄
  int Step = 4000;
  int Ratio = 3;
  int Dly = 1500;
  for(int i=0; i<Step; i++){
    Turn(0, 100, Ratio);
  }
//  delay(Dly);
  for(int i=0; i<Step; i++){
    Turn(0, 100, -Ratio);
  }
//  delay(Dly);
  //
  for(int i=0; i<Step-500; i++){
    Turn(-2, 100, Ratio+1);
  }
//  delay(Dly);
  for(int i=0; i<Step-500; i++){
    Turn(-2, 100, -(Ratio+1));
  }
//  delay(Dly);
  for(int i=0; i<100000; i++){
    GoBack(1);
  }

// 匀加速后退
//  for(int i=0; i<10000; i++)
//  { 
//    int SPD = 100 - int(i/200);
//    SpeedUp(SPD);
//  }
//  for(int i=0; i<100000; i++){
//    GoBack(1, 50);
//  }
//  delay(2000);

//// 测距寻迹
//
//    Measure_Dis();
//    dis = rounding(dis);
//    Serial.print("Global forward distance is ");
//    Serial.println(dis);
//    Measure_Dis_b();
//    dis_b = rounding(dis_b);
//    Serial.print("Global back distance is ");
//    Serial.println(dis_b);
//
////    dis = 72;
//  int dis_th = 69;
//  for(int i=0; i<2000; i++)
//  {
//    if(dis_b==dis_th)
//    {
//      GoBack(1);
//    }
//    else if(dis_b<dis_th)
//    {
//      Turn(-2, 100, -2);
//    }
//    else if(dis_b>dis_th)
//    {
//      Turn(-2, 100, 2);
//    }
//  }
}
