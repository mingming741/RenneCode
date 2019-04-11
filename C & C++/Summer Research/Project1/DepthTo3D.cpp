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
#include <cmath>
using namespace std;

int main(){
	IKinectSensor* pSensor = NULL; //Initialize the Kinect camera
	HRESULT hResult = S_OK;
	IDepthFrameSource* pDepthSource = NULL; // Source, get the source data
	IDepthFrameReader* pDepthReader = NULL; // Reader, point to the source, read the data from the source
	IFrameDescription* pDescription = NULL; // Description, description the data property of the source data
	hResult = GetDefaultKinectSensor(&pSensor); //link with the input kinect
	if (FAILED(hResult)) {
		std::cerr << "Error : GetDefaultKinectSensor" << std::endl;
		return -1;
	}
	hResult = pSensor->Open();  //open the sensor
	if (FAILED(hResult)) {
		std::cerr << "Error : IKinectSensor::Open()" << std::endl;
		return -1;
	}
	hResult = pSensor->get_DepthFrameSource(&pDepthSource);
	if (FAILED(hResult)) {
		std::cerr << "Error : IKinectSensor::get_DepthFrameSource()" << std::endl;
		return -1;
	}
	hResult = pDepthSource->OpenReader(&pDepthReader);
	if (FAILED(hResult)) {
		std::cerr << "Error : IDepthFrameSource::OpenReader()" << std::endl;
		return -1;
	}
	hResult = pDepthSource->get_FrameDescription(&pDescription);
	if (FAILED(hResult)) {
		std::cerr << "Error : IDepthFrameSource::get_FrameDescription()" << std::endl;
		return -1;
	}
	KinectInitial(pSensor, hResult, pDepthSource, pDepthReader, pDescription);
	
	//Initialize the 3D sound 
	FMOD::System *system = NULL;
	FMOD::DSP *dsp = NULL;
	FMOD::Channel *channel[blocknumber];
	FMOD::Sound *sound[blocknumber];
	FMOD::System_Create(&system);	// Create system
	system->init(36, FMOD_INIT_NORMAL, NULL);
	system->createDSPByType(FMOD_DSP_TYPE_OSCILLATOR, &dsp);
	dsp->setParameterFloat(FMOD_DSP_OSCILLATOR_RATE, 440.0f); /* Musical note 'A' */
	system->set3DSettings(1.0, DISTANCEFACTOR, 1.0f);
	system->set3DListenerAttributes(0, &listenerpos, &vel, 0, 0);
	system->createSound("..\\Audio\\A cat.mp3", FMOD_3D, 0, &sound[0]); //Create 3D sound
	system->createSound("..\\Audio\\heli.wav", FMOD_3D, 0, &sound[1]); //Create 3D sound
	system->createSound("..\\Audio\\e.ogg", FMOD_3D, 0, &sound[2]); //Create 3D sound
	for (int i = 0; i < blocknumber; i++) {
		channel[i] = NULL;
		sound[i]->setMode(FMOD_LOOP_NORMAL);
		sound[i]->set3DMinMaxDistance(0.2f * DISTANCEFACTOR, 5000.0f * DISTANCEFACTOR);
	}
	// Play the sound, with loop mode
	/*for (int i = 0; i < blocknumber; i++) {
	system->playSound(sound[i], 0, true, &channel[i]);
	channel[i]->set3DAttributes(&pos, &vel);
	channel[i]->setVolume(1.0f);
	channel[i]->setPaused(false);
	}*/
	system->update();
	
	//Progress
	cout << "Process Starting " << endl;
	int total = 0;
	while (CurrentTime >= 0) {
		vector<UINT16> depthBuffer(width * height);
		IDepthFrame* pDepthFrame = nullptr;
		hResult = pDepthReader->AcquireLatestFrame(&pDepthFrame);
		if (SUCCEEDED(hResult)) {
			if (CurrentTime % TimeInterval == 0) {
				total++;
				cout << "Time: " << total << " State:" << endl;
				hResult = pDepthFrame->CopyFrameDataToArray(depthBuffer.size(), &depthBuffer[0]);
				if (SUCCEEDED(hResult)) {
					//VoiceTesting(channel[0], sound[1], system, dsp, listenerpos, pos, vel,2);
					DataAnalyze(&depthBuffer[0],channel,sound,system,dsp);
					system->update();
				}		
				cout << endl;
			}	
			int TimeStop = TimeInterval / 2;
			if (CurrentTime % TimeInterval == TimeStop) {
				for (int i = 0; i < blocknumber; i++) { 
					if (channel[i] != NULL) {
						channel[i]->stop();
					}			
				}
			}
			CurrentTime++;
			//cout << "Current time: " << time << endl;
		}
		SafeRelease(pDepthFrame);
	}
	//Close the camera and sound file
	SafeRelease(pDepthSource);
	SafeRelease(pDepthReader);
	SafeRelease(pDescription);
	if (pSensor) {
		pSensor->Close();
	}
	SafeRelease(pSensor);
	for (int i = 0; i < blocknumber; i++) {
		sound[i]->release();
	}	
	return 0;
}

//Main function for data analyze
int DataAnalyze(UINT16 * buffer, FMOD::Channel *channel[blocknumber], FMOD::Sound *sound[blocknumber], FMOD::System *system, FMOD::DSP *dsp, int width, int height) {
	UINT16 left[3][blocksize * blocksize], middle[3][blocksize * blocksize], right[3][blocksize * blocksize];
	int half = blocksize / 2;
	for (int m = 0; m < blocksize; m++) {
		for (int n = 0; n < blocksize; n++) {
			//cout << "Move to: " << move << " position" << endl;
			for (int k = 0; k < 3; k++) {
				int move = (width * (m + 212 + (k - 1) * extend - half)) + n + 256 - half;
				middle[k][m * blocksize + n] = *(buffer + move);
				left[k][m * blocksize + n] = *(buffer + move + shift);
				right[k][m * blocksize + n] = *(buffer + move - shift);
			}		
		}
	}
	float depth[blocknumber * blocklevel];
	if (Information == false) {
		cout << " " << setw(10) << "Left " << setw(10) << " Middle " << setw(10) << " Right " << endl;
		if (TrainMode == false) {
			for (int i = 0; i < 3; i++) {
				cout << i << " ";
				depth[i] = BlockLevelAnalyze(&left[i][0]);
				depth[3 + i] = BlockLevelAnalyze(&middle[i][0]);
				depth[6 + i] = BlockLevelAnalyze(&right[i][0]);
				cout << endl;
			}
		}
		else if (TrainMode == true) {
			cout << "State:";
			depth[0] = BlockLevelAnalyze(&left[1][0]);
			depth[1] = BlockLevelAnalyze(&middle[1][0]);
			depth[2] = BlockLevelAnalyze(&right[1][0]);
			cout << endl;
		}
		
	}
	else {
		if (TrainMode == false) {
			cout << "Left: " << endl;
			for (int i = 0; i < 3; i++) {
				cout << "Position: " << i << " ";
				depth[i] = BlockLevelAnalyze(&left[i][0]);
			}
			cout << "Middle: " << endl;
			for (int i = 0; i < 3; i++) {
				cout << "Position: " << i << " ";
				depth[3 + i] = BlockLevelAnalyze(&middle[i][0]);
			}
			cout << "Right: " << endl;
			for (int i = 0; i < 3; i++) {
				cout << "Position: " << i << " ";
				depth[6 + i] = BlockLevelAnalyze(&right[i][0]);
			}
		}
		else if (TrainMode == true) {
			cout << "Left:   "; depth[0] =  BlockLevelAnalyze(&left[1][0]);		
			cout << "Middle: ";  depth[1] = BlockLevelAnalyze(&middle[1][0]);
			cout << "Right:  ";  depth[2] = BlockLevelAnalyze(&right[1][0]);
		}
	}
	TimeDivision(buffer, channel, sound, system, dsp, depth);
	//MaxOfThreeSound(buffer, channel, sound, system, dsp, depth);
	//ThreeSoundOneTime(buffer, channel, sound, system, dsp, depth);
	return -1;
}

//Give 3 sound different(individual) time to alert the user
int TimeDivision(UINT16 * buffer, FMOD::Channel *channel[blocknumber], FMOD::Sound *sound[blocknumber], FMOD::System *system, FMOD::DSP *dsp, float depth[blocknumber  * blocklevel]) {
	int index = (CurrentTime % (TimeInterval * blocknumber)) / TimeInterval;
	int reset = shift * (index - (blocknumber / 2));
	const float angle = atan(shift / 361);
	float array[3]; int whichindex[3];
	for (int i = 0; i < 3; i++) {
		array[i] = 200.0f;
	}
	if (TrainMode == false) {
		for (int i = 0; i < 3; i++) {
			for (int j = 0; j < 3; j++) {
				if (array[i] > depth[3 * i + j]) {
					array[i] = depth[3 * i + j];
					whichindex[i] = j;
				}
			}
		}
		cout << "Horizantal Index is: " << index << " Vertical Index is " << whichindex[index] << endl;
	}
	else if (TrainMode == true) {
		for (int j = 0; j < 3; j++) {
			array[j] = depth[j];
			whichindex[j] = 1;
		}
	}
	if (Information == true) {
		cout << setprecision(3) << "Depth: " << array[index] << " Horizantal: " << array[index] * sin(angle) << " Distance: " << array[index] << endl;
	}
	
	if (array[index] <= 3.0f) {
		pos = { array[index] * sin(angle), array[index] * cos(angle), 0.0f };
		float volume = 2 / (pos.x * pos.x + pos.y * pos.y + pos.z * pos.z) * RelativeVolume[index];
		//system->playSound(sound[index], 0, true, &channel[index]);
		system->playDSP(dsp, 0, true, &channel[index]);
		float frequency;
		channel[index]->getFrequency(&frequency);
		frequency = frequency * pow(0.5f, (double)(whichindex[index] - 1));
		channel[index]->setFrequency(frequency);
		if (index == 0) {
			dsp->setParameterInt(FMOD_DSP_OSCILLATOR_TYPE, 0);
		}
		else if (index == 1) {
			dsp->setParameterInt(FMOD_DSP_OSCILLATOR_TYPE, 4);
		}
		else if (index == 2) {
			dsp->setParameterInt(FMOD_DSP_OSCILLATOR_TYPE, 2);
		}
		channel[index]->setVolume(volume);
		if (Information) {
			cout << "Volume = " << volume << " Frequency = " << (int)frequency << endl;
		}	
		channel[index]->setMode(FMOD_3D);
		channel[index]->set3DAttributes(&pos, &vel);
		channel[index]->setPaused(false);
	}
	return -1;
}

template<class Interface>
int SafeRelease(Interface *& pInterfaceToRelease) {
	if (pInterfaceToRelease != NULL) {
		pInterfaceToRelease->Release();
		pInterfaceToRelease = NULL;
	}
	return -1;
}