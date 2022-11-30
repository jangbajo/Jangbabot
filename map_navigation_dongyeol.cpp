#include <iostream>
#include <unistd.h>
#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include "std_msgs/String.h"
#include "std_msgs/Int32.h"
#include <string>

using namespace std;

#define UIMODE		1
#define AUTOMODE	2
int startsign = 0;
int mode = UIMODE;
char order[100];

/** function declarations **/
bool moveToGoal(double xGoal, double yGoal, double zGoal, double wGoal);
void startAuto(int num, char* orderlist);

/** declare the coordinates of interest **/

//---------------------------------------------//
ros::Rate rate(2);
ros::NodeHandle n;
//-------------------------------------------//

struct Pos{
	double x;
	double y;
	double z;
	double w;
};

struct Pos pos0 = {1.88, -1.73, -0.50, 0.86};
struct Pos pos1 = {2.83, -3.23, -0.50, 0.86};
struct Pos pos2 = {3.87, -2.67, 0.18, 0.98};
struct Pos pos3 = {3.09, -1.95, -0.96, 0.26};
struct Pos pos4 = {3.28, -1.27, 0.29, 0.95};

bool goalReached = false;
// UIMODE는 1이고, AUTOMODE는 2다.



void modeCallback(const std_msgs::Int32::ConstPtr& msg){
	ROS_INFO("mode: [%d]", msg->data);
	mode = msg->data;
	cout<< mode << '\n';
}
//여기서 메시지를 통해 야 "1,3,4"로 가줘 또는 야 "1,2"로 가줘 같은 스트링을 받음
void autoCallback(const std_msgs::String::ConstPtr& msg){
        ROS_INFO("list order: [%s]", msg->data.c_str());
	if(mode == AUTOMODE){
		int ordernum = strlen(msg->data.c_str());
		cout << "ordernum: " << ordernum << '\n';
		strcpy(order, msg->data.c_str());
		cout << order << '\n';
		startAuto(ordernum, order);
	}
}
//------------------------------------------//
void detectionCallback(const std_msgs::Int32::ConstPtr& msg){
	ROS_INFO("Detcted : [%d]",msg->data);
	while(startsign<=5){
		startsign++;
		rate.sleep();
	}
	startsign = 0 ;
}
//-----------------------------------------//


int main(int argc, char** argv){
	ros::init(argc, argv, "map_navigation_node");
	//ros::NodeHandle n;
	//	ros::Rate rate(2);
	
	ros::Publisher mode_pub = n.advertise<std_msgs::Int32>("uimode", 1000);

	while(true){
		ros::spinOnce();
		ros::Subscriber modesub = n.subscribe("mode", 1000, modeCallback);
		rate.sleep();
		ros::spinOnce();
		ros::Subscriber autosub = n.subscribe("listorder", 1000, autoCallback);
//        	rate.sleep();

		ros::spin();

		return 0;
	}
}

void startAuto(int num, char* orderlist){
	for(int i = 0; i < num; i++){
		char section = orderlist[i];

		cout << section << "구역 이동 시작" << '\n';
		if(section == '1'){
			goalReached = moveToGoal(pos1.x, pos1.y, pos1.z, pos1.w);
			//---------------------------------------//
			rate.sleep()
			ros::Subscriber detectionsub = n.subscribe("detection", 1000, detectionCallback);
			ros::spinOnce();
			//--------------------------------------//
        }
		else if (section == '2'){
			goalReached = moveToGoal(pos2.x, pos2.y, pos2.z, pos2.w);
			//-------------------------------------//
			rate.sleep()
			ros::Subscriber detectionsub = n.subscribe("detection", 1000, detectionCallback);
			ros::spinOnce();
			//---------------------------------------//
		}
		else if (section == '3'){
			goalReached = moveToGoal(pos3.x, pos3.y, pos3.z, pos3.w);
			//---------------------------------------//
			rate.sleep()
			ros::Subscriber detectionsub = n.subscribe("detection", 1000, detectionCallback);
			ros::spinOnce();
			//---------------------------------------//
		}
		else if (section == '4'){
			goalReached = moveToGoal(pos4.x, pos4.y, pos4.z, pos4.w);
			//--------------------------------------//
			rate.sleep()
			ros::Subscriber detectionsub = n.subscribe("detection", 1000, detectionCallback);
			ros::spinOnce();
			//-----------------------------------------//
		}
		if (goalReached){
			ROS_INFO(":) success!!!");
		}
		else{
			ROS_INFO(":( fail ..");
		}
	}

	ROS_INFO("초기 위치 시작");
	goalReached = moveToGoal(pos1.x, pos1.y, 0.0, 1.0);
	goalReached = moveToGoal(pos0.x, pos0.y, pos0.z, pos0.w);
	if (goalReached){
		ROS_INFO("success!!!");
	}
	else{
		ROS_INFO("fail ..");
	}
	mode = UIMODE;
}




bool moveToGoal(double xGoal, double yGoal, double zGoal, double wGoal){

	//define a client for to send goal requests to the move_base server through a SimpleActionClient
	actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> ac("move_base", true);

	//wait for the action server to come up
	while(!ac.waitForServer(ros::Duration(5.0))){
		ROS_INFO("Waiting for the move_base action server to come up");
	}

	move_base_msgs::MoveBaseGoal goal;

	//set up the frame parameters
	goal.target_pose.header.frame_id = "map";
	goal.target_pose.header.stamp = ros::Time::now();

	/* moving towards the goal*/

	goal.target_pose.pose.position.x =  xGoal;
	goal.target_pose.pose.position.y =  yGoal;
	goal.target_pose.pose.position.z =  0.0;
	goal.target_pose.pose.orientation.x = 0.0;
	goal.target_pose.pose.orientation.y = 0.0;
	goal.target_pose.pose.orientation.z = zGoal;
	goal.target_pose.pose.orientation.w = wGoal;

	ROS_INFO("Sending goal location ...");
	ac.sendGoal(goal);

	ac.waitForResult();

	if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED){
		ROS_INFO("You have reached the destination");
		return true;
	}
	else{
		ROS_INFO("The robot failed to reach the destination");
		return false;
	}

}

