;; Auto-generated. Do not edit!


(when (boundp 'lslidar_x10_msgs::LslidarX10Packet)
  (if (not (find-package "LSLIDAR_X10_MSGS"))
    (make-package "LSLIDAR_X10_MSGS"))
  (shadow 'LslidarX10Packet (find-package "LSLIDAR_X10_MSGS")))
(unless (find-package "LSLIDAR_X10_MSGS::LSLIDARX10PACKET")
  (make-package "LSLIDAR_X10_MSGS::LSLIDARX10PACKET"))

(in-package "ROS")
;;//! \htmlinclude LslidarX10Packet.msg.html


(defclass lslidar_x10_msgs::LslidarX10Packet
  :super ros::object
  :slots (_stamp _data ))

(defmethod lslidar_x10_msgs::LslidarX10Packet
  (:init
   (&key
    ((:stamp __stamp) (instance ros::time :init))
    ((:data __data) (make-array 2000 :initial-element 0 :element-type :char))
    )
   (send-super :init)
   (setq _stamp __stamp)
   (setq _data __data)
   self)
  (:stamp
   (&optional __stamp)
   (if __stamp (setq _stamp __stamp)) _stamp)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:serialization-length
   ()
   (+
    ;; time _stamp
    8
    ;; uint8[2000] _data
    (* 1    2000)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; time _stamp
       (write-long (send _stamp :sec) s) (write-long (send _stamp :nsec) s)
     ;; uint8[2000] _data
     (princ _data s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; time _stamp
     (send _stamp :sec (sys::peek buf ptr- :integer)) (incf ptr- 4)  (send _stamp :nsec (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; uint8[2000] _data
   (setq _data (make-array 2000 :element-type :char))
   (replace _data buf :start2 ptr-) (incf ptr- 2000)
   ;;
   self)
  )

(setf (get lslidar_x10_msgs::LslidarX10Packet :md5sum-) "8b4a4c3a12627c71d9c1beffa4ce1941")
(setf (get lslidar_x10_msgs::LslidarX10Packet :datatype-) "lslidar_x10_msgs/LslidarX10Packet")
(setf (get lslidar_x10_msgs::LslidarX10Packet :definition-)
      "# Raw Leishen LIDAR packet.

time stamp              # packet timestamp
uint8[2000] data        # packet contents


")



(provide :lslidar_x10_msgs/LslidarX10Packet "8b4a4c3a12627c71d9c1beffa4ce1941")


