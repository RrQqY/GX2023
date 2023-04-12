#ifndef SUN_PID_H
#define SUN_PID_H

#include "Arduino.h"

class PID {
 public:
  //构造函数
  PID(double min_val, double max_val, double kp, double ki, double kd);
  //位置式PID,计算输出值
  double Compute(double setpoint, double measured_value);
  void UpdateTunings(double kp, double ki, double kd);
  void UpdateParameters();

 private:
  double min_val_;
  double max_val_;
  double kp_;
  double ki_;
  double kd_;
  double integral_;
  double derivative_;
  double prev_error_;
};

#endif
