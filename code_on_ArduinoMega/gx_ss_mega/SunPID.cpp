#include "SunPID.h"
PID::PID(double min_val, double max_val, double kp, double ki, double kd)
    : min_val_(min_val), max_val_(max_val), kp_(kp), ki_(ki), kd_(kd) {}

double PID::Compute(double setpoint, double measured_value) {
  double error;
  double pid;
  error = setpoint - measured_value;
  integral_ += error;
  //抗积分饱和——限幅方法
  integral_ = constrain(integral_, min_val_, max_val_);
  derivative_ = error - prev_error_;
  if (setpoint == 0 && error == 0) {
    integral_ = 0;
  }

  pid = (kp_ * error) + (ki_ * integral_) + (kd_ * derivative_);
  prev_error_ = error;
  //抗执行器饱和——限幅方法
  return constrain(pid, min_val_, max_val_);
}

void PID::UpdateTunings(double kp, double ki, double kd) {
  kp_ = kp;
  ki_ = ki;
  kd_ = kd;
}

void PID::UpdateParameters() {
  integral_ = 0;
  derivative_ = 0;
  prev_error_ = 0;
}