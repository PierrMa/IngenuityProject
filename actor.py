import time

class Actor:
    """generic class for actors"""

    t0 = time.time()

    def __init__(self,m_name,m_consummedToken=1,m_producedToken=1,m_frequency=0,m_nextChannel=None,m_previousChannel=None):
        """
            Initialization function
            m_name = actor's name
            m_consummedToken = number of tokens consummed by the actor
            m_producedToken = number of tokens produced when the actor is fired
            m_frequency = actor's firing frequency
            m_nextChannel = channel that precedes the actor
            m_previousChannel = channel that follows the actor
        """
        self.name = m_name
        self.consummedToken = m_consummedToken
        self.producedToken = m_producedToken
        self.frequency = m_frequency
        self.nextChannel = m_nextChannel
        self.previousChannel = m_previousChannel

    def produce(self,t0=t0):
        """
            method to produce tokens on the next channel(s)
        """
        if(self.nextChannel != None):
            try:
                for i in range(len(self.nextChannel)):
                    self.nextChannel[i].numOfCurrentTokens +=  self.producedToken[i]
                    t1 = time.time()
                    delay = (t1-t0)*100
                    print("current tokens on {} = {} (fired by {})".format(self.nextChannel[i].name,self.nextChannel[i].numOfCurrentTokens,self.name))
                    print("delay for {} to produce = {}ms".format(self.name,delay))
                    t0 = t1
            except:
                self.nextChannel.numOfCurrentTokens +=  self.producedToken
                t1 = time.time()
                delay = (t1-t0)*100
                print("current tokens on {} = {} (fired by {})".format(self.nextChannel.name,self.nextChannel.numOfCurrentTokens,self.name))
                print("delay for {} to produce = {}ms".format(self.name,delay))
                t0 = t1

    def consume(self,t0=t0):
        """
            method to consume tokens from the previous channel
        """
        if(self.previousChannel != None):
            try:
                for i in range(len(self.previousChannel)):
                    self.previousChannel[i].numOfCurrentTokens -= self.consummedToken[i]
                    t1 = time.time()
                    delay = (t1-t0)*100
                    print("current tokens on {}={} (fired by {})".format(self.previousChannel[i].name,self.previousChannel[i].numOfCurrentTokens,self.name))
                    print("delay for {} to consume = {}ms".format(self.name,delay))
                    t0 = t1
            except:
                self.previousChannel.numOfCurrentTokens -= self.consummedToken
                t1 = time.time()
                delay = (t1-t0)*100
                print("current tokens on {}={} (fired by {})".format(self.previousChannel.name,self.previousChannel.numOfCurrentTokens,self.name))
                print("delay for {} to consume = {}ms".format(self.name,delay))
                t0 = t1