#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>

#include <opencv/cv.h>
#include <opencv/highgui.h>

using namespace std;
using namespace cv;

int main(int argc, char *argv[])
{

    Mat matImg = imread("../gogh.jpg", CV_LOAD_IMAGE_GRAYSCALE);
    Mat matImg3 = imread("../gogh.jpg");

    if (matImg.data == NULL) {
        cerr << "Error: Can't find file gogh.jpg" << endl;
        return -1;
    }

    return 0;
}
