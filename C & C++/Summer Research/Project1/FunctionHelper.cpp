#include <Kinect.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "fmod.hpp"
#include "fmod_errors.h"
#include <iostream>
#include <iomanip>
#include "Function.h"
#include <cstdlib>
#include <windows.h>
using namespace std;

int KinectInitial(IKinectSensor* pSensor, HRESULT hResult, IDepthFrameSource* pDepthSource, IDepthFrameReader* pDepthReader, IFrameDescription* pDescription) {
	// for the whole graph's width & height
	unsigned int bufferSize = width * height * sizeof(unsigned short); // initialize the buffer to store the depth data
	unsigned short min = 0, max = 0; // Range ( Range of Depth is 500-8000[mm], Range of Detection is 500-4500[mm] ) 
	pDepthSource->get_DepthMinReliableDistance(&min); // 500
	pDepthSource->get_DepthMaxReliableDistance(&max); // 4500
	std::cout << "Initialize Kinect" << endl;
	std::cout << "Range: " << min << " - " << max << std::endl;
	std::cout << "Width: " << width << "  Height: " << height << std::endl;
	return 1;
}

int CopyToFile(UINT16 * buffer, int width, int height) {
	ofstream f;
	int total = 0;
	string filename = "C:\\Users\\41995\\Desktop\\buffer.txt";
	std::cout << "Write depth data to file: " << endl;
	f.open(filename);
	for (int i = 0; i < height; i++) {
		for (int j = 0; j < width; j++) {
			f << *(buffer + i * height + j) << " ";
			total++;
		}
		f << "\r\n";
	}
	cout << "Successed, total: " << total << endl;
	f.close();
	return -1;
}

int GetDistribution(UINT16 * buffer, int width, int height) {
	UINT16 Data[65536];
	for (int i = 0; i < 65536; i++) {
		Data[i] = 0;
	}
	for (int i = 0; i < width * height; i++) {
		Data[*(buffer + i)]++;
	}
	ofstream f;
	string filename = "C:\\Users\\41995\\Desktop\\buffer.txt";
	std::cout << "Get Distribution:" << endl;
	f.open(filename);
	int start = 1, getstart = 0, end = 8000;
	for (int i = 8000; i > 0; i--) {
		if (Data[i] <= 10) {
			end--;
		}
		else {
			break;
		}
	}
	int line = 0;
	for (int i = 1; i < end; i++) {
		if (Data[i] == 0 && getstart == false) {
			start++;
		}
		else {
			if (getstart == false) {
				getstart = true;
				f << "Start at: " << start << " End at: " << end << "\r\n";
			}
			if (i % 100 == 0) {
				f << "\r\n" << setw(4) << i << " to " << setw(4) << i + 100 << ": ";
			}
			f << setw(3) << Data[i] << " ";
		}
	}
	cout << "Successed " << endl;
	f.close();
	return -1;
}

//3D voice, x->(left & right), y->(front & behind), x->(up & down)
int VoiceTesting(FMOD::Channel *channel, FMOD::Sound *sound, FMOD::System *system, FMOD::DSP *dsp, FMOD_VECTOR listenerpos, FMOD_VECTOR pos, FMOD_VECTOR vel,int type) {
	system->set3DListenerAttributes(0, &listenerpos, &vel, 0, 0);
	channel->set3DAttributes(&pos, &vel);
	system->playSound(sound, 0, true, &channel);
	//system->playDSP(dsp, 0, true, &channel);
	//dsp->setParameterInt(FMOD_DSP_OSCILLATOR_TYPE, 0);
	sound->setMode(FMOD_LOOP_OFF);
	channel->setVolume(1.0f);
	channel->setPaused(false);
	system->update();
	float x, y, z, t = 0,polar = 1;
	cout << "Start voice test, listener position is at (0, 0, 0)" << endl;
	while (true) {
		if (type == 0) {
			cout << "Please Input sound position (x, y, z): ";
			cin >> x >> y >> z;
			std::system("cls");
			cout << "Position x= " << x << " y= " << y << " z= " << z << endl;			
		}
		else if (type == 1) { // round test
			x = sin(t) * 10.0f;
			y = 0;
			z = cos(t) * 10.0f;
			t = t + 0.002f;
			if (t >= 180.0f) {
				t = 0.0f;
			}
			//std::system("cls");
			cout << "Position x= " << x << " y= " << y << " z= " << z << endl;
		}
		else if (type == 2) { //linear test
			x = t;
			y = 0;
			z = 0;
			t = t + 0.02f * polar;
			if (t >= 8.0f || t <= -8.0f) {
				polar = polar * -1;
			}
			//std::system("cls");
			cout << "Position x= " << x << " y= " << y << " z= " << z << endl;
		}
		pos = { x, y, z };
		channel->setMode(FMOD_3D);
		channel->set3DAttributes(&pos, &vel);
		channel->setVolume(5.0f);
		channel->setPaused(false);
		system->update();
	}
	return -1;
}

void Test() {
	
}
