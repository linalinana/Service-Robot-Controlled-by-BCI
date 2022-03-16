#include<ros/ros.h>
#include<topic_demo/gps.h>
int main(int argc,char** argv){
    ros::init(argc,argv,"talker");
    ros::NodeHandle nh;          
    topic_demo::gps msg;         
    msg.x=1.0;
    msg.y=1.0;
    msg.state="working";
    ros::Publisher pub=nh.advertise<topic_demo::gps>("gps1",1);
    ros::Rate loop_rate(1.0);
    while(ros::ok()){
         msg.x=10;
	 pub.publish(msg);                            
 	 loop_rate.sleep();                          
	}
    return 0;
 }

