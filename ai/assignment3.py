import sys
from copy import deepcopy
from math import sqrt
from functools import reduce
from heapq import heappop, heappush
import numpy as np
import matplotlib.pyplot as plt

w_map = {}

def cnv(x):
	if x == 'X':
		return 1
	else:
		return 0


def print_lab(lab):
	for i in lab:
		for j in i:
			sys.stdout.write(str(j))
		print ""

########################################### Din lab01 ###########################################

def euclidean_distance(a, b):  
	return sqrt(sum( (a - b)**2 for a, b in zip(a, b)))

def manhattan_distance(a, b):
	return sum(abs(e - s) for s,e in zip(a, b))

def is_good(pos):
	(r, c) = pos
	if(r < w_map['M'] and r > 0 and c < w_map['N'] and c > 0):
		if(w_map['L'][r][c] != 1):
			for gate in w_map['G']:
				if gate[0] == pos:
					return False
			return True
	return False

def get_neighbours(pos):
	(r, c) = pos # Asa se poate desface o pozitie in componentele sale
	res = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)] 
	return list(filter(is_good, res))

def astar1(start, end, h):
	# Frontiera, ca lista (heap) de tupluri (cost-total-estimat, nod)
	frontier = []
	heappush(frontier, (0 + h(start, end), start))
	# Nodurile descoperite ca dictionar nod -> (parinte, cost-pana-la-nod)
	print start
	discovered = {start: (None, 0)}
	while frontier:
		(current_score, current_node) = heappop(frontier)
		if current_node == end:
			break;
		neighbours = get_neighbours(current_node)
		for neighbour in neighbours:
			if neighbour in discovered:
				if discovered[neighbour][1] > current_score + 1:
					discovered[neighbour][1] = current_score + 1
			else:
				discovered[neighbour] = (current_node, current_score +1)
				heappush(frontier, (current_score + 1 + h(neighbour, end), neighbour))
			
	
	cost_map = [[discovered[(r,c)][1] if (r,c) in discovered else 0 for c in range(w_map['N'])]for r in range(w_map['M'])]
	plt.imshow(cost_map , cmap='Greys', interpolation='nearest');
	
	# Refacem drumul
	path = []
	path_node = end
	while True:
		path.append(path_node)
		path_node = discovered[path_node][0]
		if path_node is None:
			break
	return path[::-1] # drumul, ca lista de pozitii




########################################### Subpct 2 ###########################################	
def is_gate(pos):
	for gate in w_map['G']:
		if gate[0] == pos:
			return gate[1]
	return False

def is_dest(pos):
	for gate in w_map['G']:
		for dest in gate[1]:
			d_pos = (dest[0], dest[1])
			if pos == d_pos:
				return gate[0]
	return False

def is_good2(pos):
	(r, c) = pos
	#print str(r) + " " + str(c)
	if(r < w_map['M'] and r > 0 and c < w_map['N'] and c > 0):
		if(w_map['L'][r][c] != 1):
			return True
	return False

def get_neighbours2(pos):
	(r, c) = pos #- Asa se poate desface o pozitie in componentele sale
	res = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)] 
	return list(filter(is_good2, res))

def astar2(start, end, h):
	# Frontiera, ca lista (heap) de tupluri (cost-total-estimat, nod)
	frontier = []
	heappush(frontier, (0 + h(start, end), start))
	# Nodurile descoperite ca dictionar nod -> (parinte, cost-pana-la-nod)
	discovered = {start: (None, 0)}
	while frontier:
		(current_score, current_node) = heappop(frontier)
		if current_node == end:
			break;
		neighbours = get_neighbours2(current_node)
		for neighbour in neighbours:
			if neighbour not in discovered or (discovered[neighbour][1] > current_score + 1):
				gt = is_gate(neighbour)

				if gt is False:
					discovered[neighbour] = (current_node, current_score +1)
					heappush(frontier, (current_score + 1 + h(neighbour, end), neighbour))
				else:
					discovered[neighbour] = (current_node, current_score +1)
					dist = 0

					for i in gt:
						dist += h((i[0], i[1]), end)*i[2]
					
					heappush(frontier, (current_score + 1 + dist, neighbour))
					if dist <= h(neighbour, end):
						for i in gt:
							i_pos = (i[0], i[1])
							if i_pos not in discovered or (discovered[i_pos][1] > current_score + 1):
								discovered[i_pos] = (neighbour, current_score +1)
								heappush(frontier, (current_score + 1 + h(i_pos, end), i_pos))
	
	cost_map = [[discovered[(r,c)][1] if (r,c) in discovered else 0 for c in range(w_map['N'])]for r in range(w_map['M'])]
	plt.imshow(cost_map , cmap='Greys', interpolation='nearest');

	# Refacem drumul
	path = []
	path_node = end
	while True:
		path.append(path_node)
		path_node = discovered[path_node][0]
		if path_node is start:
			break
	return path[::-1] # drumul, ca lista de pozitii


def game2(start, end, h):
	f_path = []
	f_path.append(start)
	count_tele = 0
	path = astar2(w_map['Pi'], w_map['Pf'], h)
	while len(path) != 1:
		f_path.append(path[0])
		gt = is_gate(path[0])
		if gt == False:
			path = astar2(path[0], w_map['Pf'], h)
		else:
			prob = []
			for i in gt:
				prob.append(i[2])

			val = []
			for i in xrange(0, len(prob)):
				val.append(i)
			x = np.random.choice(val, p=prob)
			choice = (gt[x][0], gt[x][1])
			count_tele += 1
			f_path.append(choice)
			path = astar2(choice, w_map['Pf'], h)
	
	return f_path


########################################### Subpct 3 ###########################################


def is_gate3(pos):
	for gate in w_map['G3']:
		if gate[0] == pos:
			return gate[1]
	return False

def is_dest3(pos):
	for gate in w_map['G3']:
		for dest in gate[1]:
			d_pos = (dest[0], dest[1])
			if pos == d_pos:
				return gate[0]
	return False


def astarEx(start, end, h):
	# Frontiera, ca lista (heap) de tupluri (cost-total-estimat, nod)
	frontier = []
	heappush(frontier, (0 + h(start, end), start))
	# Nodurile descoperite ca dictionar nod -> (parinte, cost-pana-la-nod)
	discovered = {start: (None, 0)}
	while frontier:
		(current_score, current_node) = heappop(frontier)
		if current_node == end:
			break;
		neighbours = get_neighbours2(current_node)
		for neighbour in neighbours:
			if neighbour in discovered:
				if discovered[neighbour][1] > current_score + 1:
					discovered[neighbour][1] = current_score + 1
			else:
				discovered[neighbour] = (current_node, current_score +1)
				heappush(frontier, (current_score + 1 + h(neighbour, end), neighbour))
			
	
	cost_map = [[discovered[(r,c)][1] if (r,c) in discovered else 0 for c in range(w_map['N'])]for r in range(w_map['M'])]
	plt.imshow(cost_map , cmap='Greys', interpolation='nearest');
	
	# Refacem drumul
	path = []
	path_node = end
	while True:
		path.append(path_node)
		path_node = discovered[path_node][0]
		if path_node is None:
			break
	return path[::-1] # drumul, ca lista de pozitii


def astar3(start, end, h):
	#telep = []
	# Frontiera, ca lista (heap) de tupluri (cost-total-estimat, nod)
	frontier = []
	heappush(frontier, (0 + h(start, end), start))
	# Nodurile descoperite ca dictionar nod -> (parinte, cost-pana-la-nod)
	discovered = {start: (None, 0)}
	while frontier:
		(current_score, current_node) = heappop(frontier)
		if current_node == end:
			break;
		neighbours = get_neighbours2(current_node)
		for neighbour in neighbours:
			if neighbour not in discovered or (discovered[neighbour][1] > current_score + 1):
				gt = is_gate3(neighbour)
				if gt is False:
					discovered[neighbour] = (current_node, current_score +1)
					heappush(frontier, (current_score + 1 + h(neighbour, end), neighbour))
				else:
					discovered[neighbour] = (current_node, current_score +1)
					dist = 0
					for i in gt:
						dist += h((i[0], i[1]), end)*i[2]
					
					heappush(frontier, (current_score + 1 + dist, neighbour))
					if dist <= h(neighbour, end):
						for i in gt:
							i_pos = (i[0], i[1])

							if i_pos not in discovered or (discovered[i_pos][1] > current_score + 1):
								discovered[i_pos] = (neighbour, current_score +1)
								heappush(frontier, (current_score + 1 + h(i_pos, end), i_pos))
	
	cost_map = [[discovered[(r,c)][1] if (r,c) in discovered else 0 for c in range(w_map['N'])]for r in range(w_map['M'])]
	plt.imshow(cost_map , cmap='Greys', interpolation='nearest');

	# Refacem drumul
	path = []
	path_node = end
	while True:
		path.append(path_node)
		path_node = discovered[path_node][0]
		if path_node is start:
			break
	return path[::-1] # drumul, ca lista de pozitii

def explore3(start, pasi):
	cnt = len(w_map['G'])
	gates = []
	for i in w_map['G']:
		gates.append([i[0], []])
	
	ppg = pasi/len(gates)

	for kk1 in xrange(len(gates)):
		ppg_crt = ppg
		probs = {}
		tot = 0
		while ppg_crt > 0:
			path = astarEx(start, gates[kk1][0], manhattan_distance)
			ppg_crt -= len(path)

			gt = is_gate(gates[kk1][0])
			prob = []
			for i in gt:
				prob.append(i[2])


			val = []
			for i in xrange(0, len(prob)):
				val.append(i)
			x = np.random.choice(val, p=prob)
			choice = (gt[x][0], gt[x][1])


			if choice in probs:
				probs[choice] = probs[choice] + 1
			else:
				probs[choice] = 1
			start = choice
			tot += 1

		for key, value in probs.iteritems():
			gates[kk1][1].append((key[0], key[1], value*1.0/tot))
	print "gates"
	print gates
	w_map['G3'] = gates


def game3(start, end, h, pasi):
	
	f_path = []
	f_path.append(start)
	count_tele = 0
	path = astar2(w_map['Pi'], w_map['Pf'], h)
	while len(path) != 1:
		f_path.append(path[0])
		gt = is_gate(path[0])
		if gt == False:
			path = astar2(path[0], w_map['Pf'], h)
		else:
			prob = []
			for i in gt:
				prob.append(i[2])

			val = []
			for i in xrange(0, len(prob)):
				val.append(i)
			x = np.random.choice(val, p=prob)
			choice = (gt[x][0], gt[x][1])
			count_tele += 1
			f_path.append(choice)
			path = astar2(choice, w_map['Pf'], h)
		
	return len(f_path)-count_tele


def read_map(in_file):
	w_map['M'], w_map['N'], w_map['T'] = [int(x) for x in next(in_file).split()]
	w_map['Pi'] = tuple([int(x) for x in next(in_file).split()])
	w_map['Pf'] = tuple([int(x) for x in next(in_file).split()])
	w_map['Pi'] = (w_map['Pi'][1], w_map['Pi'][0])
	w_map['Pf'] = (w_map['Pf'][1], w_map['Pf'][0])

	tel = []
	for i in xrange(w_map['T']):
		val = next(in_file).split()
		g_pos = (int(val[1]), int(val[0]))
		d_pos = []
		for j in xrange(3, (int(val[2])+1)*3, 3):
			d_pos.append((int(val[j+1]), int(val[j]), float(val[j+2])))
		tel.append((g_pos, d_pos))
	w_map['G'] = tel

	labyrinth = [[cnv(c) for c in line.strip()] for line in in_file]
	for x in labyrinth:
		if x == []:
			labyrinth.remove(x)
	w_map["L"] = labyrinth


def main(args):
	in_file = open(args[1])
	read_map(in_file)
	print w_map
	print_lab(w_map['L'])

	# plt.imshow(w_map['L'], cmap='Greys')
	# plt.plot([w_map['Pi'][1]], [w_map['Pi'][0]], 'bo')
	# plt.plot([w_map['Pf'][1]], [w_map['Pf'][0]], 'ro')
	# for t in w_map['G']:
	# 	y, x = t[0]
	# 	plt.plot([x], [y], 'go')
	# plt.show()

	'''
	path = astar1(w_map['Pi'], w_map['Pf'], manhattan_distance)
	plt.plot([w_map['Pi'][1]], [w_map['Pi'][0]], 'bo')
	plt.plot([w_map['Pf'][1]], [w_map['Pf'][0]], 'ro')

	for t in w_map['G']:
		y, x = t[0]
		plt.plot([x], [y], 'go')

	for y, x in path:
		plt.plot([x], [y], 'rx')
	plt.show()
	print path
	'''


	# cost_tot = 0
	# for i in xrange(10):
	# 	# cost_tot += 
	# 	print game2(w_map['Pi'], w_map['Pf'], manhattan_distance)
	# print cost_tot/1000.0

	cost_tot = 0
	explore3(w_map['Pi'], 100)
	for i in xrange(1000):
		 cost_tot += game3(w_map['Pi'], w_map['Pf'], manhattan_distance, 100)
	print "100"
	print cost_tot/1000.0

	cost_tot = 0
	explore3(w_map['Pi'], 1000)
	for i in xrange(1000):
		 cost_tot += game3(w_map['Pi'], w_map['Pf'], manhattan_distance, 1000)
	print "1000"
	print cost_tot/1000.0


	cost_tot = 0
	explore3(w_map['Pi'], 10000)
	for i in xrange(1000):
		cost_tot += game3(w_map['Pi'], w_map['Pf'], manhattan_distance, 10000)
	print "10000"
	print cost_tot/1000.0
	#print game3(w_map['Pi'], w_map['Pf'], manhattan_distance, 100)

	# path = game2(w_map['Pi'], w_map['Pf'], manhattan_distance)
	# plt.plot([w_map['Pi'][1]], [w_map['Pi'][0]], 'bo')
	# plt.plot([w_map['Pf'][1]], [w_map['Pf'][0]], 'ro')

	# for t in w_map['G']:
	# 	y, x = t[0]
	# 	plt.plot([x], [y], 'go')

	# for y, x in path:
	# 	plt.plot([x], [y], 'rx')
	# plt.show()
	

if __name__ == '__main__':
	main(sys.argv)


	
	
