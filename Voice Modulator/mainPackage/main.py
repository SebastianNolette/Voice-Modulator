'''
Created on Sep 18, 2020

@author: Sebastian
'''

import sys


import numpy as np
import sounddevice

import mainPackage.InputOuputFiles as InOut
import mainPackage.AudioManipulation as AudManip


'''
Unused Code that hopefully would allow me to record and play sound

def OutputSound(FileData,OutputDevice):
    
    Length=FileData['Frames']
    Channels=FileData['Channels']
    SampleRate=FileData['FrameRate']
    
    NumpyArray=np.zeros((Length,Channels))
    
    i=0
    for data in FileData['IntData']:
        NumpyArray[i][0]=data[0]
        NumpyArray[i][1]=data[1]
        i+= 1
    
    sounddevice.play(NumpyArray, SampleRate)
    sounddevice.OutputStream()
    print()
    
def MicInput(InputDevice):
    
    ReadableAudioFile={}
    SampleRate=44100
    Channels=2
    Duration=1
    SoundData=sounddevice.rec(int(Duration*SampleRate),samplerate=SampleRate,channels=Channels)
    SoundData=sounddevice.InputStream(samplerate=SampleRate,channels=Channels,dtype='int16')
    
    ReadableAudioFile['Channels']= Channels             # Gets the audio channels: mono vs. Stereo
    ReadableAudioFile['SampleWidth']= 2                 # Gets Sample Width
    ReadableAudioFile['FrameRate']= SampleRate;         # Gets the Frame Rate of the audio file
    ReadableAudioFile['Compression']= 'NONE'
    
    AudioFrames=[]
    for i in SoundData:
        AudioFrames.append((round(i[0]),round(i[1])))   # Translates NumPy into my Data format
           
    ReadableAudioFile['IntData']=AudioFrames
    ReadableAudioFile['Frames']=len(AudioFrames)    

    return ReadableAudioFile
'''
# Translates NumPy into my Data format   
def CallBack(indata,outdata, frames, time, status):

    Audio={}
    Audio['Channels']= 2             
    Audio['SampleWidth']= 2                 
    Audio['FrameRate']= 44100;         
    Audio['Compression']= 'NONE'
    
    AudioFrames=[]
    for i in indata:
        AudioFrames.append((round(i[0]),round(i[1])))
    Audio['IntData']=AudioFrames
    Audio['Frames']=len(AudioFrames)   
     
    pitch=float(sys.argv[3])
    #Change the sound data
    Audio=AudManip.PitchShift(Audio,pitch)    

    NumpyArray=np.zeros((Audio['Frames'],2))
    #Translates back into NumPy
    i=0
    for data in Audio['IntData']:
        NumpyArray[i][0]=data[0]
        NumpyArray[i][1]=data[1]
        i+= 1
        
    outdata[:]=NumpyArray   


def AudioStream(InputDevice, OutputDevice):
    
    SampleRate=44100
    Channels=2    
    
    
    with sounddevice.Stream(device=(InputDevice,OutputDevice),
                            samplerate=SampleRate,channels=Channels,
                            dtype='int16',callback=CallBack,blocksize=44100):
        print('#' * 80)
        print('press Return to quit')
        print('#' * 80)
        input()

# In order to tell Which input outputs there are use
# py -m sounddevice

'''
Run configurations
For Files:
"C:\eclipse-workspace\Senior Project\I Find Lack of Faith - Normal.wav"
"C:\eclipse-workspace\Senior ProjectI Find Lack of Faith - New Test.wav"
0.5
For Live Voice:
1
4
0.8
Real
'''



def main():
    if len(sys.argv)==4:
        File=sys.argv[1]
        FileChanged=sys.argv[2]
        pitch=float(sys.argv[3])
        
        DataFile=InOut.InputFile(File)       
        AudManip.PitchShift(DataFile,pitch)
        InOut.OutputFile(DataFile,FileChanged)       
        
    elif len(sys.argv)==5:

        InputAudio=int(sys.argv[1])
        OutputAudio=int(sys.argv[2])
        AudioStream(InputAudio, OutputAudio)
        
    else:
        print("Incorrect Argument")
        print("Try 'File Input Path' 'File Output Path' 'Pitch by float'")
        print("Try 'Input Device' 'Output Device' 'Pitch by float' '(Real)/(Store)'")

    print("Done")

main()

if __name__ == '__main__':
    pass