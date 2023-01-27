from actor import Actor
from channel import Channel

actors_list = []
channel_list = []

#actors
a1 = Actor(m_name = 'A', m_consummedToken=0,m_producedToken=[3,2],m_frequency=0,m_nextChannel=None,m_previousChannel=None)
#print("A.consummedToken={}\nA.frequency={}\nA.nextChannel={}\nA.previousChannel={}\nA.producedToken={}\n".format(A.consummedToken,A.frequency,A.nextChannel,A.previousChannel,A.producedToken))
actors_list.append(a1)
a2 = Actor(m_name = 'B',m_consummedToken=4,m_producedToken=3,m_frequency=0,m_nextChannel=None,m_previousChannel=None)
actors_list.append(a2)
a3 = Actor(m_name = 'C',m_consummedToken=[2,1],m_producedToken=0,m_frequency=20,m_nextChannel=None,m_previousChannel=None)
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

for t in range(5):
    #each actor without previous channel is automatically fired
    for j in actors_list:
        if(not j.previousChannel):
            print("automatic firing for actors without previous channel")
            j.produce()
    #check if the number of required tokens is reach on each channel
    for i in channel_list:
        i.checkAvailability()
    
