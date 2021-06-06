#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <eigen3/Eigen/Eigen>
// #include <opencv2>
using namespace std;
using namespace Eigen;

Matrix<float,800,2> mat()
{
    Matrix<float,800,2> m;
    for(int i=0; i<800; i++)
    {
        m(i,0) = i;
        m(i,1) = i * i * 2;
    }
    cout << m << endl;
    return m;
}

int main()
{
    Matrix<float,800,2> matrix = mat();
    fstream output_stream;
    output_stream.open("matrix.txt",ios::out | ios::app);
    output_stream << matrix << endl;
    return 0;
}