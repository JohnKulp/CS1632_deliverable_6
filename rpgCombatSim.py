

def printhi():
	print "hi"

#any character, including both players or monsters
class Character():
	def __init__(self, health, strength, name):
		self.health = health
		self.strength = strength
		self.name = name

	#function for the player to take damage
	def take_damage(self, damage):
		self.health -= damage

	#function to attack a target
	def attack(self, target):
		damage_dealt = self.strength

		target.take_damage(damage_dealt)
		return damage_dealt

#function to accept and process input for a player's turn
def player_turn(player, enemies):
	print_intro(player, enemies)
	command = accept_command()
	turn_is_over = False
	while not turn_is_over:
		#accept a command
		while not command:
			command = accept_command()

		#act according to the command

		#help command
		if command == "help":
			print_help()

		#attack command
		elif command == "attack":
			enemy = choose_enemy(enemies)
			if enemy is not -1:
				#attacking ends the turn
				damage = player.attack(enemies[enemy])
				print_damage(enemies[enemy], player, damage)
				turn_is_over = True
		command = None

#function for a player to select an enemy from a list
def choose_enemy(enemies):
	choice = None
	loop_condition = True
	while loop_condition:
		input_string = "\nType 'back' to go back\n"
		for i in range(len(enemies)):
			input_string += "Type " + str(i + 1) + " to target " + enemies[i].name + "\n"

		choice = raw_input(input_string).lower()
		try:
			choice = int(choice)
			loop_condition = choice < 1 or choice > len(enemies)
		except ValueError:
			loop_condition = choice != "back"

	if choice == "back":
		return -1
	else:
		return choice -1

#print functions. 
#  These are here to allow for stubbing in the test cases or allow for
#  alternate input methods

def print_intro(player, monsters):
	text = "You have " + str(player.health) + "health\n"
	text += "There are " + str(len(monsters)) + " enemies in front of you\n"
	for i in range(len(monsters)):
		text += monsters[i].name + ": " + str(monsters[i].health) + " health\n"
	text += "what will you do?\n"
	print text
def print_help():
	print """
		"attack" : attack the enemy\n
		"help" : get a list of commands
		"""
def print_damage(source, target, damage):
	print source.name + " was attacked by " + target.name + " for " + str(damage) + " damage.\n"
def print_death(character):
	print character.name + " died!"

#function to collect a command and determine if it is valid
def accept_command():
	command = raw_input("please enter a command.  Enter help for a list of commands\n").lower()

	accepted_commands = [
		"attack",
		"help"
	]

	if command in accepted_commands:
		return command
	else:
		return False

#function to automatically take the turn of each enemy
def enemy_turn(player, enemies):
	for enemy in enemies:
		damage = enemy.attack(player)
		print_damage(player, enemy, damage)


#function to check whether the player has won
def check_for_win(enemies):
	if len(enemies) is 0:
		return True
	return False

#function to check whether the player has lost
def check_for_loss(player):
	return player.health <= 0

#function to check the monsters for any deaths and remove the dead monsters
def check_for_deaths(monsters):
	for monster in monsters[:]:
		if monster.health <= 0:
			print_death(monster)
			monsters.remove(monster)




#main loop
if __name__ == "__main__":
	won = False
	lost = False

	#objects used for the scenario
	player = Character(health = 50, strength = 10, name = "player")
	monster = Character(health = 10, strength = 10, name = "monster1")
	monster2 = Character(health = 15, strength = 10, name = "monster2")
	monster3 = Character(health = 20, strength = 5, name = "monster3")
	enemies = [monster, monster2, monster3]

	#runtime loop
	while not won and not lost:
		player_turn(player, enemies)
		check_for_deaths(enemies)
		won = check_for_win(enemies)
		enemy_turn(player, enemies)
		lost = check_for_loss(player)

	if won:
		print "You win!  Yay!"
	elif lost:
		print "You died.  Do better next time!"
