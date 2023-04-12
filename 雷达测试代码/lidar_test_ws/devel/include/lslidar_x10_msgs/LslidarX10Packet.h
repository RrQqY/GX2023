// Generated by gencpp from file lslidar_x10_msgs/LslidarX10Packet.msg
// DO NOT EDIT!


#ifndef LSLIDAR_X10_MSGS_MESSAGE_LSLIDARX10PACKET_H
#define LSLIDAR_X10_MSGS_MESSAGE_LSLIDARX10PACKET_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace lslidar_x10_msgs
{
template <class ContainerAllocator>
struct LslidarX10Packet_
{
  typedef LslidarX10Packet_<ContainerAllocator> Type;

  LslidarX10Packet_()
    : stamp()
    , data()  {
      data.assign(0);
  }
  LslidarX10Packet_(const ContainerAllocator& _alloc)
    : stamp()
    , data()  {
  (void)_alloc;
      data.assign(0);
  }



   typedef ros::Time _stamp_type;
  _stamp_type stamp;

   typedef boost::array<uint8_t, 2000>  _data_type;
  _data_type data;





  typedef boost::shared_ptr< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> const> ConstPtr;

}; // struct LslidarX10Packet_

typedef ::lslidar_x10_msgs::LslidarX10Packet_<std::allocator<void> > LslidarX10Packet;

typedef boost::shared_ptr< ::lslidar_x10_msgs::LslidarX10Packet > LslidarX10PacketPtr;
typedef boost::shared_ptr< ::lslidar_x10_msgs::LslidarX10Packet const> LslidarX10PacketConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator1> & lhs, const ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator2> & rhs)
{
  return lhs.stamp == rhs.stamp &&
    lhs.data == rhs.data;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator1> & lhs, const ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace lslidar_x10_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> >
{
  static const char* value()
  {
    return "8b4a4c3a12627c71d9c1beffa4ce1941";
  }

  static const char* value(const ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x8b4a4c3a12627c71ULL;
  static const uint64_t static_value2 = 0xd9c1beffa4ce1941ULL;
};

template<class ContainerAllocator>
struct DataType< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> >
{
  static const char* value()
  {
    return "lslidar_x10_msgs/LslidarX10Packet";
  }

  static const char* value(const ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# Raw Leishen LIDAR packet.\n"
"\n"
"time stamp              # packet timestamp\n"
"uint8[2000] data        # packet contents\n"
"\n"
;
  }

  static const char* value(const ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.stamp);
      stream.next(m.data);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct LslidarX10Packet_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::lslidar_x10_msgs::LslidarX10Packet_<ContainerAllocator>& v)
  {
    s << indent << "stamp: ";
    Printer<ros::Time>::stream(s, indent + "  ", v.stamp);
    s << indent << "data[]" << std::endl;
    for (size_t i = 0; i < v.data.size(); ++i)
    {
      s << indent << "  data[" << i << "]: ";
      Printer<uint8_t>::stream(s, indent + "  ", v.data[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // LSLIDAR_X10_MSGS_MESSAGE_LSLIDARX10PACKET_H
