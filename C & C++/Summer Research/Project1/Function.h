#include <Kinect.h>
#include <string>
#include "fmod.hpp"
#include "fmod_errors.h"
#include "Parameter.h"
using namespace std;

template<class Interface>
int SafeRelease(Interface *& pInterfaceToRelease); 
//Release the Kinect memory

int KinectInitial(IKinectSensor* pSensor, HRESULT hResult, IDepthFrameSource* pDepthSource, IDepthFrameReader* pDepthReader, IFrameDescription* pDescription);

int CopyToFile(UINT16 * buffer, int width = 512, int height = 424); 
//Copy the Depth data to file for manual check 

int GetDistribution(UINT16 * buffer, int width = 512, int height = 424); 
// Get the depth data distribution 

int VoiceTesting(FMOD::Channel *channel, FMOD::Sound *sound, FMOD::System *system, FMOD::DSP *dsp, FMOD_VECTOR listenerpos, FMOD_VECTOR pos, FMOD_VECTOR vel,int type);  
// Test the 3D audio based on the input type

int DataAnalyze(UINT16 * buffer, FMOD::Channel *channel[blocknumber], FMOD::Sound *sound[blocknumber], FMOD::System *system, FMOD::DSP *dsp, int width = 512, int height = 424);
//Main function for depth data analyze

int ThreeSoundOneTime(UINT16 * buffer, FMOD::Channel *channel[blocknumber], FMOD::Sound *sound[blocknumber], FMOD::System *system, FMOD::DSP *dsp, float depth[blocknumber * blocklevel]);
//Sound generate function, detected and generated sound one time for all three block

int MaxOfThreeSound(UINT16 * buffer, FMOD::Channel *channel[blocknumber], FMOD::Sound *sound[blocknumber], FMOD::System *system, FMOD::DSP *dsp, float depth[blocknumber * blocklevel]);
//Sound generate function, choose the closest block to generate sound

int TimeDivision(UINT16 * buffer, FMOD::Channel *channel[blocknumber], FMOD::Sound *sound[blocknumber], FMOD::System *system, FMOD::DSP *dsp, float depth[blocknumber  * blocklevel]);
//Sound generate function, time Division to give left, middle, right block different time interval to create thier sound 

float BlockAverageAnalyze(UINT16 * buffer, int width = blocksize, int height = blocksize);
//Block analyze function, mainly focus on the average depth of each block

float BlockLevelAnalyze(UINT16 * buffer, int width = blocksize, int height = blocksize);
//Block analyze function, mainly focus on the depth level of each block, this function can detected the part of some big object which cannot show its whole in the small block

void Test();
//For some test reason