#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>

/** function declarations **/
bool moveToGoal(double xGoal, double yGoal, double zGoal, double wGoal);
char choose();

/** declare the coordinates of interest **/

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

int main(int argc, char** argv){
	ros::init(argc, argv, "map_navigation_node");
	ros::NodeHandle n;
//	sound_play::SoundClient sc;
	ros::spinOnce();
//	path_to_sounds = "/home/ros/catkin_ws/src/gaitech_edu/src/sounds/";
	//sc.playWave(path_to_sounds+"short_buzzer.wav");
	//tell the action client that we want to spin a thread by default

	char choice = 'q';
	do{
		choice =choose();
		if (choice == '0'){
			goalReached = moveToGoal(pos0.x, pos0.y, pos0.z, pos0.w);
		}else if (choice == '1'){
			goalReached = moveToGoal(pos1.x, pos1.y, pos1.z, pos1.w);
		}else if (choice == '2'){
			goalReached = moveToGoal(pos2.x, pos2.y, pos2.z, pos2.w);
		}else if (choice == '3'){
			goalReached = moveToGoal(pos3.x, pos3.y, pos3.z, pos3.w);
		}else if (choice == '4'){
                        goalReached = moveToGoal(pos4.x, pos4.y, pos4.z, pos4.w);
                }

		if (choice!='q'){
			if (goalReached){
				ROS_INFO("Congratulations!");
				ros::spinOnce();
//				sc.playWave(path_to_sounds+"ship_bell.wav");
				ros::spinOnce();

			}else{
				ROS_INFO("Hard Luck!");
//				sc.playWave(path_to_sounds+"short_buzzer.wav");
			}
		}
	}while(choice !='q');
	return 0;
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

char choose(){
	char choice='q';
	std::cout<<"|-------------------------------|"<<std::endl;
	std::cout<<"|PRESSE A KEY:"<<std::endl;
	std::cout<<"|'0': Start "<<std::endl;
	std::cout<<"|'1': Snack "<<std::endl;
	std::cout<<"|'2': Ramyun "<<std::endl;
	std::cout<<"|'3': Coke "<<std::endl;
        std::cout<<"|'4': Bread "<<std::endl;
	std::cout<<"|'q': Quit "<<std::endl;
	std::cout<<"|-------------------------------|"<<std::endl;
	std::cout<<"|WHERE TO GO?";
	std::cin>>choice;

	return choice;


}
