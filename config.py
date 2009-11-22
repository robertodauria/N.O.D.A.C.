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

import array
import random
from re import * 
from xml.dom import minidom

activation_types = ('linear', 'tanh', 'sigmoid')
config_version = 0

class NeuralNetwork:
	def __init__(self): # Initialize the network
		self.__ready = False # Flag for ready-to-run network
		
		# Filled by "TO BE REPLACED" functions
		self.__sets = []
		self.__epochs = []
		self.__mode = 0 # default: train
		
		# Filled by new() or readconfig()
		self.__layers = []
		self.__weights = []
		
	def new(self, layers, wgen = 0): # New network from scratch
		self.__layers = layers
		for layer in self.__layers:
			if not layer.has_key('activation'): 
				# make 'linear' standard value, if not specified
				layer['activation'] = 'linear'
			if not layer.has_key('neurons'):
				print "Error: no neurons number specified"
				exit()
				
		self.__firstlayer = self.__layers[0]['neurons']
		self.__lastlayer = self.__layers[-1]['neurons']
		
		# Fill weights list
		nsyn = self.syncalc(self.__layers)
		for i in range(nsyn):
			if wgen == 0: # Weights generation type: 0 = random
				self.__weights.append(random.random())
			else:
				self.__weights.append(wgen)
		self.__ready = True
		
	def set_activation(self, nlayer, act_type): # Set layer activation type
		if act_type in activation_types:
			self.__layers[nlayer]['activation'] = act_type
			print "Layer", nlayer, "activation changed to:", act_type
		else:
			print "Error: unknown activation type:", act_type
			exit()
			
	def set_mode(self, mode): # Set running mode - 0 is 'train', 1 is 'test'
		if mode == 0 or mode == 1:
			self.__mode = mode
			print "Network mode changed to:", mode
		else:
			print "Error: invalid mode:", mode
			exit()
	
	def set_epochs(self, set, epochs): # Set training epochs for a given set
		if epochs > 0 and epochs < 65000: # TODO: change 65000 to unsigned int upper limit
			self.__epochs[set] = epochs
			print "Epochs for set", set, "changed to", epochs
		else:
			print "Error: epochs should be between 0 and 65000"
			exit()
			
	# --------------------------------------------
	# TODO: make a xml parser for dataset handling
	# --------------------------------------------
	def add_set(self): # Adds an empty set - TO BE REPLACED
		self.__sets.append([])
		self.__epochs.append(1000) # default for new sets is 1000

	def add_entry(self, setn, input, output): # Adds a input/output pair in set setn
	# - TO BE REPLACED
		if len(self.__sets) <= setn:
			print "Error: invalid set number:", setn
			print self.__sets
			exit()
		self.__sets[setn].append([input, output])
		
	def add_file(self, filename): # Read filename and add data to sets - TO BE REPLACED
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
	# --------------------------------------------
	
	def syncalc(self, layers): # Returns synapses number
		syn = 0
		for i in range(len(layers)-1): # synapses number
			syn += layers[i]['neurons'] * layers[i+1]['neurons']
		return syn

	def writeconfig(self, xmlfile):
		if self.__ready == False: # Network state check
			print "Why should I save an empty network?"
			return
		fp = open(xmlfile, "w")
		fp.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
		fp.write("<config>\n")
		fp.write("\t<version>" + str(config_version) + "</version>\n")
		for layer in self.__layers:
			fp.write("\t<layer>\n")
			fp.write("\t\t<size>" + str(layer['neurons']) + "</size>\n")
			fp.write("\t\t<activation>" + str(layer['activation']) + \
			"</activation>\n")
			fp.write("\t</layer>\n")
		fp.write("\t<weights>\n")
		for w in self.__weights:
			fp.write("\t\t<w>" + str(w) + "</w>\n")
		fp.write("\t</weights>\n")
		fp.write("</config>")
		fp.close()
		
	def readconfig(self, xmlfile):
		# temporary list - go to self.__layers if file is ok
		self.__templayers = []
		self.__isok = True # flag for correctness
		self.__config = minidom.parse(xmlfile).documentElement
		
		if int(self.__config.getElementsByTagName('version')[0].firstChild.data) \
		== config_version:
			print "Config version and program version match..."
			self.__nlayer = 0
			
			# Layer informations
			for layer in self.__config.getElementsByTagName('layer'):
				self.__templayers.append({})

				if len(layer.getElementsByTagName('size')) != 0:
					self.__templayers[self.__nlayer]['neurons'] = \
					int(layer.getElementsByTagName('size')[0].firstChild.data.encode('UTF-8'))
				else:
					print "Error in config file: missing layer size."
					self.__isok = False
					
				if len(layer.getElementsByTagName('activation')) != 0:
					self.__templayers[self.__nlayer]['activation'] = \
					layer.getElementsByTagName('activation')[0].\
					firstChild.data.encode('UTF-8')
				else:
					print "Setting default activation for layer", \
					self.__nlayer
					self.__templayers[self.__nlayer]['activation'] = \
					'linear' # default
				
				
				self.__nlayer = self.__nlayer + 1
			
			# Weights informations
			self.__tempweights = []
			self.__nweight = 0
			
			self.__synapses = self.syncalc(self.__templayers)
			print "Synapses number:", self.__synapses
			
			# Get weights
			for w in self.__config.getElementsByTagName('w'):
				self.__tempweights.append(1)
				self.__tempweights[self.__nweight] = float\
				(w.firstChild.data.encode('UTF-8'))
				self.__nweight = self.__nweight + 1
			if len(self.__tempweights) != self.__synapses:
				print "Error: Weights number doesn't match synapses number"
				self.__isok = False
				
			print "Temporary weights list:"
			print self.__tempweights
				
			print "Temporary layer list:"
			print self.__templayers
			if self.__isok:
				print "Updating layers..."
				self.__layers = self.__templayers
				self.__firstlayer = self.__layers[0]['neurons']
				self.__lastlayer = self.__layers[-1]['neurons']
				print "Updating weights..."
				self.__weights = self.__tempweights
				self.__ready = True
			else:
				print "One or more errors in config file."
				
	def make_landscape(self, N=0.5, M=0.1): # Run network
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
		for w in self.__weights:
			self.__headerw.append(w)
		
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
