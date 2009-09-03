##
# This file is part of N.O.D.A.C.
#
# (c) Copyright 2009 N.O.D.A.C. Development Team
#
# N.O.D.A.C. is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License,
# or (at your option) any later version.
#
# N.O.D.A.C. is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# Please refer to the GNU Public License for more details.
#
# You should have received a copy of the GNU Public License along with
# this program; if not, write to:
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
##

import libxml2
import array
from re import * 

network_types = ('feed-forward')
activation_types = ('linear', 'tanh', 'sigmoid')
config_version = 0

class NetRunner:
	def __init__(self, type, layers): # Set network type and layers
		if type in network_types:
			self.__type = type
		else:
			print "Error: unknown network type:", type
			exit()
			
		self.__layers = layers
		
		for layer in self.__layers:
			if not layer.has_key('activation'): 
				# make 'linear' standard value, if not specified
				layer['activation'] = 'linear'
			if not layer.has_key('neurons'):
				print "Error: no neurons number"
				exit()
		
		self.__mode = 0 # default: train		
		self.__sets = []
		self.__epochs = []
		self.__firstlayer = self.__layers[0]['neurons']
		self.__lastlayer = self.__layers[len(layers)-1]['neurons']
				
	def set_activation(self, nlayer, act_type): # Set layer activation type
		if act_type in activation_types:
			self.__layers[nlayer]['activation'] = act_type
			print "Layer", nlayer, "activation changed to:", act_type
		else:
			print "Error: unknown activation type:", act_type
			exit()
			
	def set_type(self, type): # Set network type
		if type in network_types:
			self.__type = type
			print "Network type changed to:", type
		else:
			print "Error: unknown network type:", type
			exit()
			
	def set_mode(self, mode): # Set running mode - 0 is 'train', 1 is 'test'
		if mode == 0 or mode == 1:
			self.__mode = mode
			print "Network mode changed to:", mode
		else:
			print "Error: invalid mode:", mode
			exit()
	
	def add_set(self): # Adds an empty set
		self.__sets.append([])
		self.__epochs.append(1000) # default for new sets is 1000
		
	def set_epochs(self, set, epochs): # Set training epochs for a given set
		if epochs > 0 and epochs < 65000: # TODO: change 65000 to unsigned int upper limit
			self.__epochs[set] = epochs
			print "Epochs for set", set, "changed to", epochs
		else:
			print "Error: epochs should be between 0 and 65000"
			exit()
			
	def add_entry(self, setn, input, output): # Adds a input/output pair in set setn
		if len(self.__sets) <= setn:
			print "Error: invalid set number:", setn
			print self.__sets
			exit()
		self.__sets[setn].append([input, output])
		
	def add_file(self, filename): # Read filename and add data to sets
		if len(self.__sets) == 0:
			self.add_set()
			self.__current = 0
		else:
			self.__current = len(self.__sets) - 1
		self.__separator = compile("-") # sets' separator
		fp = open(filename, "r")
		for line in fp:
			if match(self.__separator, line):
				self.add_set()
				self.__current += 1
				continue
			line = line.split()
			self.add_entry(self.__current, 
					line[0:self.__firstlayer], 
					line[(self.__firstlayer):(self.__firstlayer + self.__lastlayer)])
		fp.close()
	
	# TODO: readconfig()/writeconfig(), to read/write 
	# human-readable configuration files ;)
	
	def write_config():
		pass
		
	def read_config():
		pass
	
	def make_landscape(self, epochs=1000, N=0.5, M=0.1): # Run network
		print "Network type:", self.__type 
		for i in range(len(self.__layers)):
			print "Layer", i, "-"
			print "    Neurons:", self.__layers[i]['neurons']
			print "    Activation function:", self.__layers[i]['activation']
			
		print "Writing config file for", len(self.__sets),"sets..."
		
		self.__fp = open("landscape.nod", "wb")
		
		# HEADER section
		
		# header int values
		self.__header = array.array('I')
		self.__header.append(config_version)
		self.__header.append(len(self.__layers)-1)
		for layer in self.__layers:
			self.__header.append(layer['neurons'])
			for i in range(len(activation_types)):
				if activation_types[i] == layer['activation']:
					self.__header.append(i)
		print "INT part of header (layers, neurons number, act. functions, ...):"
		print self.__header
		
		# header weights values
		self.__headerw = array.array('f')
		self.__synapses = 0
		for i in range(len(self.__layers)-1): # synapses number
			self.__synapses += self.__layers[i]['neurons'] * self.__layers[i+1]['neurons']

		for i in range(self.__synapses): # add standard weights
			self.__headerw.append(1.0/self.__layers[0]['neurons'])
		
		print "DUMP part of header:"
		print self.__headerw
		
		# operating mode
		self.__opmode = array.array('I')
		self.__opmode.append(self.__mode)
		print "OPERATING MODE:"
		print self.__opmode
		
		# header float values	
		self.__headerfl = array.array('f')
		self.__headerfl.append(N)
		self.__headerfl.append(M)
		print "FLOAT part of header (learning rate, momentum):"
		print self.__headerfl
		
		# sets number
		self.__setsarr = array.array('I')
		self.__setsarr.append(len(self.__sets))
		print "SETS number:", self.__setsarr
		
		# print header to file
		self.__header.tofile(self.__fp)
		self.__headerw.tofile(self.__fp)
		self.__opmode.tofile(self.__fp)
		self.__headerfl.tofile(self.__fp)
		self.__setsarr.tofile(self.__fp)
		
		# DATA section
		
		print "DATA:"
		for set in self.__sets:
			self.__miniheader = array.array('I')
			self.__numarray = array.array('f')
			self.__miniheader.append(self.__epochs[self.__sets.index(set)])
			self.__miniheader.append(len(set))
			for case in set:
				for io in case:
					for num in io:
						self.__numarray.append(float(num))
			self.__miniheader.tofile(self.__fp)
			self.__numarray.tofile(self.__fp)
			print self.__miniheader
			print self.__numarray
		
		self.__fp.close()
		#########################################################
		# TODO: execute the network
		#########################################################
