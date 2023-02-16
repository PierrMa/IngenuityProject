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
                        matrix[i,j]+=-actor.consummedToken
            #explore next channel(s)
            if(actor.nextChannel!=None):
                try:
                    for k,next in enumerate(actor.nextChannel):
                        if(next==channel):
                            matrix[i,j]+=actor.producedToken[k]
                except:
                    if(actor.nextChannel==channel):
                        matrix[i,j]+=actor.producedToken
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
    areAllIntergers = False
    while(areAllIntergers!=True):
        areAllIntergers = True
        k += 1
        for i in myVector:
            if ((i*k)!=int(i*k)): #check if all the number of the repat vector are integers
                areAllIntergers = areAllIntergers and False  
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
    isTheSame = True #this flag is true if the repeat vector is equal to numOfFiringList

    #get the number of firing for each actor in a list
    for i in actors_list:
        numOfFiringList.append(i.numOfFiringsPerExecution)
    
    #check if the number of firing for each actor is equal to the number of firing requiered to complete an execution of the graph
    for index, numOfFiring in enumerate(numOfFiringList):
        if(repeatVector[index]!=numOfFiring):
            isTheSame = isTheSame and False
    return isTheSame

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
                weAreBack = weAreBack and False
    
    if((isCompleted) and (not weAreBack)):
        print("Consistency not checked!")
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
            myTimer.wait(current_time,i)
        elif (i.frequency==0):
            if(i.nextChannel != None):#if the actor has at least one following channel
                try: #for actors with more than one following channel
                    IsEnough = True
                    for j in i.nextChannel:#check if all following channels have enough tokens to fire the next actors
                        if(j.requiredTokens>j.numOfCurrentTokens):#if one channel has not reach yet the number of required tokens
                            IsEnough = IsEnough and False
                except:#if the actor has only one following channel
                    if(i.nextChannel.requiredTokens>i.nextChannel.numOfCurrentTokens):
                        IsEnough = IsEnough and False
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
    
    #print("============================ T = {}ms ============================= ".format(current_time))
    
    for index,actor in enumerate(actors_list):
        if((actor.frequency>0) and ((current_time)%(1000/actor.frequency)==0)): #check if it is time to fired timed actors
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

#actors
a1 = Actor(m_name = 'A', m_consummedToken=0,m_producedToken=[3,2],m_frequency=0,m_nextChannel=None,m_previousChannel=None)
#print("A.consummedToken={}\nA.frequency={}\nA.nextChannel={}\nA.previousChannel={}\nA.producedToken={}\n".format(A.consummedToken,A.frequency,A.nextChannel,A.previousChannel,A.producedToken))
actors_list.append(a1)
a2 = Actor(m_name = 'B',m_consummedToken=4,m_producedToken=3,m_frequency=0,m_nextChannel=None,m_previousChannel=None)
actors_list.append(a2)
a3 = Actor(m_name = 'C',m_consummedToken=[2,1],m_producedToken=1,m_frequency=20,m_nextChannel=None,m_previousChannel=None)
actors_list.append(a3)
a4 = Actor(m_name = 'D',m_consummedToken=[2,1],m_producedToken=[1,1],m_frequency=0,m_nextChannel=None,m_previousChannel=None)
actors_list.append(a4)
a5 = Actor(m_name = 'E',m_consummedToken=1,m_producedToken=0,m_frequency=10,m_nextChannel=None,m_previousChannel=None)
actors_list.append(a5)

#channels
c1 = Channel(m_name = 'c1',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=2, m_previousActor=a1, m_nextActor=a3)
channel_list.append(c1)
c2 = Channel(m_name = 'c2',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=4, m_previousActor=a1, m_nextActor=a2)
channel_list.append(c2)
c3 = Channel(m_name = 'c3',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=1, m_previousActor=a2, m_nextActor=a3)
#print("c3.divisor={}\nc3.numOfInitialTokens={}\nc3.requiredTokens={}\n".format(c3.divisor,c3.numOfInitialTokens,c3.requiredTokens))
channel_list.append(c3)
c4 = Channel(m_name = 'c4',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=2, m_previousActor=a3, m_nextActor=a4)
channel_list.append(c4)
c5 = Channel(m_name = 'c5',m_divisor=1, m_numOfInitialTokens=1, m_requiredTokens=1, m_previousActor=a4, m_nextActor=a4)
channel_list.append(c5)
c6 = Channel(m_name = 'c6',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=1, m_previousActor=a4, m_nextActor=a5)
channel_list.append(c6)

a1.nextChannel = [c1,c2]
a2.nextChannel = c3
a2.previousChannel = c2
a3.previousChannel=[c1,c3]
a3.nextChannel=c4
a4.previousChannel=[c4,c5]
a4.nextChannel=[c6,c5]
a5.previousChannel=c6
#print("A.consummedToken={}\nA.frequency={}\nA.nextChannel={}\nA.previousChannel={}\nA.producedToken={}\n".format(A.consummedToken,A.frequency,A.nextChannel,A.previousChannel,A.producedToken))

myTimer = LogicTimer(m_tic=5, m_t0 = 0)
##########################################################################
#                               main program
##########################################################################  
topologicMatrix = processTopologicMatrix(actors_list,channel_list)
#print("matrix = ",matrix)
#matrix_mini = np.delete(matrix,4,0)
#print("matrix simplifiée= ",matrix_mini)
#solutions=[(x1,x2,x3,x4,x5) for x1 in range(1,20) for x2 in range(1,20) for x3 in range(1,20) for x4 in range(1,20) for x5 in range(1,20) if 3*x1-2*x3==0 and 2*x1-4*x2==0 and 3*x2-x3==0 and x3-2*x4==0 and x4-x5==0]
#print(solutions)
repeatVector = processRepeatVector(topologicMatrix)
print(repeatVector)


IsEnough = True #flag False if at least one of the following channels of an actor has not enough tokens to allow the next actor to fire
for t in range(241):
    #Uncomment the function below to allow an implementation where firing frequency of not timed actor is determined during runtime
    #implementationWithFiringFrequencyDeterminedDuringRuntime(myTimer,actors_list)
    
    #Uncomment the function below to allow an implementation where firing frequency of not timed actor is determined at compiler time
    implementationWithFiringFrequencyDeterminedAtCompilerTime(myTimer,actors_list,repeatVector)
    

chekFiring(actors_list)#debug function