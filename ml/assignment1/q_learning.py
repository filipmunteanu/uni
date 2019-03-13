# Filip Munteanu 342C4

# General imports
from copy import copy
#from random import choice, random
from argparse import ArgumentParser
from time import sleep
import numpy as np

# Game functions
from pong import get_initial_state

def random(Q, state, legal_actions, epsilon):
	return np.random.choice(legal_actions)

def greedy(Q, state, legal_actions, epsilon):
	return best_action(Q, state, legal_actions)

def perfect(Q, state, legal_actions, epsilon):
	if np.random.sample(epsilon):
		return np.random.choice(legal_actions)
	else:
		act = "STAY"
		if state[0] > state[3]:
			act = "UP"
		elif state[0] < state[3]:
			act = "DOWN"

		if act not in legal_actions:
			act = "STAY"

		#print "adv: " + str(legal_actions) + "  " + act + "  " + str(state)
		return act

def epsilon_greedy(Q, state, legal_actions, epsilon):
	l = filter(lambda x: (state, x) not in Q, legal_actions)
	if l != []:
		return np.random.choice(l)

	if np.random.sample(epsilon):
		return np.random.choice(legal_actions)
	else:
		return best_action(Q, state, legal_actions)

def best_action(Q, state, legal_actions): # greedy
	l = filter(lambda x: (state, x) in Q, legal_actions)
	if l == []:
		return np.random.choice(legal_actions)

	maxQ = max(map(lambda x: Q[(state, x)], l))
	best_actions = filter(lambda x: Q[(state, x)] == maxQ, l)
	#return best_actions[0]
	return np.random.choice(best_actions)

def q_learning(args):
	Q = {}
	train_scores = []
	eval_scores = []
	eval_episodes = args.eval_episodes

	if args.pl_type == "rand":
		pl_func = random
	elif args.pl_type == "greedy":
		pl_func = greedy
	elif args.pl_type == "egreedy":
		pl_func = epsilon_greedy

	if args.adv_type == "rand":
		adv_func = random
	elif args.adv_type == "greedy":
		adv_func = greedy
	elif args.adv_type == "aperf":
		adv_func = perfect
														  # for each episode ...
	for train_ep in range(1, args.train_episodes + 1):

													# ... get the initial state,
		score = 0
		game = get_initial_state(args.display_size, args.paleta_size, args.learning_rate, args.discount, args.epsilon, args.pl_type, args.adv_type)
		#game = get_initial_state(args.display_size, args.paleta_size)
		state = game.get_state("player")
		state_adv = game.get_state("advers")
											   # display current state and sleep
		if args.verbose:
			game.init_draw()
			game.draw(); sleep(args.sleep)

										   # while current state is not terminal
		while not game.is_final_state():

											   # choose one of the legal actions
			actions = game.get_legal_actions("player")
			action = pl_func(Q, state, actions, args.epsilon)


			actions_adv = game.get_legal_actions("advers")
			action_adv = adv_func(Q, state_adv, actions_adv, args.epsilon)

							# apply action and get the next state and the reward
			o_state = state

			#print(o_state)
			reward, msg = game.apply_action(action, action_adv)
			state = game.get_state("player")
			state_adv = game.get_state("advers")
			
			score += reward


			# TODO (1) : Q-Learning
			n_actions = game.get_legal_actions("player")
			best_act = best_action(Q, state, n_actions)
			if (state, best_act) in Q:
				maxQ = Q[(state, best_act)]
			else:
				maxQ = 0.0

			if (o_state, action) not in Q:
				Q[(o_state, action)] = 0.0
			Q[(o_state, action)] += args.learning_rate*(reward + args.discount*maxQ -  Q[(o_state, action)])

											   # display current state and sleep
			if args.verbose:
				print(msg); game.draw(); sleep(args.sleep)

		print("Episode %6d / %6d rew %6d" % (train_ep, args.train_episodes, score))
		train_scores.append(score)

													# evaluate the greedy policy
		# TODO (4) : Evaluate
		if train_ep % args.eval_every == 0:
			#print Q
			print len(Q)
			avg_score = 0.0
			for i in xrange(eval_episodes):
				game = get_initial_state(args.display_size, args.paleta_size, args.learning_rate, args.discount, args.epsilon, args.pl_type, args.adv_type)
				state = game.get_state("player")
				state_adv = game.get_state("advers")

				final_score = 0
				while not game.is_final_state():

					action = best_action(Q, state, game.get_legal_actions("player"))

					actions_adv = game.get_legal_actions("advers")
					action_adv = adv_func(Q, state_adv, actions_adv, args.epsilon)

					reward, msg = game.apply_action(action, action_adv)
					state = game.get_state("player")
					state_adv = game.get_state("advers")

					final_score += reward
				avg_score += final_score
			avg_score = avg_score/eval_episodes
			eval_scores.append(avg_score)

	# --------------------------------------------------------------------------
	if args.final_show:
		#print Q
		game = get_initial_state(args.display_size, args.paleta_size, args.learning_rate, args.discount, args.epsilon, args.pl_type, args.adv_type)
		game.init_draw()

		state = game.get_state("player")
		state_adv = game.get_state("advers")

		final_score = 0
		while not game.is_final_state():
			actions = game.get_legal_actions("player")
			action = best_action(Q, state, actions)
			

			actions_adv = game.get_legal_actions("advers")
			action_adv = adv_func(Q, state_adv, actions_adv, args.epsilon)

			# print "play: " + str(actions) + "  " + action + "  " + str(state)
			#print "adv: " + str(actions_adv) + "  " + action_adv + "  " + str(state_adv)

			reward, msg = game.apply_action(action, action_adv)
			state = game.get_state("player")
			state_adv = game.get_state("advers")

			final_score += reward
			#print(msg); 
			game.draw(); sleep(args.sleep)
		print("final score: %s" % final_score)

	if args.plot_scores:
		from matplotlib import pyplot as plt
		
		plt.xlabel("Episode")
		plt.ylabel("Average score")
		plt.axis([-(args.train_episodes * 0.03), args.train_episodes+(args.train_episodes * 0.03), -1.1, 1.1])

		plt.plot(
			np.linspace(1, args.train_episodes, args.train_episodes),
			np.convolve(train_scores, [0.2,0.2,0.2,0.2,0.2], "same"),
			linewidth = 1.0, color = "blue"
		)
		plt.plot(
			np.linspace(args.eval_every, args.train_episodes, len(eval_scores)),
			eval_scores, linewidth = 2.0, color = "red"
		)
		plt.show()

if __name__ == "__main__":
	parser = ArgumentParser()
	# Input params
	parser.add_argument("--display_size", type = int, default = 6,
						help = "Size of the display")
	parser.add_argument("--paleta_size", type = int, default = 4,
						help = "Size of the paleta")
	parser.add_argument("--pl_type", type = str, default = "egreedy",
						help = "Player type: rand, greedy, egreedy")
	parser.add_argument("--adv_type", type = str, default = "aperf",
						help = "Adversary type: rand, greedy, aperf")
	# Meta-parameters
	parser.add_argument("--learning_rate", type = float, default = 0.1,
						help = "Learning rate")
	parser.add_argument("--discount", type = float, default = 0.99,
						help = "Value for the discount factor")
	parser.add_argument("--epsilon", type = float, default = 0.05,
						help = "Probability to choose a random action.")
	# Training and evaluation episodes
	parser.add_argument("--train_episodes", type = int, default = 1000,
						help = "Number of episodes")
	parser.add_argument("--eval_every", type = int, default = 100,
						help = "Evaluate policy every ... games.")
	parser.add_argument("--eval_episodes", type = float, default = 10,
						help = "Number of games to play for evaluation.")
	# Display
	parser.add_argument("--verbose", dest="verbose",
						action = "store_true", help = "Print each state")
	parser.add_argument("--plot", dest="plot_scores", action="store_true",
						help = "Plot scores in the end")
	parser.add_argument("--sleep", type = float, default = 0.05,
						help = "Seconds to 'sleep' between moves.")
	parser.add_argument("--final_show", dest = "final_show",
						action = "store_true",
						help = "Demonstrate final strategy.")
	args = parser.parse_args()
	q_learning(args)
