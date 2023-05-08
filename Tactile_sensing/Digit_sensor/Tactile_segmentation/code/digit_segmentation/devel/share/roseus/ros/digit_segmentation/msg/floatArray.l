;; Auto-generated. Do not edit!


(when (boundp 'digit_segmentation::floatArray)
  (if (not (find-package "DIGIT_SEGMENTATION"))
    (make-package "DIGIT_SEGMENTATION"))
  (shadow 'floatArray (find-package "DIGIT_SEGMENTATION")))
(unless (find-package "DIGIT_SEGMENTATION::FLOATARRAY")
  (make-package "DIGIT_SEGMENTATION::FLOATARRAY"))

(in-package "ROS")
;;//! \htmlinclude floatArray.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass digit_segmentation::floatArray
  :super ros::object
  :slots (_header _type _rotation _translation ))

(defmethod digit_segmentation::floatArray
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:type __type) "")
    ((:rotation __rotation) 0.0)
    ((:translation __translation) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _header __header)
   (setq _type (string __type))
   (setq _rotation (float __rotation))
   (setq _translation __translation)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:type
   (&optional __type)
   (if __type (setq _type __type)) _type)
  (:rotation
   (&optional __rotation)
   (if __rotation (setq _rotation __rotation)) _rotation)
  (:translation
   (&optional __translation)
   (if __translation (setq _translation __translation)) _translation)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; string _type
    4 (length _type)
    ;; float64 _rotation
    8
    ;; float64[] _translation
    (* 8    (length _translation)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; string _type
       (write-long (length _type) s) (princ _type s)
     ;; float64 _rotation
       (sys::poke _rotation (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64[] _translation
     (write-long (length _translation) s)
     (dotimes (i (length _translation))
       (sys::poke (elt _translation i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; string _type
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _type (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float64 _rotation
     (setq _rotation (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64[] _translation
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _translation (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _translation i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get digit_segmentation::floatArray :md5sum-) "5ae8a1a1538beabbdecb82544adb51e8")
(setf (get digit_segmentation::floatArray :datatype-) "digit_segmentation/floatArray")
(setf (get digit_segmentation::floatArray :definition-)
      "Header header
string type
float64 rotation
float64[] translation

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

")



(provide :digit_segmentation/floatArray "5ae8a1a1538beabbdecb82544adb51e8")


