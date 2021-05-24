# define dist A12

float distance;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  distance = analogRead(dist);
//  printf('Distance : %f', distance);
  Serial.print("Distance : ");
  Serial.println(distance);
  delay(1500);
}
