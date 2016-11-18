#include <ros/ros.h>
#include <pcl_conversions/pcl_conversions.h>
#include <std_msgs/MultiArrayLayout.h>
#include <std_msgs/MultiArrayDimension.h>
#include <std_msgs/UInt16.h>
#include <std_msgs/UInt8MultiArray.h>
#include <pcl_ros/point_cloud.h>
#include <pcl/point_types.h>
#include <iostream>
#include <vector>

#define PI 3.1415926

typedef pcl::PointCloud<pcl::PointXYZ> PointCloud;

ros::Publisher pub;
int array_size = 512; //check
float angle_range = 2*PI; //adjust

//int direction = 1; //0->180, else 0: 180->0

void process_data (const std_msgs::UInt8MultiArray::ConstPtr& array)
{
  // Create a container for the data
  PointCloud::Ptr msg (new PointCloud);

  msg->header.frame_id = "base_link";
  msg->height = 1; //unordered point cloud
  msg->width = array_size;

  //int i=0;
  float x,y, z=0.0, start_angle = 0.0;
  //(direction==1)?(start_angle = 0.0):(direction = PI);
  
  // iterate through array
  for(int j=0; j<array->data.size(); j++)
  {
    int d = array->data[j]; //in cm

    float theta;

    //if(direction == 0)
    theta = start_angle + j*(angle_range/array_size);
    if(theta >= 2*PI) theta = theta - 2*PI;

    ROS_INFO("%lf", theta);
    //else
      //theta = start_angle - i*(angle_range/array_size);

    //calculate x,y,z
    x = d*cos(theta)/100;
    y = -d*sin(theta)/100;
    z = 0.0; 
    
    //add to point cloud
    msg->points.push_back (pcl::PointXYZ(x, y, z));
  }
  
  //add time stamp
  pcl_conversions::toPCL(ros::Time::now(), msg->header.stamp);

  //if(direction == 1) direction = 0;
  //else direction = 1;
  
  //publish message
  pub.publish (msg);
}

int main(int argc, char** argv)
{
  // Initialize ROS
  ros::init (argc, argv, "pcl_publisher");
  ros::NodeHandle nh;

  // Create a ROS subscriber for the input uint8 array
  ros::Subscriber sub = nh.subscribe("raw_data", 1, process_data);

  //Create a ROS publisher for the output point cloud
  pub = nh.advertise<PointCloud> ("range_map", 1);

  // Spin
  ros::spin ();
}