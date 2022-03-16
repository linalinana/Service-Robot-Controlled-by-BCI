#include<ros/ros.h>

#include<topic_demo/gps.h>

void gpsCallback(const topic_demo::gps::ConstPtr &msg)
{
	float distance;
	distance=(msg->x)+(msg->y);	
	ROS_INFO("listener:GPS:distance=%f",distance);
}

int main(int argc,char** argv){
	ros::init(argc,argv,"listener");
	ros::NodeHandle n;
	ros::Subscriber sub = n.subscribe("gps1",1,gpsCallback);
	ros::spin();
	return 0;

}
