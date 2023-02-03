import time

class Channel:
    """generic class for channels"""
    def __init__(self,m_name,m_requiredTokens,m_previousActor,m_nextActor,m_numOfInitialTokens=0,m_divisor=1):
        """
            Initialization function
            m_name : name of the channel
            m_divisor : attribute channel receiving a rationnal number of tokens from its previous actor
            m_numOfInitialTokens : number of initial tokens on the channel
            m_requiredTokens : number of tokens requiered to fire the actor following the channel
            m_previousActor : actor which produces tokens on the channel
            m_nextActor : actor which consumes tokens from the channel
        """
        if(m_divisor==0):
            print("ZeroDivisionError")
            exit
        else:
            self.divisor = m_divisor
        self.name = m_name
        self.numOfInitialTokens = m_numOfInitialTokens
        self.requiredTokens = m_requiredTokens
        self.previousActor = m_previousActor
        self.nextActor = m_nextActor
        self.numOfCurrentTokens = m_numOfInitialTokens

    def fireNext(self,t0):
        """
            method to fire the actor following the channel
        """
        t1=time.time()
        delay = (t1-t0)*1000
        print("{} is firing after {}ms".format(self.name,delay))
        self.nextActor.produce()
        self.nextActor.consume()
    
    def checkTokens(self,t0):
        """
            method to check if the number of required tokens is reached for each the previous channel
        """
        isEnough = True #This flag become False if at list one channel reveiced by the actor to fire has not enough tokens to fire the actor
        try:#case where an actor receive multiple channels
            for i in self.nextActor.previousChannel:#on récupère le nombre de jetons requis pour l'activation
                if(i.numOfCurrentTokens < i.requiredTokens):
                    isEnough = isEnough and False
            if(isEnough):
                for i in self.nextActor.previousChannel:
                    if(i.numOfCurrentTokens >= i.requiredTokens):
                        i.fireNext(t0)
                    else:
                        print("Not enough tokens on {}".format(i.name))
        except:
            if(self.numOfCurrentTokens >= self.requiredTokens):
                self.fireNext(t0) #the actor following the channel is fired
            else:
                print("Not enough tokens on {}".format(self.name))

