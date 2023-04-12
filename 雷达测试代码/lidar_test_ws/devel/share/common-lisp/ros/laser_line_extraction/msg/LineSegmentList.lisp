; Auto-generated. Do not edit!


(cl:in-package laser_line_extraction-msg)


;//! \htmlinclude LineSegmentList.msg.html

(cl:defclass <LineSegmentList> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (line_segments
    :reader line_segments
    :initarg :line_segments
    :type (cl:vector laser_line_extraction-msg:LineSegment)
   :initform (cl:make-array 0 :element-type 'laser_line_extraction-msg:LineSegment :initial-element (cl:make-instance 'laser_line_extraction-msg:LineSegment))))
)

(cl:defclass LineSegmentList (<LineSegmentList>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <LineSegmentList>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'LineSegmentList)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name laser_line_extraction-msg:<LineSegmentList> is deprecated: use laser_line_extraction-msg:LineSegmentList instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <LineSegmentList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader laser_line_extraction-msg:header-val is deprecated.  Use laser_line_extraction-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'line_segments-val :lambda-list '(m))
(cl:defmethod line_segments-val ((m <LineSegmentList>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader laser_line_extraction-msg:line_segments-val is deprecated.  Use laser_line_extraction-msg:line_segments instead.")
  (line_segments m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <LineSegmentList>) ostream)
  "Serializes a message object of type '<LineSegmentList>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'line_segments))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'line_segments))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <LineSegmentList>) istream)
  "Deserializes a message object of type '<LineSegmentList>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'line_segments) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'line_segments)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'laser_line_extraction-msg:LineSegment))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<LineSegmentList>)))
  "Returns string type for a message object of type '<LineSegmentList>"
  "laser_line_extraction/LineSegmentList")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'LineSegmentList)))
  "Returns string type for a message object of type 'LineSegmentList"
  "laser_line_extraction/LineSegmentList")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<LineSegmentList>)))
  "Returns md5sum for a message object of type '<LineSegmentList>"
  "15c60e2ccf21433a5067160ec144f8c3")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'LineSegmentList)))
  "Returns md5sum for a message object of type 'LineSegmentList"
  "15c60e2ccf21433a5067160ec144f8c3")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<LineSegmentList>)))
  "Returns full string definition for message of type '<LineSegmentList>"
  (cl:format cl:nil "Header header~%LineSegment[] line_segments~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: laser_line_extraction/LineSegment~%float32 radius~%float32 angle~%float32[4] covariance~%float32[2] start~%float32[2] end~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'LineSegmentList)))
  "Returns full string definition for message of type 'LineSegmentList"
  (cl:format cl:nil "Header header~%LineSegment[] line_segments~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: laser_line_extraction/LineSegment~%float32 radius~%float32 angle~%float32[4] covariance~%float32[2] start~%float32[2] end~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <LineSegmentList>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'line_segments) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <LineSegmentList>))
  "Converts a ROS message object to a list"
  (cl:list 'LineSegmentList
    (cl:cons ':header (header msg))
    (cl:cons ':line_segments (line_segments msg))
))
