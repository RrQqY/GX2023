
(cl:in-package :asdf)

(defsystem "lslidar_x10_msgs-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "LslidarX10Difop" :depends-on ("_package_LslidarX10Difop"))
    (:file "_package_LslidarX10Difop" :depends-on ("_package"))
    (:file "LslidarX10Packet" :depends-on ("_package_LslidarX10Packet"))
    (:file "_package_LslidarX10Packet" :depends-on ("_package"))
    (:file "LslidarX10Point" :depends-on ("_package_LslidarX10Point"))
    (:file "_package_LslidarX10Point" :depends-on ("_package"))
    (:file "LslidarX10Scan" :depends-on ("_package_LslidarX10Scan"))
    (:file "_package_LslidarX10Scan" :depends-on ("_package"))
    (:file "LslidarX10Sweep" :depends-on ("_package_LslidarX10Sweep"))
    (:file "_package_LslidarX10Sweep" :depends-on ("_package"))
  ))