
(cl:in-package :asdf)

(defsystem "digit_segmentation-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "floatArray" :depends-on ("_package_floatArray"))
    (:file "_package_floatArray" :depends-on ("_package"))
  ))