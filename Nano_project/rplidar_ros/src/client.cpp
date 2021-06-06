/*
 * Copyright (c) 2014, RoboPeak
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without 
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, 
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice, 
 *    this list of conditions and the following disclaimer in the documentation 
 *    and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */
/*
 *  RoboPeak LIDAR System
 *  RPlidar ROS Node client test app
 *
 *  Copyright 2009 - 2014 RoboPeak Team
 *  http://www.robopeak.com
 * 
 */


#include "ros/ros.h"
#include "sensor_msgs/LaserScan.h"
#include <iostream>
#include <fstream>
#include <eigen3/Eigen/Eigen>
#include <math.h>
#include <vector>
// #include "matplotlibcpp.h"
// namespace plt = matplotlibcpp;
using namespace std;
using namespace Eigen;
int number = 1; // The number of point cloud

#define RAD2DEG(x) ((x)*180./M_PI)

Matrix<float,1,2> transform(float angle,float distance)
{
    Matrix<float,1,2> m;
    m(0,0) = distance * sin(angle/180*M_PI);
    m(0,1) = distance * cos(angle/180*M_PI);
    return m;
}

void scanCallback(const sensor_msgs::LaserScan::ConstPtr& scan)
{
    int count = scan->scan_time / scan->time_increment;
    ROS_INFO("I heard a laser scan %s[%d]:", scan->header.frame_id.c_str(), count);
    ROS_INFO("angle_range, %f, %f", RAD2DEG(scan->angle_min), RAD2DEG(scan->angle_max));
    
    //init
    int length = 800;
    Matrix<float,1,2> mat;
    Matrix<float,800,2> Mat;
    Matrix<float,800,2> src_pc; // old
    Matrix<float,800,2> tar_pc; // new
    float pre_degree = 200; // First scan must turning!!
    int order = 0; // Every point cloud's order
    for(int i = 0; i < count; i++) {
        float degree = RAD2DEG(scan->angle_min + scan->angle_increment * i);
        ROS_INFO(": [%f, %f]", degree, scan->ranges[i]);
        //TODO
        // cout << "I am here!!" << endl;
        mat = transform(degree,scan->ranges[i]);
        Mat(order,0) = mat(0,0);
        Mat(order,1) = mat(0,1);
        // cout << order << "results: " << Mat(order, 0) << "  " << Mat(order, 1) << endl;
        // cout << "Matrix : " << Mat << endl;
        if(pre_degree > degree)
        {
            order = 0;
            cout << "Mat : " << endl << Mat << endl;
            src_pc = tar_pc;
            tar_pc = Mat;
            // Save into txt
            cout << "I am gona write data into txt file!!!" << endl;
            fstream output_stream;
            output_stream.open("/home/fanghaow/dev/catkin_ws/src/rplidar_ros/src/matrix.txt",ios::out | ios::app);
            output_stream << "No. " << number << " point cloud" <<endl;
            output_stream << tar_pc << endl;
            output_stream << "The end of No. " << number << " point cloud" << endl;
            // Caculate the sum of absolute error between src_pc and tar_pc
            float abs_sum = 0;
            for(int i =0; i<length; i++)
            {
                if(isnan(abs(src_pc(i,0)-tar_pc(i,0))) || isinf(abs(src_pc(i,0)-tar_pc(i,0))))
                {
                    cout << "nan or inf" << endl;
                }
                else
                {
                    abs_sum += abs(src_pc(i,0)-tar_pc(i,0));
                    abs_sum += abs(src_pc(i,1)-tar_pc(i,1));
                }
            }
            cout << "Sum of absolute difference : " << abs_sum << endl;
            cout << "$$$$$$$$$$$$$$$$$$#Make a turning!!!#$$$$$$$$$$$$$$$$$$$$$$$" << endl;
            number++;
        }
        pre_degree = degree;
        order++;
    }
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "rplidar_node_client");
    ros::NodeHandle n;

    ros::Subscriber sub = n.subscribe<sensor_msgs::LaserScan>("/scan", 1000, scanCallback);

    ros::spin();

    return 0;
}
