"""v1
#bibliothèques
from datetime import datetime

#fonctions	
def fire(jetonIn,jetonOut):
	t0 = datetime.now().microsecond
	jetonIn -= jetonIn
	jetonOut['base_frame'] += 1/10
	jetonOut['search_frame'] += 9/10
	return t0


#variable
frequence = 30 #fréquence d'activation de l'acteur en Hz
entree = "mode_commander"
sortie = ["base_frame","search_frame"]
jetonIn = 0
jetonOut = 0
requiered_token = 1
delta = 0
t0 = 0
first_fire = True

while(1):
	#vérifier si nombre de jetons en entrée suffisant
	if(jetonIn == requiered_token):
		if(first_fire):
			fire(jetonIn,jetonOut)
			first_fire = False
		else:
			#récupération du temps écoulé (en ms) depuis la dernière activation de l'acteur
			t1 = datetime.now().microsecond
			delta = t0-t1

			#si la durée écoulé depuis la dernière activation >33ms
			if(delta>(1/frequence)):
				t0 = fire(jetonIn,jetonOut)
"""

#v2
#Libraries
import asyncio
from datetime import datetime

#functions
async def fire(jetonIn,jetonOut,requiered_token,delay,flag):
	#starting the count down of the actor's period
	if(not flag):
		await asyncio.sleep(delay)#
		#verifying if we have requiered conditions to fire the actor
		if(jetonIn == requiered_token):
			jetonIn -= jetonIn
			jetonOut['base_frame'] += 1/10
			jetonOut['search_frame'] += 9/10
			#print(str(datetime.now().second))
	else:
		flag = False
		#print('première fois')
		#verifying if we have requiered conditions to fire the actor
		if(jetonIn == requiered_token):
			jetonIn -= jetonIn
			jetonOut['base_frame'] += 1/10
			jetonOut['search_frame'] += 9/10
			#print(str(datetime.now().second))
	return flag

async def main():
	#variables
	frequence = 30 #fire frequency of the actor (Hz)
	entree = "mode_commander"
	sortie = ["base_frame","search_frame"]
	jetonIn = 1
	jetonOut = {}
	requiered_token = 1
	delay = round(1/frequence)
	first_fire = True #True means the function has never been fired

	for i in range(len(sortie)):
		jetonOut[sortie[i]] = 0

	while(1):
		task1 = asyncio.create_task(fire(jetonIn,jetonOut,requiered_token,delay,first_fire))
		first_fire = await task1

asyncio.run(main())