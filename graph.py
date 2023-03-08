##########################################################################
#                               Libraries
##########################################################################
from actor import Actor
from channel import Channel
from LogicTimer import LogicTimer
import numpy as np
from sympy import *
##########################################################################
#                               Functions
##########################################################################
def processTopologicMatrix(actor_list,channel_list):
    """
        fonction du process the topologic matrix of a graph
        actor_list : the list of actors of the graph
        channel_list : the list of channels of the graph
    """
    matrix = np.zeros([len(channel_list),len(actor_list)])
    for i,channel in enumerate(channel_list):
        for j,actor in enumerate(actor_list):
            #explore previous channel(s)
            if(actor.previousChannel!=None):
                try:
                    for k in actor.previousChannel:
                        if(k==channel):
                            matrix[i,j]+=-k.requiredTokens
                except:
                    if(actor.previousChannel==channel):
                        matrix[i,j]+=-actor.consummedToken#/channel.divisor
            #explore next channel(s)
            if(actor.nextChannel!=None):
                try:
                    for k,next in enumerate(actor.nextChannel):
                        if(next==channel):
                            matrix[i,j]+=actor.producedToken[k]#/channel.divisor
                except:
                    if(actor.nextChannel==channel):
                        matrix[i,j]+=actor.producedToken#/channel.divisor
    return matrix

def processRepeatVector(matrix):
    """
        function to compute the repeat vector of a topologic matrix
        matrix : the topologic matrix of which we have to compute the repeat vector
    """
    myVector = Matrix(matrix).nullspace()
    myVector = np.array(myVector)
    myVector = np.ndarray.flatten(myVector)
    k = 0
    areAllIntegers = False
    while(areAllIntegers!=True):
        areAllIntegers = True
        k += 1
        for i in myVector:
            if (round(i*k,15)!=int(i*k)): #check if all the number of the repat vector are integers
                areAllIntegers = False
    for i in range(len(myVector)):
        myVector[i] = int(k*myVector[i])
    return myVector

def chekFiring(actors_list):
    """
        function to print the number of times and the date when the different actors have been fired
        actors_list : the list of actors to check
    """
    for i in actors_list:
        i.printStat()

def isExecutionCompleted(actors_list,repeatVector):
    """
        function to check if a execution of the graph has been completed
        actors_list : list of actors
        repeatVector : repeat vector of the graph
    """
    numOfFiringList = [] #list to get the current number of firing for each actor (in order)
    isCompleted = True #this flag is true if the repeat vector is equal to numOfFiringList

    #get the number of firing for each actor in a list
    for i in actors_list:
        numOfFiringList.append(i.numOfFiringsPerExecution)
    
    #check if the number of firing for each actor is equal to the number of firing requiered to complete an execution of the graph
    for index, numOfFiring in enumerate(numOfFiringList):
        if(repeatVector[index]!=numOfFiring):
            isCompleted = False
    return isCompleted

def checkConsistancy(actors_list,repeatVector,channel_list):
    """
        function to check the consistancy of the graph
        actors_list : list of actors
        repeatVector : repeat vector of the graph
        channel_list : list of channels
    """
    weAreBack = True

    isCompleted = isExecutionCompleted(actors_list,repeatVector)
    #if a complete execution of the graph has been done, check if we are back to initial state
    if(isCompleted):
        for i in channel_list:
            if(i.numOfInitialTokens!=i.numOfCurrentTokens):
                weAreBack = False
    
    if((isCompleted) and (not weAreBack)):
        print("Consistency not checked!")
        for i in channel_list:
            print("numOfCurrentTokens of {} = {}".format(i.name,i.numOfCurrentTokens))
    if(isCompleted and weAreBack):
        print("Consistency checked!")

def implementationWithFiringFrequencyDeterminedDuringRuntime(myTimer,actors_list):
    """
        function to fire actors regarding a frequency determined during runtime
        myTimer: logical timer
        actors_list: list of actors
    """
    IsEnough = True #flag False if at least one of the following channels of an actor has not enough tokens to allow the next actor to fire
    
    current_time = myTimer.get_current_time() #get the current value of the logical clock
    
    #print("============================ T = {}ms ============================= ".format(current_time))
    
    for i in actors_list:
        if((i.frequency>0) and ((current_time)%(1000/i.frequency)==0)):#check if it is time to fired timed actors
            if(i.delay>0 and (current_time>=i.delay)):
                myTimer.wait(current_time,i)
            elif(i.delay==0):
                myTimer.wait(current_time,i)
        elif (i.frequency==0):
            if(i.nextChannel != None):#if the actor has at least one following channel
                try: #for actors with more than one following channel
                    IsEnough = True
                    for j in i.nextChannel:#check if all following channels have enough tokens to fire the next actors
                        if(j.requiredTokens>j.numOfCurrentTokens):#if one channel has not reach yet the number of required tokens
                            IsEnough = False
                except:#if the actor has only one following channel
                    if(i.nextChannel.requiredTokens>i.nextChannel.numOfCurrentTokens):
                        IsEnough = False
            if(not IsEnough): #a not timed actor is fired only if at least one of its next channels has not yet reach the number of required tokens to fired the next actor
                myTimer.wait(current_time,i)
    myTimer.do_task(current_time)#fire the actors if it is possible
    myTimer.run()  #add one period to the logical clock

def implementationWithFiringFrequencyDeterminedAtCompilerTime(myTimer,actors_list,repeatVector):
    """
        function to fire actors regarding a frequency determined at compiler time for each actor
        myTimer: logical timer
        actors_list: list of actors
        repeatVector : repeat vector of the graph
    """
    current_time = myTimer.get_current_time() #get the current value of the logical clock
    current_time = round(current_time,6)
    #print("============================ T = {}ms ============================= ".format(current_time))
    
    for index,actor in enumerate(actors_list):
        if((actor.frequency>0) and (actor.numOfFiringsPerExecution<repeatVector[index])): #check if it is time to fired timed actors
            if(actor.delay>0 and (current_time>=actor.delay)):
                if((current_time-actor.delay)%(1000/actor.frequency)==0):
                    myTimer.wait(current_time,actor)
            elif(actor.delay==0 ):
                if((current_time)%(1000/actor.frequency)==0):
                    myTimer.wait(current_time,actor)
        elif (actor.frequency==0):
            if(actor.numOfFiringsPerExecution<repeatVector[index]): #check is the actor has already been fired enough to complete an execution of the graph
                myTimer.wait(current_time,actor)
            
    
    myTimer.do_task(current_time)#fire the actors if it is possible
    myTimer.run() #add one period to the logical clock

    checkConsistancy(actors_list,repeatVector,channel_list) #check consistency of the graph
    
    isCompleted = isExecutionCompleted(actors_list,repeatVector)#check if one execution of the graph has been completed    
    if(isCompleted): #reset numOfFiringsPerExecution for each actor if an execution of the graph has been completed
        for i in actors_list:
            i.numOfFiringsPerExecution = 0

def decimalToInteger(channels_list):
    """
        Function to allows the use of integer rather than decimal for tokens
        channels_list: channels list
        actors_list: actors list
    """
    divisor_list=[]
    for i in channels_list:
        divisor_list.append(i.divisor)
    print("divisor_list",divisor_list)
    ppcm = np.lcm.reduce(divisor_list)
    print("ppcm=",ppcm)

    multiplier_list = []

    for i in divisor_list:
        multiplier_list.append(ppcm/i)

    multiplier_list=np.array(multiplier_list)
    print(multiplier_list)
    for index,channel in enumerate(channels_list):
        channel.multiplier = multiplier_list[index]

def msToTic(actors_list,clock_period):
    for i in actors_list:
        if(i.frequency>0):
            i.nbTic = (1000/i.frequency)/clock_period
            i.delayInTic = i.delay/clock_period

def implementationWithFiringFrequencyDeterminedAtCompilerTimeInteger(myTimer,actors_list,repeatVector):
    """
        function to fire actors regarding a frequency determined at compiler time for each actor
        myTimer: logical timer
        actors_list: list of actors
        repeatVector : repeat vector of the graph
    """
    current_time = myTimer.get_current_time() #get the current value of the logical clock
    #print("============================ T = {}ms ============================= ".format(current_time))
    
    for index,actor in enumerate(actors_list):
        if((actor.frequency>0) and (actor.numOfFiringsPerExecution<repeatVector[index])): #check if it is time to fired timed actors
            if(actor.delayInTic>0 and (current_time>=actor.delayInTic)):
                if((current_time-actor.delayInTic)%(actor.nbTic)==0):
                    myTimer.wait(current_time,actor)
            elif(actor.delay==0 ):
                if((current_time)%(actor.nbTic)==0):
                    myTimer.wait(current_time,actor)
        elif (actor.frequency==0):
            if(actor.numOfFiringsPerExecution<repeatVector[index]): #check is the actor has already been fired enough to complete an execution of the graph
                myTimer.wait(current_time,actor)
            
    
    myTimer.do_task(current_time)#fire the actors if it is possible
    myTimer.run() #add one period to the logical clock

    checkConsistancy(actors_list,repeatVector,channel_list) #check consistency of the graph
    
    isCompleted = isExecutionCompleted(actors_list,repeatVector)#check if one execution of the graph has been completed    
    if(isCompleted): #reset numOfFiringsPerExecution for each actor if an execution of the graph has been completed
        for i in actors_list:
            i.numOfFiringsPerExecution = 0
        
##########################################################################
#                               Variables
##########################################################################
actors_list = []
channel_list = []

#definition des acteurs
camera=Actor(m_name='Camera', m_consummedToken=20, m_producedToken=[1,4], m_frequency=25, m_nextChannel=None, m_previousChannel=None)
actors_list.append(camera)

base_frame=Actor(m_name='base_frame',m_consummedToken=5,m_producedToken=1, m_frequency=0, m_nextChannel=None, m_previousChannel=None)
actors_list.append(base_frame)

search_frame=Actor(m_name='search_frame',m_consummedToken=5, m_producedToken=1, m_frequency=0,m_nextChannel=None, m_previousChannel=None)
actors_list.append(search_frame)

feature_detector_base_frame=Actor(m_name='feature_detector_base_frame',m_consummedToken=1, m_producedToken=1,m_frequency=0, m_nextChannel=None, m_previousChannel=None)
actors_list.append(feature_detector_base_frame)

feature_detector_search_frame=Actor(m_name='feature_detector_search_frame',m_consummedToken=1,m_producedToken=1,m_frequency=0,m_nextChannel=None,m_previousChannel=None)
actors_list.append(feature_detector_search_frame)

pseudo_landmarks=Actor(m_name='pseudo_landmarks',m_consummedToken=1,m_producedToken=4,m_frequency=0,m_nextChannel=None, m_previousChannel=None)
actors_list.append(pseudo_landmarks)

match_feature_landmarks=Actor(m_name='match_feature_landmarks', m_consummedToken=[1,1],m_producedToken=100,m_frequency=0,m_nextChannel=None,m_previousChannel=None)
actors_list.append(match_feature_landmarks)

extended_kalman_filter=Actor(m_name='extended_kalman_filter', m_consummedToken=[4,32,1], m_producedToken=1, m_frequency=500, m_nextChannel=None, m_previousChannel=None,m_delay=7.8)
actors_list.append(extended_kalman_filter)

imu_1=Actor(m_name='IMU_1', m_consummedToken=5, m_producedToken=[5,5], m_frequency=3200, m_nextChannel=None,m_previousChannel=None,m_delay=5.8)
actors_list.append(imu_1)

mode_commander=Actor(m_name='mode_commander', m_consummedToken=1, m_producedToken=[1,32,1], m_frequency=0, m_nextChannel=None, m_previousChannel=None)
actors_list.append(mode_commander)

LRF=Actor(m_name='LRF', m_consummedToken=10, m_producedToken=[10,10], m_frequency=50, m_nextChannel=None, m_previousChannel=None)
actors_list.append(LRF)

state_propagation=Actor(m_name='state_propagation', m_consummedToken=[1,32,1], m_producedToken=1, m_frequency=500,m_nextChannel=None,m_previousChannel=None,m_delay=8.8)
actors_list.append(state_propagation)


#channel
c1 = Channel(m_name = 'c1',m_divisor=5, m_numOfInitialTokens=4, m_requiredTokens=5, m_previousActor=camera, m_nextActor=base_frame)
channel_list.append(c1)

c2 = Channel(m_name = 'c2',m_divisor=5, m_numOfInitialTokens=0, m_requiredTokens=5, m_previousActor=camera, m_nextActor=search_frame)
channel_list.append(c2)

c3 = Channel(m_name = 'c3',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=1, m_previousActor=base_frame, m_nextActor=feature_detector_base_frame)
channel_list.append(c3)

c4 = Channel(m_name = 'c4',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=1, m_previousActor=search_frame, m_nextActor=feature_detector_search_frame)
channel_list.append(c4)

c5 = Channel(m_name = 'c5',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=1, m_previousActor=feature_detector_base_frame, m_nextActor=pseudo_landmarks)
channel_list.append(c5)

c6= Channel(m_name = 'c6',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=1, m_previousActor=feature_detector_search_frame, m_nextActor=match_feature_landmarks)
channel_list.append(c6)

c7 = Channel(m_name = 'c7',m_divisor=4, m_numOfInitialTokens=0, m_requiredTokens=1, m_previousActor=pseudo_landmarks, m_nextActor=match_feature_landmarks)
channel_list.append(c7)

c8 = Channel(m_name = 'c8',m_divisor=100, m_numOfInitialTokens=136, m_requiredTokens=4, m_previousActor=match_feature_landmarks, m_nextActor=extended_kalman_filter)
channel_list.append(c8)

c9 = Channel(m_name = 'c9',m_divisor=32, m_numOfInitialTokens=104, m_requiredTokens=32, m_previousActor=imu_1, m_nextActor=extended_kalman_filter)
channel_list.append(c9)

c10 = Channel(m_name = 'c10',m_divisor=1, m_numOfInitialTokens=3, m_requiredTokens=1, m_previousActor=extended_kalman_filter, m_nextActor=state_propagation)
channel_list.append(c10)

c11 = Channel(m_name = 'c11',m_divisor=10, m_numOfInitialTokens=7, m_requiredTokens=1, m_previousActor=LRF, m_nextActor=extended_kalman_filter)
channel_list.append(c11)

c12 = Channel(m_name = 'c12',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=1, m_previousActor=state_propagation, m_nextActor=mode_commander)
channel_list.append(c12)

c13 = Channel(m_name = 'c13',m_divisor=20, m_numOfInitialTokens=40, m_requiredTokens=20, m_previousActor=mode_commander, m_nextActor=camera)
channel_list.append(c13)

c14 = Channel(m_name = 'c14',m_divisor=5, m_numOfInitialTokens=80, m_requiredTokens=5, m_previousActor=mode_commander, m_nextActor=imu_1)
channel_list.append(c14)

c15 = Channel(m_name = 'c15',m_divisor=32, m_numOfInitialTokens=89, m_requiredTokens=32, m_previousActor=imu_1, m_nextActor=state_propagation)
channel_list.append(c15)

c16 = Channel(m_name = 'c16',m_divisor=10, m_numOfInitialTokens=23, m_requiredTokens=10, m_previousActor=mode_commander, m_nextActor=LRF)
channel_list.append(c16)

c17 = Channel(m_name = 'c17',m_divisor=10, m_numOfInitialTokens=7, m_requiredTokens=1, m_previousActor=LRF, m_nextActor=state_propagation)
channel_list.append(c17)

camera.nextChannel=[c1,c2]
camera.previousChannel=c13

base_frame.nextChannel=c3
base_frame.previousChannel=c1

search_frame.nextChannel=c4
search_frame.previousChannel=c2

feature_detector_base_frame.nextChannel=c5
feature_detector_base_frame.previousChannel=c3

feature_detector_search_frame.nextChannel=c6
feature_detector_search_frame.previousChannel=c4

pseudo_landmarks.nextChannel=c7
pseudo_landmarks.previousChannel=c5

match_feature_landmarks.nextChannel=c8
match_feature_landmarks.previousChannel=[c6,c7]

extended_kalman_filter.nextChannel=c10
extended_kalman_filter.previousChannel=[c8,c9,c11]

imu_1.nextChannel=[c9,c15]
imu_1.previousChannel=c14

mode_commander.nextChannel=[c13,c14,c16]
mode_commander.previousChannel=c12

LRF.nextChannel=[c11,c17]
LRF.previousChannel=c16

state_propagation.nextChannel=c12
state_propagation.previousChannel=[c10,c15,c17]

myTimer = LogicTimer(m_tic=0.0125, m_t0 = 0)
##########################################################################
#                               main program
########################################################################## 

decimalToInteger(channel_list)

topologicMatrix = processTopologicMatrix(actors_list,channel_list)
print("matrice topologique : \n",topologicMatrix)
repeatVector = processRepeatVector(topologicMatrix)
print("vecteur de répétition :",repeatVector)

for i in channel_list:
    i.reduceToTheSameDevisor()

msToTic(actors_list,myTimer.tic)

IsEnough = True #flag False if at least one of the following channels of an actor has not enough tokens to allow the next actor to fire
for t in range(2000000):
    #allow an implementation where firing frequency of not timed actors is determined at compiler time and use period in nb tics
    implementationWithFiringFrequencyDeterminedAtCompilerTimeInteger(myTimer,actors_list,repeatVector)

#chekFiring(actors_list)#debug function
    
