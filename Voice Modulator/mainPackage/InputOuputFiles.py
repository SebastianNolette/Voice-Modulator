'''
Created on Nov 30, 2020

@author: Sebastian
'''

import wave
import struct


def InputFile(FilePath):
        
    ReadableAudioFile = {} #This creates a dictiony to hold the information So I can edit it later.
    
    OpenedFile = wave.open(FilePath, 'rb')
    
    ReadableAudioFile['Channels']= OpenedFile.getnchannels();       # Gets the audio channels: mono vs. Stereo
    ReadableAudioFile['SampleWidth']= OpenedFile.getsampwidth();    # Gets Sample Width
    ReadableAudioFile['FrameRate']= OpenedFile.getframerate();      # Gets the Frame Rate of the audio file
    ReadableAudioFile['Frames']= OpenedFile.getnframes();           # Gets the number of frames, This is the number of datapoints
    ReadableAudioFile['Compression']= OpenedFile.getcomptype();     # This determines how the file is compressed    

    '''
    # This is incorrect, It only goes up to 256, not what the actual number is.
    #for n in Soun:
        if n < 127:
            NumericSound.append()
        else:
            NumericSound.append(n-256)
    '''
    
    NumericSound = []
    sizes={1: 'B', 2: 'h', 4:'i'}
    
    fmt_size= sizes[ReadableAudioFile['SampleWidth']]
    fmt = "<" + fmt_size * ReadableAudioFile['Channels']
    # This while loop takes all of the information out of the Frames for audio
    while OpenedFile.tell() < ReadableAudioFile['Frames']:
        NumericSound.append(struct.unpack(fmt, OpenedFile.readframes(1)))
    
    ReadableAudioFile['IntData']= NumericSound;
    OpenedFile.close() # This is to close the file
    return ReadableAudioFile


def OutputFile(FileInfo,FilePath):
    NewFile= wave.open(FilePath,'wb')
    
    # These commands set the channels, sample width, and Frame Rate for the New File
    NewFile.setnchannels(FileInfo['Channels'])
    NewFile.setsampwidth(FileInfo['SampleWidth'])
    NewFile.setframerate(FileInfo['FrameRate'])

        
    sizes={1: 'B', 2: 'h', 4:'i'}
    fmt_size= sizes[FileInfo['SampleWidth']]
    fmt = "<" + fmt_size * FileInfo['Channels']
    
    for data in FileInfo['IntData']:
        SoundData = struct.pack(fmt,data[0],data[1])
        NewFile.writeframesraw(SoundData)
    
    NewFile.close()