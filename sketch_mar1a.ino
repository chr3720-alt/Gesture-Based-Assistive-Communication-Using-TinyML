#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin(21,22);   // SDA=21, SCL=22

  mpu.initialize();

  if (mpu.testConnection())
    Serial.println("MPU6050 Connected");
  else
    Serial.println("MPU6050 Connection Failed");

  Serial.println("data,ax,ay,az,gx,gy,gz");
}

void loop() {
  int16_t ax, ay, az, gx, gy, gz;

  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  Serial.print("data,");
  Serial.print(ax / 16384.0); Serial.print(",");
  Serial.print(ay / 16384.0); Serial.print(",");
  Serial.print(az / 16384.0); Serial.print(",");
  Serial.print(gx / 131.0); Serial.print(",");
  Serial.print(gy / 131.0); Serial.print(",");
  Serial.println(gz / 131.0);

  delay(20);  // 50Hz sampling
}