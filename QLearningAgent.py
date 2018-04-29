import os
import numpy as np

class QLearningAgent(object):

	def __init__(self):
		self.game_count = 0
		self.discount_factor = 1.0
		self.learning_rate = 0.7
		self.reward = {0:1,1:-1000}
		self.previous_state = [96,47,0]
		self.previous_action = 0
		self.moves = []
		self.scores = []
		self.max_score = 0
		self.xdim = 120
		self.ydim = 120
		self.vdim = 20
		self.qvalues = np.zeros((self.xdim, self.ydim, self.vdim, 2))
		self.get_model()

	def get_model(self):
		if os.path.exists("qvalues.txt"):
			self.read_data()
		
	def act(self, xdist, ydist, vely):
		state = [xdist,ydist,vely]
		self.moves.append([self.previous_state,self.previous_action,state])
		self.previous_state = state

		if self.qvalues[xdist,ydist,vely][0] >= self.qvalues[xdist,ydist,vely][1]:
			self.previous_action = 0
		else:
			self.previous_action = 1
		return self.previous_action

	def update_qvalues(self, score):
		history = list(reversed(self.moves))
		
		first = True
		jump = True
		for move in history:
			[x,y,v] = move[0]
			action = move[1]
			[x1,y1,z1] = move[2]
			r = 0
			if first:
				r = 1
				first = False
			if jump and action:
				r = 1
				jump = False
			self.qvalues[x,y,v,action] = (1- self.learning_rate) * (self.qvalues[x,y,v,action]) + (self.learning_rate) * ( self.reward[r] + (self.discount_factor)*max(self.qvalues[x1,y1,z1,0],self.qvalues[x1,y1,z1,1]))

		self.game_count += 1
		self.moves = []
		self.max_score = max(self.max_score, score)
		print("Game count: " + str(self.game_count) + " Score: " + str(score) + " Max Score: " + str(self.max_score))
		self.scores.append(score)
		
	def write_data(self):
		qfile = open("qvalues.txt","w")
		data = ""
		for x in range(120):
			for y in range(120):
				for v in range(20):
					for a in range(2):
						data += str(x) + ", " + str(y) + ", " + str(v) + ", " + str(a) + ", " + str(self.qvalues[x,y,v,a]) + "\n"
		qfile.write(data)
		qfile.close()
		sfile = open("scores.txt","w")
		data1 = ''
		for i in range(len(self.scores)):
			data1 += str(i) + ',' + str(self.scores[i]) + "\n"
		sfile.write(data1)
		sfile.close() 

	def read_data(self):
		qfile = open("qvalues.txt","r")
		line = qfile.readline()
		while len(line) != 0:
			print(line)
			state = line.split(',')
			self.qvalues[int(state[0]),int(state[1]),int(state[2]),int(state[3])] = float(state[4])
			line = qfile.readline()
		qfile.close()

