; Auto-generated. Do not edit!


(cl:in-package lslidar_x10_msgs-msg)


;//! \htmlinclude LslidarX10Difop.msg.html

(cl:defclass <LslidarX10Difop> (roslisp-msg-protocol:ros-message)
  ((rpm
    :reader rpm
    :initarg :rpm
    :type cl:integer
    :initform 0))
)

(cl:defclass LslidarX10Difop (<LslidarX10Difop>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <LslidarX10Difop>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'LslidarX10Difop)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lslidar_x10_msgs-msg:<LslidarX10Difop> is deprecated: use lslidar_x10_msgs-msg:LslidarX10Difop instead.")))

(cl:ensure-generic-function 'rpm-val :lambda-list '(m))
(cl:defmethod rpm-val ((m <LslidarX10Difop>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lslidar_x10_msgs-msg:rpm-val is deprecated.  Use lslidar_x10_msgs-msg:rpm instead.")
  (rpm m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <LslidarX10Difop>) ostream)
  "Serializes a message object of type '<LslidarX10Difop>"
  (cl:let* ((signed (cl:slot-value msg 'rpm)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 18446744073709551616) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <LslidarX10Difop>) istream)
  "Deserializes a message object of type '<LslidarX10Difop>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'rpm) (cl:if (cl:< unsigned 9223372036854775808) unsigned (cl:- unsigned 18446744073709551616))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<LslidarX10Difop>)))
  "Returns string type for a message object of type '<LslidarX10Difop>"
  "lslidar_x10_msgs/LslidarX10Difop")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'LslidarX10Difop)))
  "Returns string type for a message object of type 'LslidarX10Difop"
  "lslidar_x10_msgs/LslidarX10Difop")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<LslidarX10Difop>)))
  "Returns md5sum for a message object of type '<LslidarX10Difop>"
  "50442aa210dd5f42de9c4e1b86df3045")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'LslidarX10Difop)))
  "Returns md5sum for a message object of type 'LslidarX10Difop"
  "50442aa210dd5f42de9c4e1b86df3045")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<LslidarX10Difop>)))
  "Returns full string definition for message of type '<LslidarX10Difop>"
  (cl:format cl:nil "int64 rpm~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'LslidarX10Difop)))
  "Returns full string definition for message of type 'LslidarX10Difop"
  (cl:format cl:nil "int64 rpm~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <LslidarX10Difop>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <LslidarX10Difop>))
  "Converts a ROS message object to a list"
  (cl:list 'LslidarX10Difop
    (cl:cons ':rpm (rpm msg))
))
