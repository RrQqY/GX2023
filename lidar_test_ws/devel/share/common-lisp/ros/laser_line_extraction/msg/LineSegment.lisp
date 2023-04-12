; Auto-generated. Do not edit!


(cl:in-package laser_line_extraction-msg)


;//! \htmlinclude LineSegment.msg.html

(cl:defclass <LineSegment> (roslisp-msg-protocol:ros-message)
  ((radius
    :reader radius
    :initarg :radius
    :type cl:float
    :initform 0.0)
   (angle
    :reader angle
    :initarg :angle
    :type cl:float
    :initform 0.0)
   (covariance
    :reader covariance
    :initarg :covariance
    :type (cl:vector cl:float)
   :initform (cl:make-array 4 :element-type 'cl:float :initial-element 0.0))
   (start
    :reader start
    :initarg :start
    :type (cl:vector cl:float)
   :initform (cl:make-array 2 :element-type 'cl:float :initial-element 0.0))
   (end
    :reader end
    :initarg :end
    :type (cl:vector cl:float)
   :initform (cl:make-array 2 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass LineSegment (<LineSegment>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <LineSegment>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'LineSegment)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name laser_line_extraction-msg:<LineSegment> is deprecated: use laser_line_extraction-msg:LineSegment instead.")))

(cl:ensure-generic-function 'radius-val :lambda-list '(m))
(cl:defmethod radius-val ((m <LineSegment>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader laser_line_extraction-msg:radius-val is deprecated.  Use laser_line_extraction-msg:radius instead.")
  (radius m))

(cl:ensure-generic-function 'angle-val :lambda-list '(m))
(cl:defmethod angle-val ((m <LineSegment>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader laser_line_extraction-msg:angle-val is deprecated.  Use laser_line_extraction-msg:angle instead.")
  (angle m))

(cl:ensure-generic-function 'covariance-val :lambda-list '(m))
(cl:defmethod covariance-val ((m <LineSegment>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader laser_line_extraction-msg:covariance-val is deprecated.  Use laser_line_extraction-msg:covariance instead.")
  (covariance m))

(cl:ensure-generic-function 'start-val :lambda-list '(m))
(cl:defmethod start-val ((m <LineSegment>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader laser_line_extraction-msg:start-val is deprecated.  Use laser_line_extraction-msg:start instead.")
  (start m))

(cl:ensure-generic-function 'end-val :lambda-list '(m))
(cl:defmethod end-val ((m <LineSegment>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader laser_line_extraction-msg:end-val is deprecated.  Use laser_line_extraction-msg:end instead.")
  (end m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <LineSegment>) ostream)
  "Serializes a message object of type '<LineSegment>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'radius))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'covariance))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'start))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'end))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <LineSegment>) istream)
  "Deserializes a message object of type '<LineSegment>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'radius) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle) (roslisp-utils:decode-single-float-bits bits)))
  (cl:setf (cl:slot-value msg 'covariance) (cl:make-array 4))
  (cl:let ((vals (cl:slot-value msg 'covariance)))
    (cl:dotimes (i 4)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits)))))
  (cl:setf (cl:slot-value msg 'start) (cl:make-array 2))
  (cl:let ((vals (cl:slot-value msg 'start)))
    (cl:dotimes (i 2)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits)))))
  (cl:setf (cl:slot-value msg 'end) (cl:make-array 2))
  (cl:let ((vals (cl:slot-value msg 'end)))
    (cl:dotimes (i 2)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<LineSegment>)))
  "Returns string type for a message object of type '<LineSegment>"
  "laser_line_extraction/LineSegment")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'LineSegment)))
  "Returns string type for a message object of type 'LineSegment"
  "laser_line_extraction/LineSegment")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<LineSegment>)))
  "Returns md5sum for a message object of type '<LineSegment>"
  "0b798f1cd276e61d7015b3e32ccd5c78")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'LineSegment)))
  "Returns md5sum for a message object of type 'LineSegment"
  "0b798f1cd276e61d7015b3e32ccd5c78")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<LineSegment>)))
  "Returns full string definition for message of type '<LineSegment>"
  (cl:format cl:nil "float32 radius~%float32 angle~%float32[4] covariance~%float32[2] start~%float32[2] end~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'LineSegment)))
  "Returns full string definition for message of type 'LineSegment"
  (cl:format cl:nil "float32 radius~%float32 angle~%float32[4] covariance~%float32[2] start~%float32[2] end~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <LineSegment>))
  (cl:+ 0
     4
     4
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'covariance) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'start) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'end) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <LineSegment>))
  "Converts a ROS message object to a list"
  (cl:list 'LineSegment
    (cl:cons ':radius (radius msg))
    (cl:cons ':angle (angle msg))
    (cl:cons ':covariance (covariance msg))
    (cl:cons ':start (start msg))
    (cl:cons ':end (end msg))
))
