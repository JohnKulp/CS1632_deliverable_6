import unittest

from rpgCombatSim import *
import rpgCombatSim

#test interaction functions for the Character class
class testCharacterInteraction(unittest.TestCase):

	#test Character take damage function
	def test_take_damage(self):
		player = Character(health = 50, strength = 10, name = "player")
		player.take_damage(23)
		self.assertEqual(player.health, 27)


	#test Character attack function removes target's health
	def test_attack_deals_damage(self):
		player = Character(health = 50, strength = 10, name = "player")
		monster = Character(health = 15, strength = 5, name = "monster 1")
		player.attack(monster)
		self.assertEqual(monster.health, 5)

	#test Character attack function returns damage dealt
	def test_attack_returns_damage_dealth(self):
		player = Character(health = 50, strength = 10, name = "player")
		monster = Character(health = 15, strength = 5, name = "monster 1")
		damage_amount = player.attack(monster)
		self.assertEqual(damage_amount, 10)



#test functions for the player's turn
class testPlayerTurn(unittest.TestCase):

	#ensure that only the correct input options are allowed
	def test_accept_command_accepts_correct_input(self):
		#accept the base case 'attack'
		rpgCombatSim.raw_input = lambda _: "attack"
		res = accept_command()
		self.assertEqual(res, "attack", "accept_command fails base case of 'attack'")

		#accept the base case 'help'
		rpgCombatSim.raw_input = lambda _: "help"
		res = accept_command()
		self.assertEqual(res, "help", "accept_command fails base case of 'help'")

		#accept a capital value
		rpgCombatSim.raw_input = lambda _: "Attack"
		res = accept_command()
		self.assertEqual(res, "attack", "accept_command fails base case of 'Attack'")

	#ensure that incorrect input options are not allowed
	def test_accept_command_fails_to_accept_invalid_input(self):
		#don't allow an empty string
		rpgCombatSim.raw_input = lambda _: ""
		res = accept_command()
		self.assertFalse(res, "accept_command accepts empty string")

		#don't allow an incorrect string
		rpgCombatSim.raw_input = lambda _: "don't"
		res = accept_command()
		self.assertFalse(res, "accept_command accepts an invalid command")

		#don't allow a string containing a correct string
		rpgCombatSim.raw_input = lambda _: "**attack**"
		res = accept_command()
		self.assertFalse(res, "accept_command accepts a string containing a valid command")

	#test the base case of attacking the position 0 monster
	def test_navigate_player_turn_menu_attack_0(self):
		#set up stubs
		rpgCombatSim.accept_command = lambda: "attack"
		rpgCombatSim.choose_enemy = lambda _: 0
		rpgCombatSim.print_intro = lambda a, b: None
		rpgCombatSim.print_damage = lambda a, b, c: ""

		player = Character(health = 50, strength = 15, name = "player")
		monster = Character(health = 20, strength = 5, name = "monster 1")

		player_turn(player, [monster])

		self.assertEqual(monster.health, 5, "the commands 'attack' and '0' result in an attack lowering the monster's health")

	#test the 'back' commands by using a more complicated command list
	def test_navigate_player_turn_menu_help_attack_n1_attack_0(self):
		command =0
		#stubs the two functions with a counter to smartly change the command based on how many times it has been called
		class stubWithCount():
			def __init__(self):
				self.command = 0
				self.target = 0
			def stub_command(self):
				if self.command is 0:
					self.command += 1
					return "help"
				else:
					return "attack"
			target =0
			def stub_target(self, enemy):
				if self.target == 0:
					self.target += 1
					return -1
				else:
					return 0
		stub = stubWithCount()
		rpgCombatSim.accept_command = stub.stub_command
		rpgCombatSim.choose_enemy = stub.stub_target
		rpgCombatSim.print_help = lambda : None
		rpgCombatSim.print_intro = lambda a, b: None
		rpgCombatSim.print_damage = lambda a, b, c: ""

		player = Character(health = 50, strength = 15, name = "player")
		monster = Character(health = 20, strength = 5, name = "monster 1")

		player_turn(player, [monster])

		self.assertEqual(monster.health, 5, "the commands sequence 'help attack n1 attack 0' results in an attack lowering the monster's health")


	#test that choose enemy correctly handles good input
	def test_choose_enemy_works_with_correct_input(self):
		#test that the base cases work
		rpgCombatSim.raw_input = lambda _: "1"
		rpgCombatSim.print_damage = lambda a, b, c: ""
		monster = Character(health = 10, strength = 20, name = "monster 1")
		monster2 = Character(health = 20, strength = 10, name = "monster 2")
		monster3 = Character(health = 15, strength = 15, name = "monster 3")
		res = choose_enemy([monster, monster2, monster3])
		self.assertEqual(res, 0)

		rpgCombatSim.raw_input = lambda _: "2"
		res = choose_enemy([monster, monster2, monster3])
		self.assertEqual(res, 1)

		rpgCombatSim.raw_input = lambda _: "3"
		res = choose_enemy([monster, monster2, monster3])
		self.assertEqual(res, 2)

		#return case
		rpgCombatSim.raw_input = lambda _: "back"
		res = choose_enemy([monster, monster2, monster3])
		self.assertEqual(res, -1)

	#test that choose enemy correctly handles bad input
	def test_choose_enemy_fails_with_wrong_input(self):

		#stubs the raw input function
		class stubWithCount():
			def __init__(self):
				self.count = 0
				self.initial_value = "13"
			def stub_raw_input(self, dud):
				if self.count is 0:
					self.count += 1
					return self.initial_value
				else:
					return "1"
			def reset(self, value):
				self.count = 0
				self.initial_value = value

		stub = stubWithCount()

		#test that out of bounds numbers don't work
		rpgCombatSim.raw_input = stub.stub_raw_input
		monster = Character(health = 10, strength = 20, name = "monster 1")
		monster2 = Character(health = 20, strength = 10, name = "monster 2")
		monster3 = Character(health = 15, strength = 15, name = "monster 3")
		choose_enemy([monster, monster2, monster3])
		self.assertEqual(stub.count, 1)

		#test that blank input doesn't work
		stub.reset("")
		res = choose_enemy([monster, monster2, monster3])
		self.assertEqual(stub.count, 1)

		#test that negative values don't work
		stub.reset("-1")
		res = choose_enemy([monster, monster2, monster3])
		self.assertEqual(stub.count, 1)

#test the conditions for win, loss, and monster deaths
class testDeathConditions(unittest.TestCase):
	#test the check_for_win function
	def test_check_for_win(self):
		self.assertTrue(check_for_win([]))
		self.assertFalse(check_for_win(["something"]))
	#test the check_for_loss function
	def test_check_for_loss(self):
		player = Character(health = 0, strength = 5, name = "player")
		self.assertTrue(check_for_loss(player))
		player = Character(health = -1, strength = 5, name = "player")
		self.assertTrue(check_for_loss(player))
		player = Character(health = 1, strength = 5, name = "player")
		self.assertFalse(check_for_loss(player))
	#test the check_for_deaths function
	def test_check_for_deaths(self):
		rpgCombatSim.print_death = lambda _: ""
		monster = Character(health = 0, strength = 5, name = "monster1")
		monster2 = Character(health = -1, strength = 5, name = "monster2")
		monster3 = Character(health = 1, strength = 5, name = "monster3")
		monster4 = Character(health = 5, strength = 5, name = "monster4")

		list1 = [monster, monster2, monster3, monster4]
		list2 = [monster3, monster4]

		check_for_deaths(list1)

		self.assertEqual(list1, list2)


#test functions for the AI's turn
class testEnemyTurn(unittest.TestCase):
	def test_enemy_attack(self):
		rpgCombatSim.print_damage = lambda a, b, c: ""

		monster = Character(health = 10, strength = 10, name = "monster1")
		monster2 = Character(health = 15, strength = 10, name = "monster2")
		monster3 = Character(health = 20, strength = 5, name = "monster3")
		player = Character(health = 50, strength = 10, name = "player")

		enemy_turn(player, [monster, monster2, monster3])

		self.assertEqual(player.health, 25)


if __name__ == '__main__':
	unittest.main()