// Generated by gencpp from file ur_dashboard_msgs/RawRequest.msg
// DO NOT EDIT!


#ifndef UR_DASHBOARD_MSGS_MESSAGE_RAWREQUEST_H
#define UR_DASHBOARD_MSGS_MESSAGE_RAWREQUEST_H

#include <ros/service_traits.h>


#include <ur_dashboard_msgs/RawRequestRequest.h>
#include <ur_dashboard_msgs/RawRequestResponse.h>


namespace ur_dashboard_msgs
{

struct RawRequest
{

typedef RawRequestRequest Request;
typedef RawRequestResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct RawRequest
} // namespace ur_dashboard_msgs


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::ur_dashboard_msgs::RawRequest > {
  static const char* value()
  {
    return "3f9d6cecb9ae062492929b790df89058";
  }

  static const char* value(const ::ur_dashboard_msgs::RawRequest&) { return value(); }
};

template<>
struct DataType< ::ur_dashboard_msgs::RawRequest > {
  static const char* value()
  {
    return "ur_dashboard_msgs/RawRequest";
  }

  static const char* value(const ::ur_dashboard_msgs::RawRequest&) { return value(); }
};


// service_traits::MD5Sum< ::ur_dashboard_msgs::RawRequestRequest> should match
// service_traits::MD5Sum< ::ur_dashboard_msgs::RawRequest >
template<>
struct MD5Sum< ::ur_dashboard_msgs::RawRequestRequest>
{
  static const char* value()
  {
    return MD5Sum< ::ur_dashboard_msgs::RawRequest >::value();
  }
  static const char* value(const ::ur_dashboard_msgs::RawRequestRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::ur_dashboard_msgs::RawRequestRequest> should match
// service_traits::DataType< ::ur_dashboard_msgs::RawRequest >
template<>
struct DataType< ::ur_dashboard_msgs::RawRequestRequest>
{
  static const char* value()
  {
    return DataType< ::ur_dashboard_msgs::RawRequest >::value();
  }
  static const char* value(const ::ur_dashboard_msgs::RawRequestRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::ur_dashboard_msgs::RawRequestResponse> should match
// service_traits::MD5Sum< ::ur_dashboard_msgs::RawRequest >
template<>
struct MD5Sum< ::ur_dashboard_msgs::RawRequestResponse>
{
  static const char* value()
  {
    return MD5Sum< ::ur_dashboard_msgs::RawRequest >::value();
  }
  static const char* value(const ::ur_dashboard_msgs::RawRequestResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::ur_dashboard_msgs::RawRequestResponse> should match
// service_traits::DataType< ::ur_dashboard_msgs::RawRequest >
template<>
struct DataType< ::ur_dashboard_msgs::RawRequestResponse>
{
  static const char* value()
  {
    return DataType< ::ur_dashboard_msgs::RawRequest >::value();
  }
  static const char* value(const ::ur_dashboard_msgs::RawRequestResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // UR_DASHBOARD_MSGS_MESSAGE_RAWREQUEST_H