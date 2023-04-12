;; Auto-generated. Do not edit!


(when (boundp 'laser_line_extraction::LineSegmentList)
  (if (not (find-package "LASER_LINE_EXTRACTION"))
    (make-package "LASER_LINE_EXTRACTION"))
  (shadow 'LineSegmentList (find-package "LASER_LINE_EXTRACTION")))
(unless (find-package "LASER_LINE_EXTRACTION::LINESEGMENTLIST")
  (make-package "LASER_LINE_EXTRACTION::LINESEGMENTLIST"))

(in-package "ROS")
;;//! \htmlinclude LineSegmentList.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass laser_line_extraction::LineSegmentList
  :super ros::object
  :slots (_header _line_segments ))

(defmethod laser_line_extraction::LineSegmentList
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:line_segments __line_segments) (let (r) (dotimes (i 0) (push (instance laser_line_extraction::LineSegment :init) r)) r))
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
    ;; laser_line_extraction/LineSegment[] _line_segments
    (apply #'+ (send-all _line_segments :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; laser_line_extraction/LineSegment[] _line_segments
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
   ;; laser_line_extraction/LineSegment[] _line_segments
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _line_segments (let (r) (dotimes (i n) (push (instance laser_line_extraction::LineSegment :init) r)) r))
     (dolist (elem- _line_segments)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get laser_line_extraction::LineSegmentList :md5sum-) "15c60e2ccf21433a5067160ec144f8c3")
(setf (get laser_line_extraction::LineSegmentList :datatype-) "laser_line_extraction/LineSegmentList")
(setf (get laser_line_extraction::LineSegmentList :definition-)
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
MSG: laser_line_extraction/LineSegment
float32 radius
float32 angle
float32[4] covariance
float32[2] start
float32[2] end

")



(provide :laser_line_extraction/LineSegmentList "15c60e2ccf21433a5067160ec144f8c3")


