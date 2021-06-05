//#define DC_Motor_Vcc 10;
#define DC_Motor_CTL A6

void setup() {
  // put your setup code here, to run once:
  pinMode(DC_Motor_CTL, OUTPUT);
}

void turning(int step)
{
  for(int i=0; i<step; i++)
  {
    analogWrite(DC_Motor_CTL, 150);
    delay(10);
    analogWrite(DC_Motor_CTL, 0);
    delay(10);
  }
}
void loop() {
  // put your main code here, to run repeatedly:

  turning(10000);
  delay(1500);
}
