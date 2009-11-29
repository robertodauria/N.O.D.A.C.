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
dataset_version = 0

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
		print self.__layers
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
		if epochs > 0 and epochs < 4294967295: 
			self.__epochs[set] = epochs
			print "Epochs for set", set, "changed to", epochs
		else:
			print "Error: epochs should be between 0 and 65000"
			exit()
			
	def add_set(self): # Adds an empty set
		self.__sets.append([])
		self.__epochs.append(1000) # default for new sets is 1000

	def add_entry(self, setn, inputs, outputs): # Adds a input/output pair in set setn
		if len(self.__sets) <= setn:
			print "Error: invalid set number:", setn
			exit()
		self.__sets[setn].append([inputs, outputs])
	
	def read_dataset(self, xmlfile): # Read datasets from XML
		tempsets = []
		tempepochs = []
		isok = True # flag for correctness
		currentset = 0
		dataset = minidom.parse(xmlfile).documentElement
		if int(dataset.getElementsByTagName('version')[0].firstChild.data) \
		== dataset_version:
			print "Dataset version and program version match..."
			for set in dataset.getElementsByTagName('set'):
				tempsets.append([])
				setepochs = set.getElementsByTagName('epochs')
				
				if not setepochs:
					tempepochs.append(1000)
				else:
					tempepochs.append(int(setepochs[0].firstChild.data.\
					encode('UTF-8')))
				
				for case in set.getElementsByTagName('case'):
					inputs = []
					outputs = []
					for i in case.getElementsByTagName('i'):
						inputs.append(i.firstChild.data.encode('UTF-8'))
					for o in case.getElementsByTagName('o'):
						outputs.append(o.firstChild.data.encode('UTF-8'))
					tempsets[currentset].append([inputs, outputs])
					
					# At this point I should already have 
					# the network structure...
					if len(inputs) != self.__firstlayer or \
					len(outputs) != self.__lastlayer:
						isok = False
						print \
						"Error: I/O elements doesn't match layers size"
					
					
				currentset += 1
				
			print tempsets
			print tempepochs
			if isok:
				print "Updating sets..."
				self.__sets = tempsets
				print "Updating epochs..."
				self.__epochs = tempepochs
			else:
				print "One or more errors in dataset"
	
	def syncalc(self, layers): # Returns synapses number
		syn = 0
		for i in range(len(layers)-1): # synapses number
			syn += layers[i]['neurons'] * layers[i+1]['neurons']
		return syn

	def write_config(self, xmlfile): # write a XML configuration file
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
		
	def read_config(self, xmlfile): # read a XML configuration file
		templayers = []
		isok = True # flag for correctness
		config = minidom.parse(xmlfile).documentElement
		
		if int(config.getElementsByTagName('version')[0].firstChild.data) \
		== config_version:
			print "Config version and program version match..."
			nlayer = 0
			
			# Layer informations
			for layer in config.getElementsByTagName('layer'):
				templayers.append({})

				if len(layer.getElementsByTagName('size')) != 0:
					templayers[nlayer]['neurons'] = \
					int(layer.getElementsByTagName('size')[0].firstChild.data.encode('UTF-8'))
				else:
					print "Error in config file: missing layer size."
					isok = False
					
				if len(layer.getElementsByTagName('activation')) != 0:
					templayers[nlayer]['activation'] = \
					layer.getElementsByTagName('activation')[0].\
					firstChild.data.encode('UTF-8')
				else:
					print "Setting default activation for layer", nlayer
					templayers[nlayer]['activation'] = \
					'linear' # default
				
				
				nlayer += 1
			
			# Weights informations
			tempweights = []
			nweight = 0
			
			synapses = self.syncalc(templayers)
			print "Synapses number:", synapses
			
			# Get weights
			for w in config.getElementsByTagName('w'):
				tempweights.append(1)
				tempweights[nweight] = float\
				(w.firstChild.data.encode('UTF-8'))
				nweight = nweight + 1
			if len(tempweights) != synapses:
				print "Error: Weights number doesn't match synapses number"
				isok = False
				
			print "Temporary weights list:"
			print tempweights
				
			print "Temporary layer list:"
			print templayers
			if isok:
				print "Updating layers..."
				self.__layers = templayers
				self.__firstlayer = self.__layers[0]['neurons']
				self.__lastlayer = self.__layers[-1]['neurons']
				print "Updating weights..."
				self.__weights = tempweights
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
		n = 0
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
