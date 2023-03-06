class Actor:
    """generic class for actors"""

    def __init__(self,m_name,m_consummedToken=1,m_producedToken=1,m_frequency=0,m_nextChannel=None,m_previousChannel=None,m_delay=0):
        """
            Initialization function
            m_name = actor's name
            m_consummedToken = number of tokens consummed by the actor
            m_producedToken = number of tokens produced when the actor is fired
            m_frequency = actor's firing frequency
            m_nextChannel = channel that precedes the actor
            m_previousChannel = channel that follows the actor
            m_delay : date from which the actor should start
        """
        self.name = m_name
        self.consummedToken = m_consummedToken
        self.producedToken = m_producedToken
        self.frequency = m_frequency
        self.nextChannel = m_nextChannel
        self.previousChannel = m_previousChannel
        self.numOfFirings = 0 #number of times the actor has been fired
        self.datesOfFirings = [] #firing dates of the actor
        self.numOfFiringsPerExecution = 0 #number of times the actor has been fired in a execution of a yhe graph. This variable is reset for each new execution of the graph
        self.delay = m_delay

    def produce(self):
        """
            method to produce tokens on the next channel(s)
        """
        if(self.nextChannel != None):
            try:
                for i in range(len(self.nextChannel)):
                    self.nextChannel[i].numOfCurrentTokens +=  self.producedToken[i]/self.nextChannel[i].divisor
                    self.nextChannel[i].numOfCurrentTokens = round(self.nextChannel[i].numOfCurrentTokens,4)
                    #print("current tokens on {} = {} (after {} firing)".format(self.nextChannel[i].name,self.nextChannel[i].numOfCurrentTokens,self.name))
            except:
                self.nextChannel.numOfCurrentTokens +=  self.producedToken/self.nextChannel.divisor
                self.nextChannel.numOfCurrentTokens = round(self.nextChannel.numOfCurrentTokens,4)
                #print("current tokens on {} = {} (after {} firing)".format(self.nextChannel.name,self.nextChannel.numOfCurrentTokens,self.name))
        
    def consume(self):
        """
            method to consume tokens from the previous channel
        """
        if(self.previousChannel != None):
            try:
                for i in range(len(self.previousChannel)):
                    self.previousChannel[i].numOfCurrentTokens -= self.consummedToken[i]/self.previousChannel[i].divisor
                    self.previousChannel[i].numOfCurrentTokens = round(self.previousChannel[i].numOfCurrentTokens,4)
                    #print("current tokens on {}={} (after {} firing)".format(self.previousChannel[i].name,self.previousChannel[i].numOfCurrentTokens,self.name))
                    
            except:
                self.previousChannel.numOfCurrentTokens -= self.consummedToken/self.previousChannel.divisor
                self.previousChannel.numOfCurrentTokens = round(self.previousChannel.numOfCurrentTokens,4)
                #print("current tokens on {}={} (after {} firing)".format(self.previousChannel.name,self.previousChannel.numOfCurrentTokens,self.name))

    def printStat(self):
        print("==============================================================================")
        print("{} has been activated {} times at the following dates : {}".format(self.name,self.numOfFirings,self.datesOfFirings))