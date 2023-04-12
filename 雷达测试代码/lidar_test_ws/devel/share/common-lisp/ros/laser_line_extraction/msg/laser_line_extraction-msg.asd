
(cl:in-package :asdf)

(defsystem "laser_line_extraction-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "LineSegment" :depends-on ("_package_LineSegment"))
    (:file "_package_LineSegment" :depends-on ("_package"))
    (:file "LineSegmentList" :depends-on ("_package_LineSegmentList"))
    (:file "_package_LineSegmentList" :depends-on ("_package"))
  ))