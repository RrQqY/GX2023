/* 这里存储一些和IMU有关的函数 */
#include "gx_campus3.h"

// MPU6050 测试例程 请先安装库 https://github.com/jrowberg/i2cdevlib
#include "I2Cdev.h"                          //i2cdevlib/Arduino/I2Cdev/
#include "MPU6050_6Axis_MotionApps612.h"  //i2cdevlib/Arduino/MPU6050/
// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif

MPU6050  mpu;

// MPU control/status vars
bool dmpReady = false;   // set true if DMP init was successful如果dmp设置为真则设置为true
uint8_t mpuIntStatus;    // holds actual interrupt status byte from MPU
uint8_t devStatus;       // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;     // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;      // count of all bytes currently in FIFO
uint8_t fifoBuffer[64];  // FIFO storage buffer FIFO存储缓存区

// orientation/motion vars
Quaternion q;            // [w, x, y, z]    quaternion container
VectorInt16 aa;          // [x, y, z]       accel sensor measurements
VectorInt16 gy;          // [x, y, z]       gyro sensor measurements
VectorInt16 aaReal;      // [x, y, z]       gravity-free accel sensor measurements
VectorInt16 aaWorld;     // [x, y, z]       world-frame accel sensor measurements
VectorFloat gravity;     // [x, y, z]       gravity vector
float       ypr[3];      // [yaw, pitch, roll]    yaw/pitch/roll container and gravity vector


// IMU初始化
void imu_setup() {
  // join I2C bus (I2Cdev library doesn't do this automatically)
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    Wire.begin();
    Wire.setClock(400000);  // 400kHz I2C clock. Comment this line if having
                            // compilation difficulties
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
    Fastwire::setup(400, true);
  #endif

  // NOTE: 8MHz or slower host processors, like the Teensy @ 3.3V or Arduino
  // Pro Mini running at 3.3V, cannot handle this baud rate reliably due to
  // the baud timing being too misaligned with processor ticks. You must use
  // 38400 or slower in these cases, or use some kind of external separate
  // crystal solution for the UART timer.

  // initialize device
  Serial.println(F("Initializing I2C devices..."));
  mpu.initialize();

  // verify connection
  Serial.println(F("Testing device connections..."));
  Serial.println(mpu.testConnection() ? F("MPU6050 connection successful")
                                      : F("MPU6050 connection failed"));

  // load and configure the DMP
  Serial.println(F("Initializing DMP..."));
  devStatus = mpu.dmpInitialize();

  //提供陀螺仪的偏移量，运行IMU_Zero获得,按最小灵敏度进行缩放
  mpu.setXAccelOffset(-1664);
  mpu.setYAccelOffset(-5078);
  mpu.setZAccelOffset(831);
  mpu.setXGyroOffset(-37);
  mpu.setYGyroOffset(15);
  mpu.setZGyroOffset(2);        // yaw角的零偏，调这个
  
  // make sure it worked (returns 0 if so)
  if (devStatus == 0) {
    // Calibration Time: generate offsets and calibrate our MPU6050
    mpu.CalibrateAccel(6);
    mpu.CalibrateGyro(6);
    Serial.println();
    mpu.PrintActiveOffsets();
    // turn on the DMP, now that it's ready
    Serial.println(F("Enabling DMP..."));
    mpu.setDMPEnabled(true);

    dmpReady = true;

    // get expected DMP packet size for later comparison
    packetSize = mpu.dmpGetFIFOPacketSize();
  } else {
    // ERROR!
    // 1 = initial memory load failed
    // 2 = DMP configuration updates failed
    // (if it's going to break, usually the code will be 1)
    Serial.print(F("DMP Initialization failed (code "));
    Serial.print(devStatus);
    Serial.println(F(")"));
  }
}

// IMU获取yaw角数据
float get_yaw0(){
    // read a packet from FIFO
    if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) {
      mpu.dmpGetQuaternion(&q, fifoBuffer);
      mpu.dmpGetGravity(&gravity, &q);
      mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
      
      return (ypr[0] * 180 * turn_angle_comp / M_PI);
    }
}

// IMU获取yaw角数据（用HWT101）
float get_yaw(){
  while(Serial3.available()){
    JY901.CopeSerialData(Serial3.read()); //Call JY901 data cope function
  }

  return -(float)JY901.stcAngle.Angle[2]/32768*180;
}

// IMU yaw角数据处理
// 由于IMU返回值为(-180~180)，而targetYaw为累计值可能超过180，需要对IMU返回数据进行处理
float get_yaw_pro_left(float yaw){
  float yaw_pro = 0.0;

  // 当出发第一周时（转第2、3、4、5个左转）
  if((left_turn_num > 1) && (left_turn_num <= 5)){
    if(left_turn_num == 2){    // 第2个左转，此时目标为-180度，会出现-180和180的跳变，额外判断
      if(yaw < 0){
        return yaw;
      }
      else if(yaw > 0){
        yaw_pro = yaw - 360;
        return yaw_pro;
      }
    }
    else{
      yaw_pro = yaw - 360;
      return yaw_pro;
    }
  } 
  // 当出发第二周时（转第6、7、8个左转）
  else if((left_turn_num > 5) && (left_turn_num <= 9)){
    if(left_turn_num == 6){    // 第6个左转，此时目标为-180度，会出现-180和180的跳变，额外判断
      if(yaw < 0){
        yaw_pro = yaw - 360;
        return yaw_pro;
      }
      else if(yaw > 0){
        yaw_pro = yaw - 360*2;
        return yaw_pro;
      }
    }
    else{
      yaw_pro = yaw - 360*2;
      return yaw_pro;
    }
  }
  else{
    return yaw;
  }
}
