#include <Arduino_LSM6DS3.h>
#include "Statistic.h"
#include "model.h"

const uint16_t window_size = 150;

statistic::Statistic<float, int16_t, true> xs;
statistic::Statistic<float, int16_t, true> ys;
statistic::Statistic<float, int16_t, true> zs;

int16_t features[12];


void setup() {
  // set up serial
  Serial.begin(115200);
  while(!Serial);
  delay(1000);
  Serial.println("Serial is ready");

  // set up IMU
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");

    while (1);
  }

  xs.clear();
  ys.clear();
  zs.clear();

  Serial.println("Go!");
}

void loop() {
  float x, y, z;

  if (IMU.accelerationAvailable()) {
    // read IMU
    IMU.readAcceleration(x, y, z);

    // accumulate IMU in sliding window
    xs.add(x);
    ys.add(y);
    zs.add(z);

    // if sliding window is full...
    if (xs.count() >= window_size) {
      // extract statistical features
      features[0] = xs.minimum();
      features[1] = xs.maximum();
      features[2] = xs.average();
      features[3] = xs.pop_stdev();
      features[4] = ys.minimum();
      features[5] = ys.maximum();
      features[6] = ys.average();
      features[7] = ys.pop_stdev();
      features[8] = zs.minimum();
      features[9] = zs.maximum();
      features[10] = zs.average();
      features[11] = zs.pop_stdev();

      // run model inference
      const int32_t prediction = model_predict(features, 12);
      Serial.println(prediction);

      // slide the window
      xs.clear();
      ys.clear();
      zs.clear();
    }
  }
}
