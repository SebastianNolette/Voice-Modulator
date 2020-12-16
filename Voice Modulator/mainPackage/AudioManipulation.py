'''
Created on Nov 30, 2020

@author: Sebastian
'''

import math

import numpy as np
from numpy.f2py.auxfuncs import throw_error


def LinInterpol(x,x1,x0,y1,y0):
    # Function to Linearly interpolate between 2 points
    y = y0 *(x1-x) + y1* (x-x0)
    y = y/(x1-x0)
    
    return y;

def OffsetSound(FileInfo,Offset):
    #
    NewData=[]
    FirstChannel=0
    SecondChannel=0
    
    for i in range(0,Offset):
        NewData.append(FileInfo['IntData'][i])
        
    for i in range(Offset,FileInfo['Frames']):
        
        if ((FileInfo['IntData'][i][0]+FileInfo['IntData'][i-Offset][0])<-32768):
            FirstChannel=-32768
        elif ((FileInfo['IntData'][i][0]+FileInfo['IntData'][i-Offset][0])>32767):
            FirstChannel=32767
        else:
            FirstChannel=(FileInfo['IntData'][i][0]+FileInfo['IntData'][i-Offset][0])
        
        if ((FileInfo['IntData'][i][1]+FileInfo['IntData'][i-Offset][1])<-32768):
            SecondChannel=-32768
        elif ((FileInfo['IntData'][i][1]+FileInfo['IntData'][i-Offset][1])>32767):
            SecondChannel=32767
        else:
            SecondChannel=(FileInfo['IntData'][i][1]+FileInfo['IntData'][i-Offset][1])                          
                
        OffsetData=(FirstChannel,SecondChannel)
        NewData.append(OffsetData)
        
    #OffsetData=(FileInfo['IntData'][i][0]+FileInfo['IntData'][i-Offset][0],FileInfo['IntData'][i][1]+FileInfo['IntData'][i-Offset][1])
    
        
    return NewData

def PitchChange(FileInfo, NewPitchRatio):
    Len=FileInfo['Frames']
    NewLen=Len*1.0/NewPitchRatio
    
    NewData=[]
    FirstChannel=0
    SecondChannel=0
    
    for i in range(0,round(NewLen)):
        OldI=i*NewPitchRatio
        COldI=math.ceil(OldI)
        FOldI=math.floor(OldI)
        if COldI > Len:
            print("Uh oh, OldI > Length of Frames")
        if COldI != FOldI:
            try:
                FirstChannel= round(LinInterpol(OldI,FOldI,COldI,FileInfo['IntData'][FOldI][0],FileInfo['IntData'][COldI][0]))
                SecondChannel= round(LinInterpol(OldI,FOldI,COldI,FileInfo['IntData'][FOldI][1],FileInfo['IntData'][COldI][1]))      
            except: # This Runs when the Ceiling to too high dues to COldI
                FirstChannel=FileInfo['IntData'][FOldI][0]
                SecondChannel=FileInfo['IntData'][FOldI][1] 
        else:
            FirstChannel=FileInfo['IntData'][FOldI][0]
            SecondChannel=FileInfo['IntData'][FOldI][1]         
        
        ChangedVal=(FirstChannel,SecondChannel)
        
        try:
            NewData.append(ChangedVal)
        except:
            print('Old Length' + str(Len))
            print('Error Will Robinson' + str(OldI)) 

    
    FileInfo['IntData']=NewData
    FileInfo['Frames']=len(NewData)
    
    return FileInfo



def TimeChange(FileInfo, NewPitchRatio):
    
    
    
    '''
    #Window Segments are currently constant
    
    #They should be centered around pitch marks.
    
    '''

    Len=FileInfo['Frames']
    
    Windowsize=200
    HWindow = np.hanning(Windowsize)

    
    
    #WindowNum=Len/(Windowsize-2*WindowOverlap)
    

    NewData=[]
    Chan1Array=[]
    Chan2Array=[]
    
    FirstChannel=0
    SecondChannel=0    
    
    for i in FileInfo['IntData']:
        Chan1Array.append(i[0])
        Chan2Array.append(i[1])
    

    SectionArray1=[]
    SectionArray2=[]
    
    Overlap=round(Windowsize/2)

    FinalChan1Array=np.zeros(round(len(Chan1Array)*NewPitchRatio))
    FinalChan2Array=np.zeros(round(len(Chan2Array)*NewPitchRatio))
    
    
    '''
    This Code Works Now
    
    '''
    "H is the mainPackage Frequency Points"
    # Will be Window Size length except for the last run, as that will be less than the windowsize
    
    h=round(Overlap)
    for i in range(0,Len,h):
        UnitSize=len(Chan1Array[i:i+Windowsize])
        try:
            SectionArray1=Chan1Array[i:i+Windowsize]*HWindow[0:UnitSize]
            FinalChan1Array[round(i*NewPitchRatio):round(i*NewPitchRatio)+UnitSize]+=SectionArray1
            
            SectionArray2=Chan2Array[i:i+Windowsize]*HWindow[0:UnitSize]    
            FinalChan2Array[round(i*NewPitchRatio):round(i*NewPitchRatio)+UnitSize]+=SectionArray2
        except:
            RemainingLength=len(FinalChan1Array[round(i*NewPitchRatio):round(i*NewPitchRatio)+UnitSize])
            SectionArray1=Chan1Array[i:i+Windowsize]*HWindow[0:UnitSize]
            FinalChan1Array[round(i*NewPitchRatio):round(i*NewPitchRatio)+UnitSize]+=SectionArray1[RemainingLength]
            
            SectionArray2=Chan2Array[i:i+Windowsize]*HWindow[0:UnitSize]    
            FinalChan2Array[round(i*NewPitchRatio):round(i*NewPitchRatio)+UnitSize]+=SectionArray2[RemainingLength]
            break
        
    for i in range(0,len(FinalChan1Array)):
        FirstChannel=round(FinalChan1Array[i])
        SecondChannel=round(FinalChan2Array[i])
        ChangedVal=(FirstChannel,SecondChannel)
        NewData.append(ChangedVal)
    
    
    FileInfo['IntData']=NewData
    FileInfo['Frames']=len(NewData)
    
    return FileInfo    
 
    
def PitchShift(DataFile,pitch):
    
    time=1000.0/DataFile['FrameRate']
    Offset=math.floor(time*DataFile['FrameRate'])
    DataFile=PitchChange(DataFile,pitch)
    DataFile=TimeChange(DataFile, pitch)
    DataFile['IntData']=OffsetSound(DataFile,Offset)   
    
    return DataFile
     


'''
Pitch change
Extend sound
'''

def DarthVader(FileInfo):
    # Darth Vader Preset
    time=1000.0/FileInfo['FrameRate']
    Offset=math.floor(time*FileInfo['FrameRate'])
    pitch=0.8 # For Me
    FileInfo['IntData']=OffsetSound(FileInfo,Offset)
    FileInfo=PitchChange(FileInfo,pitch)
    

    
    FileInfo=TimeChange(FileInfo, pitch)
    
    return FileInfo