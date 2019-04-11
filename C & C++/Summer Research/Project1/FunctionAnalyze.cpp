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
using namespace std;

//Generate sound in "blocknumber" block simultaneously (will be noise if 2 sound alert at same time)
int ThreeSoundOneTime(UINT16 * buffer, FMOD::Channel *channel[blocknumber], FMOD::Sound *sound[blocknumber], FMOD::System *system, FMOD::DSP *dsp, float depth[blocknumber * blocklevel]) {
	float posx[blocknumber], posz = 0.0f;
	float distance[blocknumber];
	for (int i = 0; i < 3; i++) {
		depth[i] = depth[i * 3 + 1];
	}
	for (int i = 0; i < blocknumber; i++) {
		int reset = shift * (i - (blocknumber / 2));
		posx[i] = depth[i] * reset / 471;
		distance[i] = sqrt(posx[i] * posx[i] + depth[i] * depth[i] + 1.0f);
		if (distance[i] <= 3.5f) {
			pos = { posx[i] * DISTANCEFACTOR, depth[i], 0.0f };
			cout << "Get valid point: " << endl;
			cout << setprecision(3) << "Index: "  << i << " Depth: " << depth[i] << " Shift: " << posx[i] << " Distance: " << distance[i];
			float volume = 1 / sqrt(pos.x * pos.x + pos.y * pos.y + pos.z * pos.z);
			system->playSound(sound[i], 0, true, &channel[i]);
			channel[i]->setVolume(volume);
			cout << " Volume = " << volume << endl;
			channel[i]->set3DAttributes(&pos, &vel);
			channel[i]->setPaused(false);
		}
	}
	return -1;
}

//Generate 1 sound choose the block closest with user (cannot get the actural distance)
int MaxOfThreeSound(UINT16 * buffer, FMOD::Channel *channel[blocknumber], FMOD::Sound *sound[blocknumber], FMOD::System *system, FMOD::DSP *dsp, float depth[blocknumber * blocklevel]) {
	float posx[blocknumber], posz = 0.0f;
	float max = depth[0];
	int index = 1;
	for (int i = 0; i < blocknumber; i++) {
		int reset = shift * (i - (blocknumber / 2));
		posx[i] = depth[i] * reset / 471;
		if (depth[i] < depth[index]) {
			index = i;
		}
	}
	float distance = sqrt(posx[index] * posx[index] + depth[index] * depth[index] + 1.0f);
	cout << "Close point is: " << "Index: " << index << endl;
	cout << setprecision(3) << "Depth: " << depth[index] << " Shift: " << posx[index] << " Distance: " << distance << endl;
	pos = { posx[index] * DISTANCEFACTOR, depth[index], 0.0f };
	float volume = 1 / sqrt(pos.x * pos.x + pos.y * pos.y + pos.z * pos.z);
	//system->playSound(sound[index], 0, true, &channel[index]);
	system->playDSP(dsp, 0, true, &channel[index]);
	float frequency;
	channel[index]->getFrequency(&frequency);
	frequency = frequency + (distance - 1.0f) * 500;
	channel[index]->setFrequency(frequency);
	if (index == 0) {
		dsp->setParameterInt(FMOD_DSP_OSCILLATOR_TYPE, 0);
	}
	else if (index == 1) {
		dsp->setParameterInt(FMOD_DSP_OSCILLATOR_TYPE, 4);
	}
	else if (index == 2) {
		dsp->setParameterInt(FMOD_DSP_OSCILLATOR_TYPE, 5);
	}
	channel[index]->setVolume(volume);
	cout << "Volume = " << volume << " Frequency = " << (int)frequency << endl;
	channel[index]->set3DAttributes(&pos, &vel);
	channel[index]->setPaused(false);
	return -1;
}

//Block average depth
float BlockAverageAnalyze(UINT16 * buffer, int width, int height) {
	int sum = 0, total = 0;
	for (int i = 0; i < width * height; i++) {
		if (*(buffer + i) != 0) {
			sum = sum + *(buffer + i);
			total++;
		}
	}
	float average = (float)sum / (total * 1000);
	if (total == 0) {
		average = -0.1f;
		cout << "Too close!" << endl;
	}
	else if (total >= width * height * 0.9 || average >= 3.0f) {
		average = (float)sum / (total * 1000);
	}
	else if (total >= width * height * 0.6 || average >= 1.5f) {
		average = (float)sum / ((total + (width * height - total) / 2) * 1000);
	}
	else {
		average = (float)sum / (width * height * 1000);
	}
	cout << "Total valid pixel:" << total << " Depth: " << average << endl;;
	return average;
}

float BlockLevelAnalyze(UINT16 * buffer, int width, int height) {
	const int LevelIntervel = 500;
	const int LevelNumber = 8000 / LevelIntervel;
	const int threshold = blocksize * blocksize / 4;
	int Levels[LevelNumber];
	int Level = 0,total = 0;
	for (int i = 0; i < width * height; i++) {
		if (*(buffer + i) != 0) {
			total++;
		}
	}
	if (total == 0) {
		if (Information == true) {
			cout << "Too close!" << endl;
		}	
		return -0.1f;
	}
	else if (total < blocksize * blocksize / 2) {
		if (Information == true) {
			cout << "Valid Pixel is not enough!" << endl;
		}	
		return -0.1f;
	}
	for (int i = 0; i < LevelNumber; i++) {
		Levels[i] = 0;
	}
	for (int i = 0; i < width * height; i++) {
		Level = buffer[i] / LevelIntervel;
		Levels[Level]++;
	}
	Level = LevelNumber - 1;
	for (int i = 1; i < LevelNumber; i++) {
		if (Levels[i] > threshold) {
			Level = i;
			break;
		}
	}
	float result = 0;
	total = 0;
	for (int i = 0; i < width * height; i++) {
		if (buffer[i] >= Level * LevelIntervel || buffer[i] <= (Level + 1) * LevelIntervel) {
			result = result + (float)buffer[i];
			total++;
		}
	}
	result = (result / 1000.0f) / (total);
	if (Information == true) {
		cout << "Total valid pixel:" << total << " Level: " << Level << " Depth: " << result << endl;
	}
	else {
		cout << setw(10) << result << " ";
	}
	return result;
}