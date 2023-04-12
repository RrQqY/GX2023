// Auto-generated. Do not edit!

// (in-package laser_line_extraction.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class LineSegment {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.radius = null;
      this.angle = null;
      this.covariance = null;
      this.start = null;
      this.end = null;
    }
    else {
      if (initObj.hasOwnProperty('radius')) {
        this.radius = initObj.radius
      }
      else {
        this.radius = 0.0;
      }
      if (initObj.hasOwnProperty('angle')) {
        this.angle = initObj.angle
      }
      else {
        this.angle = 0.0;
      }
      if (initObj.hasOwnProperty('covariance')) {
        this.covariance = initObj.covariance
      }
      else {
        this.covariance = new Array(4).fill(0);
      }
      if (initObj.hasOwnProperty('start')) {
        this.start = initObj.start
      }
      else {
        this.start = new Array(2).fill(0);
      }
      if (initObj.hasOwnProperty('end')) {
        this.end = initObj.end
      }
      else {
        this.end = new Array(2).fill(0);
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type LineSegment
    // Serialize message field [radius]
    bufferOffset = _serializer.float32(obj.radius, buffer, bufferOffset);
    // Serialize message field [angle]
    bufferOffset = _serializer.float32(obj.angle, buffer, bufferOffset);
    // Check that the constant length array field [covariance] has the right length
    if (obj.covariance.length !== 4) {
      throw new Error('Unable to serialize array field covariance - length must be 4')
    }
    // Serialize message field [covariance]
    bufferOffset = _arraySerializer.float32(obj.covariance, buffer, bufferOffset, 4);
    // Check that the constant length array field [start] has the right length
    if (obj.start.length !== 2) {
      throw new Error('Unable to serialize array field start - length must be 2')
    }
    // Serialize message field [start]
    bufferOffset = _arraySerializer.float32(obj.start, buffer, bufferOffset, 2);
    // Check that the constant length array field [end] has the right length
    if (obj.end.length !== 2) {
      throw new Error('Unable to serialize array field end - length must be 2')
    }
    // Serialize message field [end]
    bufferOffset = _arraySerializer.float32(obj.end, buffer, bufferOffset, 2);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type LineSegment
    let len;
    let data = new LineSegment(null);
    // Deserialize message field [radius]
    data.radius = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [angle]
    data.angle = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [covariance]
    data.covariance = _arrayDeserializer.float32(buffer, bufferOffset, 4)
    // Deserialize message field [start]
    data.start = _arrayDeserializer.float32(buffer, bufferOffset, 2)
    // Deserialize message field [end]
    data.end = _arrayDeserializer.float32(buffer, bufferOffset, 2)
    return data;
  }

  static getMessageSize(object) {
    return 40;
  }

  static datatype() {
    // Returns string type for a message object
    return 'laser_line_extraction/LineSegment';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0b798f1cd276e61d7015b3e32ccd5c78';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
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
    const resolved = new LineSegment(null);
    if (msg.radius !== undefined) {
      resolved.radius = msg.radius;
    }
    else {
      resolved.radius = 0.0
    }

    if (msg.angle !== undefined) {
      resolved.angle = msg.angle;
    }
    else {
      resolved.angle = 0.0
    }

    if (msg.covariance !== undefined) {
      resolved.covariance = msg.covariance;
    }
    else {
      resolved.covariance = new Array(4).fill(0)
    }

    if (msg.start !== undefined) {
      resolved.start = msg.start;
    }
    else {
      resolved.start = new Array(2).fill(0)
    }

    if (msg.end !== undefined) {
      resolved.end = msg.end;
    }
    else {
      resolved.end = new Array(2).fill(0)
    }

    return resolved;
    }
};

module.exports = LineSegment;
