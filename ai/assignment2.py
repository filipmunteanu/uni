#!/usr/bin/env python

from copy import copy, deepcopy
from itertools import combinations
from argparse import ArgumentParser, Namespace
import sys
import time
import signal, os

DI = 0
TI = 1
REP = 2 #repartitie
PROC = 3
COND = 4


def read_input_file(in_file):
	tasks = {}
	with open(in_file) as f:
		n, p = map(int, f.readline().strip().split(","))
		for _ in range(n):
			task_info = list(map(int, f.readline().strip().split(",")))
			i, di, ti = task_info[0:3]
			tasks[i] = [di, ti, -1, -1, task_info[3:]]
	return n, p, tasks

# Verificare constrangeri pentru taskul curent
def check_constr(tasks, current):
	const = tasks[current][COND]

	for c in const:
		if tasks[c][REP] == -1 or (tasks[c][REP] + tasks[c][DI] > tasks[current][REP]):
			return False

	return True

# scriere solutie in fisier
def write_sol(tasks):
	out_f = open("out_file", "w")
		
	for ppp in xrange(no_p):
		cnt = 0
		lst = []
		for zz in xrange(1, n+1):
			if tasks[zz][PROC] == ppp:
				lst.append((zz, tasks[zz][REP]))
				cnt += 1

		out_f.write(str(cnt) + "\n")
		ddd = sorted(lst, key=lambda x: x[1])
		for xx in ddd:
			out_f.write(str(xx[0]) + "," + str(xx[1]) + "\n")


# backtracking simplu
def PCSP_simple(unsolved, procs, tasks, cost):
	global best_cost
	global best_solution
	global n
	global no_p
	global init_time

	# daca s-au planificat toate taskurile inseamna ca s-a gasit o solutie mai buna
	if unsolved == []:
		best_cost = cost
		best_solution = tasks

		write_sol(tasks)
		time1 = time.clock()
		print str(time1 - init_time) + "\t" + str(best_cost)
		return

	# se parcurg toate taskurile neplanificate si toate procesoarele incercandu-se variante
	for t in unsolved:
		for p in xrange(no_p):
			new_tasks = deepcopy(tasks)
			new_procs = deepcopy(procs)
			new_tasks[t][REP] = new_procs[p][1]
			new_tasks[t][PROC] = new_procs[p][0]
			new_procs[p][1] = new_procs[p][1] + new_tasks[t][DI]

			# se verifica constrangerile
			if check_constr(new_tasks, t) == False:
				continue

			# se verifica costul	
			delay = (new_tasks[t][REP] + new_tasks[t][DI]) - new_tasks[t][TI]
			if delay > 0:
				new_cost = cost + delay
			else:
				new_cost = cost
			if new_cost >= best_cost:
				continue

			new_unsolved = []
			for i in unsolved:
				if i != t:
					new_unsolved.append(i)

			PCSP_simple(new_unsolved, new_procs, new_tasks, new_cost)

def PCSP_ord_val(unsolved, procs, tasks, cost):
	global best_cost
	global best_solution
	global n
	global no_p
	global init_time

	if unsolved == []:
		best_cost = cost
		best_solution = tasks

		write_sol(tasks)
		time1 = time.clock()
		print str(time1 - init_time) + "	" + str(best_cost)
		return

	# se ordoneaza valorile
	procs = sorted(procs, key=lambda x: x[1])
	for t in unsolved:
		for p in xrange(no_p):
			new_tasks = deepcopy(tasks)
			new_procs = deepcopy(procs)
			new_tasks[t][REP] = new_procs[p][1]
			new_tasks[t][PROC] = new_procs[p][0]
			new_procs[p][1] = new_procs[p][1] + new_tasks[t][DI]

			if check_constr(new_tasks, t) == False:
				continue

			delay = (new_tasks[t][REP] + new_tasks[t][DI]) - new_tasks[t][TI]
			if delay > 0:
				new_cost = cost + delay
			else:
				new_cost = cost
			if new_cost >= best_cost:
				continue

			new_unsolved = []
			for i in unsolved:
				if i != t:
					new_unsolved.append(i)
			PCSP_ord_val(new_unsolved, new_procs, new_tasks, new_cost)



def PCSP_ord_var(unsolved, procs, tasks, cost):
	global best_cost
	global best_solution
	global n
	global no_p
	global init_time

	if unsolved == []:
		best_cost = cost
		best_solution = tasks

		write_sol(tasks)
		time1 = time.clock()
		print str(time1 - init_time) + "	" + str(best_cost)
		return

	# se ordoneaza variabilele
	lst = []
	for zz in xrange(1, n+1):
		lst.append((zz, tasks[zz][TI]))
	ddd = sorted(lst, key=lambda x: x[1])

	sorted_unsolved = []
	for d in ddd:
		if d[0] in unsolved:
			sorted_unsolved.append(d[0])
	unsolved = sorted_unsolved

	for t in unsolved:
		for p in xrange(no_p):
			new_tasks = deepcopy(tasks)
			new_procs = deepcopy(procs)
			new_tasks[t][REP] = new_procs[p][1]
			new_tasks[t][PROC] = new_procs[p][0]
			new_procs[p][1] = new_procs[p][1] + new_tasks[t][DI]

			if check_constr(new_tasks, t) == False:
				continue

			delay = (new_tasks[t][REP] + new_tasks[t][DI]) - new_tasks[t][TI]
			if delay > 0:
				new_cost = cost + delay
			else:
				new_cost = cost
			if new_cost >= best_cost:
				continue

			new_unsolved = []
			for i in unsolved:
				if i != t:
					new_unsolved.append(i)
			PCSP_ord_var(new_unsolved, new_procs, new_tasks, new_cost)


def PCSP_AC(unsolved, procs, tasks, cost):
	global best_cost
	global best_solution
	global n
	global no_p
	global init_time

	if unsolved == []:
		best_cost = cost
		best_solution = tasks

		write_sol(tasks)
		time1 = time.clock()
		print str(time1 - init_time) + "	" + str(best_cost)
		return

	# se reduce multimea de taskuri ce urmaza a fi testate in functie de dependindinte
	unsolved_red = []
	for i in unsolved:
		ttt = True
		const = tasks[i][COND]
		for c in const:
			if tasks[c][REP] == -1:
				ttt = False
				break
		if ttt is True:
			unsolved_red.append(i)

	for t in unsolved_red:
		for p in xrange(no_p):

			new_tasks = deepcopy(tasks)
			new_procs = deepcopy(procs)
			new_tasks[t][REP] = new_procs[p][1]
			new_tasks[t][PROC] = new_procs[p][0]
			new_procs[p][1] = new_procs[p][1] + new_tasks[t][DI]

			if check_constr(new_tasks, t) == False:
				continue

			delay = (new_tasks[t][REP] + new_tasks[t][DI]) - new_tasks[t][TI]
			if delay > 0:
				new_cost = cost + delay
			else:
				new_cost = cost
			if new_cost >= best_cost:
				continue

			new_unsolved = []
			for i in unsolved:
				if i != t:
					new_unsolved.append(i)

			PCSP_AC(new_unsolved, new_procs, new_tasks, new_cost)

def PCSP_ord_ambele(unsolved, procs, tasks, cost):
	global best_cost
	global best_solution
	global n
	global no_p
	global init_time

	if unsolved == []:
		best_cost = cost
		best_solution = tasks

		write_sol(tasks)
		time1 = time.clock()
		print str(time1 - init_time) + "	" + str(best_cost)
		return

	lst = []
	for zz in xrange(1, n+1):
		lst.append((zz, tasks[zz][TI]))
	ddd = sorted(lst, key=lambda x: x[1])

	sorted_unsolved = []
	for d in ddd:
		if d[0] in unsolved:
			sorted_unsolved.append(d[0])
	unsolved = sorted_unsolved

	procs = sorted(procs, key=lambda x: x[1])

	for t in unsolved:
		for p in xrange(no_p):
			new_tasks = deepcopy(tasks)
			new_procs = deepcopy(procs)
			new_tasks[t][REP] = new_procs[p][1]
			new_tasks[t][PROC] = new_procs[p][0]
			new_procs[p][1] = new_procs[p][1] + new_tasks[t][DI]

			if check_constr(new_tasks, t) == False:
				continue

			delay = (new_tasks[t][REP] + new_tasks[t][DI]) - new_tasks[t][TI]
			if delay > 0:
				new_cost = cost + delay
			else:
				new_cost = cost
			if new_cost >= best_cost:
				continue

			new_unsolved = []
			for i in unsolved:
				if i != t:
					new_unsolved.append(i)
			PCSP_ord_ambele(new_unsolved, new_procs, new_tasks, new_cost)


def sort_after_cond(unsolved, tasks):
	global n

	res = []
	for i in unsolved:
		res.append([i, 0]) 

	for i in res:
		for j in xrange(1, n+1):
			if i[0] in tasks[j][COND]:
				i[1] += 1

	res = sorted(res, key=lambda x: x[1])

	res2 = [r[0] for r in res]
	return res2

# numarul de conditionari
def PCSP_ord_depend(unsolved, procs, tasks, cost):
	global best_cost
	global best_solution
	global n
	global no_p
	global init_time

	# de ordoneaza variabilele in functie de numarul de constrangeri in care apar
	if unsolved == []:
		best_cost = cost
		best_solution = tasks

		write_sol(tasks)
		time1 = time.clock()
		print str(time1 - init_time) + "	" + str(best_cost)
		return

	unsolved = sort_after_cond(unsolved, tasks)
	for t in unsolved:
		for p in xrange(no_p):
			new_tasks = deepcopy(tasks)
			new_procs = deepcopy(procs)
			new_tasks[t][REP] = new_procs[p][1]
			new_tasks[t][PROC] = new_procs[p][0]
			new_procs[p][1] = new_procs[p][1] + new_tasks[t][DI]

			if check_constr(new_tasks, t) == False:
				continue

			delay = (new_tasks[t][REP] + new_tasks[t][DI]) - new_tasks[t][TI]
			if delay > 0:
				new_cost = cost + delay
			else:
				new_cost = cost
			if new_cost >= best_cost:
				continue

			new_unsolved = []
			for i in unsolved:
				if i != t:
					new_unsolved.append(i)

			PCSP_ord_depend(new_unsolved, new_procs, new_tasks, new_cost)


def main():
	arg_parser = ArgumentParser()
	arg_parser.add_argument("in_file", help="Problem file")
	args = arg_parser.parse_args()
	sys.setrecursionlimit(2500)
	global n
	global no_p

	n, no_p, tasks = read_input_file(args.in_file)
	procs = []
	for i in xrange(no_p):
		procs.append([i, 0])

	unsolved = []
	for i in xrange(1, n + 1):
		unsolved.append(i)

	global best_solution
	global best_cost

	best_solution = {}
	best_cost = sys.maxint

	global init_time
	init_time = time.clock()
	
	signal.alarm(200)

	# simple backtracking
	PCSP_simple(deepcopy(unsolved), deepcopy(procs), deepcopy(tasks), 0)

	# backtracking with ordering by variables
	#PCSP_ord_var(deepcopy(unsolved), deepcopy(procs), deepcopy(tasks), 0)

	# backtracking with Arc C
	#PCSP_AC(deepcopy(unsolved), deepcopy(procs), deepcopy(tasks), 0)

	# backtracking with ordering by variables found in constraints
	#PCSP_ord_depend(deepcopy(unsolved), deepcopy(procs), deepcopy(tasks), 0)

	# backtracking with ordering by values
	#PCSP_ord_val(deepcopy(unsolved), deepcopy(procs), deepcopy(tasks), 0)

	# backtracking with ordering by variables and values
	#PCSP_ord_ambele(deepcopy(unsolved), deepcopy(procs), deepcopy(tasks), 0)

	print best_solution
	print best_cost


if __name__ == "__main__":
	main()
