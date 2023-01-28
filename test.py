##########################################################################
#                               Libraries
##########################################################################
from actor import Actor
from channel import Channel
import time
import threading

##########################################################################
#                               Global variables
##########################################################################
first_fire = True #True means the function has never been fired

##########################################################################
#                               Functions
##########################################################################
def fireActorWithoutIncomingChannels(actor):
    global first_fire 
    #if the actor has to respect a firing frequency and if it is not the first firing (because no need to check frequency in that case)
    if((actor.frequency>0) and (not first_fire)):
        t0 = time.time()
        time.sleep(round((1/actor.frequency),2)) #wait until it's time for the next firing
        t1 = time.time()
        delay = (t1 - t0)*1000
        print("automatic firing for actors without previous channel after {}ms".format(delay))
        actor.produce()
    else:#if the actor doesn't have to respect a firing frequency or if it's the first firing
        print("automatic firing for actors without previous channel")
        actor.produce()
        first_fire = False

def fireActorWithIncomingChannels(actor):
    global first_fire 
    #if the actor has to respect a firing frequency and if it is not the first firing (because no need to check frequency in that case)
    if((actor.nextActor.frequency>0) and (not first_fire)):
        t0 = time.time()
        time.sleep(round((1/actor.nextActor.frequency),2)) #wait until it's time for the next firing
        actor.checkTokens(t0)
    else:#if the actor doesn't have to respect a firing frequency
        t0 = time.time()
        actor.checkTokens(t0)
        first_fire = False


##########################################################################
#                               Variables
##########################################################################
actors_list = []
channel_list = []

#actors
a1 = Actor(m_name = 'A', m_consummedToken=0,m_producedToken=[3,2],m_frequency=0.5,m_nextChannel=None,m_previousChannel=None)
#print("A.consummedToken={}\nA.frequency={}\nA.nextChannel={}\nA.previousChannel={}\nA.producedToken={}\n".format(A.consummedToken,A.frequency,A.nextChannel,A.previousChannel,A.producedToken))
actors_list.append(a1)
a2 = Actor(m_name = 'B',m_consummedToken=4,m_producedToken=3,m_frequency=0,m_nextChannel=None,m_previousChannel=None)
actors_list.append(a2)
a3 = Actor(m_name = 'C',m_consummedToken=[2,1],m_producedToken=0,m_frequency=0,m_nextChannel=None,m_previousChannel=None)
actors_list.append(a3)

#channels
c1 = Channel(m_name = 'c1',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=2, m_previousActor=a1, m_nextActor=a3)
channel_list.append(c1)
c2 = Channel(m_name = 'c2',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=4, m_previousActor=a1, m_nextActor=a2)
channel_list.append(c2)
c3 = Channel(m_name = 'c3',m_divisor=1, m_numOfInitialTokens=0, m_requiredTokens=1, m_previousActor=a2, m_nextActor=a3)
#print("c3.divisor={}\nc3.numOfInitialTokens={}\nc3.requiredTokens={}\n".format(c3.divisor,c3.numOfInitialTokens,c3.requiredTokens))
channel_list.append(c3)

a1.nextChannel = [c1,c2]
a2.nextChannel = c3
a2.previousChannel = c2
a3.previousChannel=[c1,c3]
#print("A.consummedToken={}\nA.frequency={}\nA.nextChannel={}\nA.previousChannel={}\nA.producedToken={}\n".format(A.consummedToken,A.frequency,A.nextChannel,A.previousChannel,A.producedToken))

#th1 = threading.Thread(target=fireActorWithoutIncomingChannels)
#th2 = threading.Thread(target=fireActorWithIncomingChannels)
thread1 = {}
thread2 = {}
cpt1 = 0
cpt2 = 0
##########################################################################
#                               main program
##########################################################################   
for t in range(5):
    #each actor without previous channel is automatically fired
    for j in actors_list:
        if(not j.previousChannel):
            fireActorWithoutIncomingChannels(j)
            """thread1[cpt1] = threading.Thread(target=fireActorWithoutIncomingChannels(j))
            thread1[cpt1].start()
            cpt1+=1"""     
    #check if the number of required tokens is reach on each channel for actors with incoming channels
    for i in channel_list:
        fireActorWithIncomingChannels(i)
        """thread2[cpt2] = threading.Thread(target=fireActorWithIncomingChannels(i))
        thread2[cpt2].start()
        cpt2+=1 """
"""
for i in thread1:
    i.join()
for i in thread2:
    i.join()"""
