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
async def fire(jetonIn,jetonOut,requiered_token,delay):
	#verifying if we have requiered conditions to fire the actor
	if(jetonIn == requiered_token):
		jetonIn -= jetonIn
		jetonOut['base_frame'] += 1/10
		jetonOut['search_frame'] += 9/10
		print(str(datetime.now()))
	#starting the count down of the actor's period
	await asyncio.sleep(delay)

async def main():
	#variables
	frequence = 30 #fire frequency of the actor (Hz)
	entree = "mode_commander"
	sortie = ["base_frame","search_frame"]
	jetonIn = 0
	jetonOut = 0
	requiered_token = 1
	delay = round(1/frequence)

	while(1):
		task1 = asyncio.create_task(fire(jetonIn,jetonOut,requiered_token,delay))


asyncio.run(main())