;; Auto-generated. Do not edit!


(when (boundp 'test_pkg::LineSegmentList)
  (if (not (find-package "TEST_PKG"))
    (make-package "TEST_PKG"))
  (shadow 'LineSegmentList (find-package "TEST_PKG")))
(unless (find-package "TEST_PKG::LINESEGMENTLIST")
  (make-package "TEST_PKG::LINESEGMENTLIST"))

(in-package "ROS")
;;//! \htmlinclude LineSegmentList.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass test_pkg::LineSegmentList
  :super ros::object
  :slots (_header _line_segments ))

(defmethod test_pkg::LineSegmentList
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:line_segments __line_segments) (let (r) (dotimes (i 0) (push (instance test_pkg::LineSegment :init) r)) r))
    )
   (send-super :init)
   (setq _header __header)
   (setq _line_segments __line_segments)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:line_segments
   (&rest __line_segments)
   (if (keywordp (car __line_segments))
       (send* _line_segments __line_segments)
     (progn
       (if __line_segments (setq _line_segments (car __line_segments)))
       _line_segments)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; test_pkg/LineSegment[] _line_segments
    (apply #'+ (send-all _line_segments :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; test_pkg/LineSegment[] _line_segments
     (write-long (length _line_segments) s)
     (dolist (elem _line_segments)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; test_pkg/LineSegment[] _line_segments
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _line_segments (let (r) (dotimes (i n) (push (instance test_pkg::LineSegment :init) r)) r))
     (dolist (elem- _line_segments)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get test_pkg::LineSegmentList :md5sum-) "15c60e2ccf21433a5067160ec144f8c3")
(setf (get test_pkg::LineSegmentList :datatype-) "test_pkg/LineSegmentList")
(setf (get test_pkg::LineSegmentList :definition-)
      "Header header
LineSegment[] line_segments

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: test_pkg/LineSegment
float32 radius
float32 angle
float32[4] covariance
float32[2] start
float32[2] end

")



(provide :test_pkg/LineSegmentList "15c60e2ccf21433a5067160ec144f8c3")


