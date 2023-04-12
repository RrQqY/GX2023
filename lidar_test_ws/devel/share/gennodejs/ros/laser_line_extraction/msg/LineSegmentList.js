// Auto-generated. Do not edit!

// (in-package laser_line_extraction.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let LineSegment = require('./LineSegment.js');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class LineSegmentList {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.line_segments = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('line_segments')) {
        this.line_segments = initObj.line_segments
      }
      else {
        this.line_segments = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type LineSegmentList
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [line_segments]
    // Serialize the length for message field [line_segments]
    bufferOffset = _serializer.uint32(obj.line_segments.length, buffer, bufferOffset);
    obj.line_segments.forEach((val) => {
      bufferOffset = LineSegment.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type LineSegmentList
    let len;
    let data = new LineSegmentList(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [line_segments]
    // Deserialize array length for message field [line_segments]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.line_segments = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.line_segments[i] = LineSegment.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += 40 * object.line_segments.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'laser_line_extraction/LineSegmentList';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '15c60e2ccf21433a5067160ec144f8c3';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new LineSegmentList(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.line_segments !== undefined) {
      resolved.line_segments = new Array(msg.line_segments.length);
      for (let i = 0; i < resolved.line_segments.length; ++i) {
        resolved.line_segments[i] = LineSegment.Resolve(msg.line_segments[i]);
      }
    }
    else {
      resolved.line_segments = []
    }

    return resolved;
    }
};

module.exports = LineSegmentList;
