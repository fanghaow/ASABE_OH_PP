#include <iostream>
#include <vector>
#include <map>
#include <eigen3/Eigen/Eigen>
using namespace std;
using namespace Eigen;

void mat()
{
    Matrix<float,2,2> m;
    m(0,0) = 1;
    m(0,1) = 2;
    m(1,0) = 3;
    m(1,1) = 4;
    cout << m << endl;
}

// Outter map 0.01, inner map 0.1
int main()
{
    int global_time = 0;
    int data_len = 2;
    float key = 0;
    float value = 0.00;
    map<int, map<float,float> > all_pos;
    map<float,float> angle_dist;
    map<int, map<float,float> >::iterator iter1;
    map<float,float>::iterator iter2;
    for(int ii=0; ii<100; ii++)
    {
        float keykey = 0;
        float valuevalue = 0;
        for(int j=0; j<360; j++)
        {
            angle_dist[keykey] = valuevalue + value;
            keykey += 1;
            valuevalue += 0.1;
        }
        all_pos[global_time] = angle_dist;

        if(all_pos.size() > data_len)
        {
            for(iter1 = all_pos.begin(); iter1 != all_pos.end();)
            {
                if(iter1->first == global_time-data_len)
                    all_pos.erase(iter1++);
                else
                {
                    iter1++;
                }
            }
            // global_time += 1;
            cout << endl;
        }

        for(iter1=all_pos.begin(); iter1!=all_pos.end(); iter1++)
        {
            for(iter2=iter1->second.begin(); iter2!=iter1->second.end(); iter2++)
            {
                cout << iter1->first << " : " << iter2->first << " : " << iter2->second << endl;
                
            }
        }

        angle_dist.clear();
        global_time++;
        key++;
        value += 0.01;
    }
    mat();
}