;; Auto-generated. Do not edit!


(when (boundp 'laser_line_extraction::LineSegment)
  (if (not (find-package "LASER_LINE_EXTRACTION"))
    (make-package "LASER_LINE_EXTRACTION"))
  (shadow 'LineSegment (find-package "LASER_LINE_EXTRACTION")))
(unless (find-package "LASER_LINE_EXTRACTION::LINESEGMENT")
  (make-package "LASER_LINE_EXTRACTION::LINESEGMENT"))

(in-package "ROS")
;;//! \htmlinclude LineSegment.msg.html


(defclass laser_line_extraction::LineSegment
  :super ros::object
  :slots (_radius _angle _covariance _start _end ))

(defmethod laser_line_extraction::LineSegment
  (:init
   (&key
    ((:radius __radius) 0.0)
    ((:angle __angle) 0.0)
    ((:covariance __covariance) (make-array 4 :initial-element 0.0 :element-type :float))
    ((:start __start) (make-array 2 :initial-element 0.0 :element-type :float))
    ((:end __end) (make-array 2 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _radius (float __radius))
   (setq _angle (float __angle))
   (setq _covariance __covariance)
   (setq _start __start)
   (setq _end __end)
   self)
  (:radius
   (&optional __radius)
   (if __radius (setq _radius __radius)) _radius)
  (:angle
   (&optional __angle)
   (if __angle (setq _angle __angle)) _angle)
  (:covariance
   (&optional __covariance)
   (if __covariance (setq _covariance __covariance)) _covariance)
  (:start
   (&optional __start)
   (if __start (setq _start __start)) _start)
  (:end
   (&optional __end)
   (if __end (setq _end __end)) _end)
  (:serialization-length
   ()
   (+
    ;; float32 _radius
    4
    ;; float32 _angle
    4
    ;; float32[4] _covariance
    (* 4    4)
    ;; float32[2] _start
    (* 4    2)
    ;; float32[2] _end
    (* 4    2)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _radius
       (sys::poke _radius (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _angle
       (sys::poke _angle (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32[4] _covariance
     (dotimes (i 4)
       (sys::poke (elt _covariance i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32[2] _start
     (dotimes (i 2)
       (sys::poke (elt _start i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32[2] _end
     (dotimes (i 2)
       (sys::poke (elt _end i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _radius
     (setq _radius (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _angle
     (setq _angle (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32[4] _covariance
   (dotimes (i (length _covariance))
     (setf (elt _covariance i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     )
   ;; float32[2] _start
   (dotimes (i (length _start))
     (setf (elt _start i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     )
   ;; float32[2] _end
   (dotimes (i (length _end))
     (setf (elt _end i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     )
   ;;
   self)
  )

(setf (get laser_line_extraction::LineSegment :md5sum-) "0b798f1cd276e61d7015b3e32ccd5c78")
(setf (get laser_line_extraction::LineSegment :datatype-) "laser_line_extraction/LineSegment")
(setf (get laser_line_extraction::LineSegment :definition-)
      "float32 radius
float32 angle
float32[4] covariance
float32[2] start
float32[2] end

")



(provide :laser_line_extraction/LineSegment "0b798f1cd276e61d7015b3e32ccd5c78")


