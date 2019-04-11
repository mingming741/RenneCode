#include <Kinect.h>
#include <vector>
#include <string>
#include "fmod.hpp"
#include "fmod_errors.h"

const float DISTANCEFACTOR = 1.0f; // The factor of distance paremeter, not used currently
const int width = 512, height = 424; // The size of the whole graph catched by Kinect
const int blocksize = 32; // The length & height of a square block
const int blocknumber = 3; // The block number of horizantal level 
const int blocklevel = 3; // The block number of vertical level
const int shift = 128; // For horizantal shift interval of each block
const int extend = 54; // For vertical extend interval of each block
const int TimeInterval = 30; // The time interval of Analyze function was excuted 
const float RelativeVolume[3] = { 1.0f, 0.9f, 0.15f }; // The relative volume for different sound source
const bool Information = true; // True means more information for debug
const bool TrainMode = true; //Train mode for 3 block, else for 9 block
static int CurrentTime = 0; // The center counter of the whole function
static FMOD_VECTOR listenerpos = { 0.0f, 0.0f, 0.0f * DISTANCEFACTOR }; // Repersent the listener position of 3D sound
static FMOD_VECTOR pos = { 0.0f * DISTANCEFACTOR, 0.0f, 0.0f }; // Reperesent the position of the 3D sound source 
static FMOD_VECTOR vel = { 0.0f, 0.0f, 0.0f }; // Represent the velocity of this sound

/*Kinect defalut horizantal angle of view is 70.6 degrees, corrsponding depth distance is 361 pixels, vertical angle of view is 60 degrees, 
0 value get: when the depth is not that dark, some pixels value still has some value, so we need a algorithm to detected the 0 range
*/
