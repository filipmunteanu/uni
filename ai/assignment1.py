import sys
import pickle
from copy import deepcopy

TYPE = "type"
ARGS = "args"

def predicate(name, args=[]):
	return {TYPE : name, ARGS : args}

def is_sat(state, precond):
	for p in precond:
		if p not in state:
			return p
	return True

def add_uniq(l, precond, state):
	if precond not in l and precond not in state:
		l.append(precond)
	return l


class Fly:
	def __init__(self, startCell, stopCell):
		self.startCell = startCell
		self.stopCell = stopCell

		self.precond = [predicate("position", startCell)]
		self.addit = [predicate("position", self.stopCell)]
		self.delet = [predicate("position", self.startCell)]

	def get_action(self):
		act = 'Fly(' + str(self.startCell) + ', ' + str(self.stopCell) + ')'
		return act


class Load:
	def __init__(self, position, productId):
		self.productId = productId
		self.position = position

		self.precond = [
			predicate("warehouse", position), 
			predicate("hasProduct", (position, productId)), 
			predicate("position", position),
			predicate("empty")
		]
		self.addit = [
			predicate("position", position), 
			predicate("carries", self.productId)
		]
		self.delet = [predicate("empty")]

	def get_action(self):
		act = 'Load(' + str(self.position) + ', ' + str(self.productId) + ')'
		act = 'Load(' + str(self.productId) + ')'
		return act


class Deliver:
	def __init__(self, position, productId):
		self.productId = productId
		self.position = position

		self.precond = [
			predicate("position", position), 
			predicate("carries", productId), 
			predicate("client", position),
			predicate("order", (position, productId))
		]
		self.addit = [
			predicate("position", position), 
			predicate("delivered", (self.position, self.productId)), 
			predicate("empty")
		]
		self.delet = [predicate("carries", self.productId)]


	def get_action(self):
		act = 'Deliver(' + str(self.position) + ', ' + str(self.productId) + ')'
		act = 'Deliver(' + str(self.productId) + ')'
		return act


def rec(state, goals, path, scenario, level, act, position):
	new_goals = deepcopy(goals)
	new_path = deepcopy(path)

	for ef in act.addit:
		new_goals.remove(ef)
	for prec in act.precond:
		new_goals = add_uniq(new_goals, prec, state)

	new_path.insert(0, act.get_action())
	return backtrack(state, new_goals, new_path, scenario, level+1, position)

def backtrack(state, goals, path, scenario, level, position):
	if goals == [predicate("empty")]:
		print ""
		return path
	
	if level % 2 == 0:
	# Deliver
		for o in scenario["orders"]:
			act = Deliver(o[0], o[1])
			if is_sat(goals, act.addit) == True:
				ret = rec(state, goals, path, scenario, level, act, position)
				if ret != False:
					return ret

		# Load
		for ap in scenario["available_products"]:
			act = Load(ap[0], ap[1])
			if is_sat(goals, act.addit) == True:
				ret = rec(state, goals, path, scenario, level, act, position)
				if ret != False:
					return ret
	else:
	# Fly
		pos2 = scenario["clients"]
		pos2.append(scenario["initial_position"])

		for cl in scenario["clients"]:
			act = Fly(cl, position)
			if is_sat(goals, act.addit) == True:
				ret = rec(state, goals, path, scenario, level, act, cl)
				if ret != False:
					return ret

		for w in scenario["warehouses"]:	
			act = Fly(w, position)
			if is_sat(goals, act.addit) == True:
				ret = rec(state, goals, path, scenario, level, act, w)
				if ret != False:
					return ret

	return False

def make_plan(scenario):
	print "Scenario"
	print "available_products " + str(scenario["available_products"])
	print "dimensions " + str(scenario["dimensions"])
	print "warehouses " + str(scenario["warehouses"])
	print "clients " + str(scenario["clients"])
	print "initial_position " + str(scenario["initial_position"])
	print "number_of_products " + str(scenario["number_of_products"])
	print "orders " + str(scenario["orders"])
	print ""

	l = []
	known_facts = []
	known_facts.append(predicate("position", scenario["initial_position"]))

	for w in scenario["warehouses"]:
		known_facts.append(predicate("warehouse", w))
	for ap in scenario["available_products"]:
		known_facts.append(predicate("hasProduct", ap))
	for cl in scenario["clients"]:
		known_facts.append(predicate("client", cl))
	for o in scenario["orders"]:
		known_facts.append(predicate("order", o))
	
	end_pos = scenario["orders"][0][0]

	goals = [predicate("empty"), predicate("position", end_pos)]
	path = []
	for i in scenario["orders"]:
		goals.append(predicate("delivered", i))
	print goals
	#path = 

	return backtrack(known_facts, goals, path, scenario, 0, end_pos)

def main(args):
	scenario = pickle.load(open(args[1]))
	plan = make_plan(scenario)
	print plan

	#check(scenario, plan)

if __name__ == '__main__':
	main(sys.argv)
