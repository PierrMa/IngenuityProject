##########################################################################
#                               Libraries
##########################################################################
from actor import Actor
from channel import Channel
from LogicTimer import LogicTimer

##########################################################################
#                               Functions
##########################################################################


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

myTimer = LogicTimer(m_tic=5)
##########################################################################
#                               main program
##########################################################################  
for t in range(12):
    current_time = myTimer.get_current_time()
    print(current_time)
    for i in actors_list:
        if((i.frequency>0) and ((current_time/1000)%(1/i.frequency)==0)):
            myTimer.wait(current_time,i)
        elif (i.frequency==0):
            myTimer.wait(current_time,i)
    myTimer.do_task(current_time)
    myTimer.run()