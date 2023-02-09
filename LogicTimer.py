import numpy as np

class LogicTimer:
    """ class to implement a logic timer """

    def __init__(self,m_tic, m_t0=0):
        """
            m_tic : time spent for each of the timer's tic
            m_t0 : initial value of the logic timer
        """
        self.tic = m_tic
        self.__current_time = m_t0  #number of tics spent until now
        self.list_of_task = [] #list of tasks to execute

    def run(self):
        """
            method to increment the timer of one tic
        """
        self.__current_time+=self.tic
    
    def do_task(self,milestone):
        """
            method to execute the list of tasks
            milestone : limit time to execute the tasks
        """
        #chek if the list is empty
        if(len(self.list_of_task)==0):
            return

        task = np.array(self.list_of_task)
        i=0

        while(task[len(task)-1-i][0]<=milestone):
            actor = task[len(task)-1-i][1]
            if(actor.previousChannel==None): #for actors without incoming channels
                print("Activation de {} à {}ms".format(actor.name,self.__current_time))
                actor.produce()
            else:
                try: #try to see if there are more than one previous channel
                    size = len(actor.previousChannel) #this throw an error if there is only one previous channel
                    actor.previousChannel[0].checkTokens(self.__current_time)
                except:
                    actor.previousChannel.checkTokens(self.__current_time)
            try:
                self.list_of_task.pop() 
                i+=1
            except:
                break #if the list is empty, get out of the loop

    def get_current_time(self):
        """
            method to return the current value of the logic timer
        """
        return self.__current_time
    
    def wait(self,time_of_execution,actor):
        """
            method to add an actor with its time of execution to a ordered list
            time_of_execution : when to execute the actor
            actor : actor to add to the list
        """
        self.list_of_task.append([time_of_execution,actor])
        print("passage dans wait, time of exexution = {} pour l'acteur {}".format(time_of_execution,actor.name))