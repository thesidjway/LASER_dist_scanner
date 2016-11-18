#include <ros/ros.h>
#include <std_msgs/MultiArrayLayout.h>
#include <std_msgs/MultiArrayDimension.h>
#include <std_msgs/UInt8MultiArray.h>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "test_publisher");

	ros::NodeHandle n;

	ros::Publisher pub = n.advertise<std_msgs::UInt8MultiArray>("raw_data", 2);

	while (ros::ok())
	{
		std_msgs::UInt8MultiArray array;
		//Clear array
		array.data.clear();
		//for loop, pushing data in the size of the array
		for (int i = 0; i < 512; i++)
		{
			//assign array a random number between 0 and 255.
			array.data.push_back(20);
		}
		//Publish array
		pub.publish(array);
		//Do this.
		ros::spinOnce();
	}
}