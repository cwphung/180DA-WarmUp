/*
  Arduino LSM6DS3 - Simple Accelerometer

  This example reads the acceleration values from the LSM6DS3
  sensor and continuously prints them to the Serial Monitor
  or Serial Plotter.

  The circuit:
  - Arduino Uno WiFi Rev 2 or Arduino Nano 33 IoT

  created 10 Jul 2019
  by Riccardo Rizzo

  This example code is in the public domain.
*/

#include <Arduino_LSM6DS3.h>

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");

    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");  
  Serial.println();
  Serial.println("Acceleration in g's\tGyroscope in degrees/second\tState" );
  Serial.println("X\tY\tZ\tA\tB\tC");
}

void loop() {
  float Ax, Ay, Az, Gx, Gy, Gz;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(Ax, Ay, Az);

    Serial.print(Ax);
    Serial.print('\t');
    Serial.print(Ay);
    Serial.print('\t');
    Serial.print(Az);
    Serial.print('\t');
  }
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(Gx, Gy, Gz);

    Serial.print(Gx);
    Serial.print('\t');
    Serial.print(Gy);
    Serial.print('\t');
    Serial.print(Gz);
    Serial.print('\t');
  }

  // State classifier
  if (abs(Ax) <= 0.1 && abs(Ay) <= 0.1 && abs(Az) - 1 <= 0.1) {
    Serial.print("Idle");
    Serial.println();
  } else if (Ax <= -0.2 && abs(Az) - 1 <= 0.3) {
    Serial.print("Forward Push");
    Serial.println();
  } else if (Az <= 0.7) {
    Serial.print("Upward Lift");
    Serial.println();
  } else {
    Serial.print("N/A");
    Serial.println();
  }
  delay(100);
}
