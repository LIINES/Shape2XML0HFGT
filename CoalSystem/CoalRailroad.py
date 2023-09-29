"""
Copyright (c) 2018-2023 Laboratory for Intelligent Integrated Networks of Engineering Systems
@author: Dakota J. Thompson, Amro M. Farid
@lab: Laboratory for Intelligent Integrated Networks of Engineering Systems
@Modified: 09/29/2023
"""

import numpy as np
import xml.etree.ElementTree as ET
from collections import OrderedDict

class CoalRailroad(object):
	"""
		This class represents all coal systems controllable railroads.

		Attributes:
			name     		railroad name
			type    		type of object
			fBus   			origin of railroad
			tBus   			destination of railroad
			maxCoal     	maximum coal output
			minCoal     	minimum coal output
			lineName		railroad name
			refinement		refinement of line
			fuelType    	fuel source dealt with
			status      	machine status, >0 = machine in-service, 0 = machine out-of-service
			cluster			Cluster node belongs too
			coordinate		coordinates of line
			clust_origin	cluster of railroad origin
			clust_dest		cluster of railroad destination
			joined			railroads joined together when cleaning
		"""
	def __init__(self):
		"""
		Construct a new railroad with all parameters set to none type
		"""
		self.name = 'Coal Railroad'
		self.type = 'CoalRailroad'
		self.fBus = None
		self.tBus = None
		self.maxCoal = None
		self.minCoal = None
		self.lineName = None
		self.refinement = None
		self.fuelType = None
		self.status = None

		self.coordinate = None
		self.clust_origin = ''
		self.clust_dest = ''
		self.joined = set()
		self.controller = []

	def __repr__(self):
		"""
		This function is used to print your class attributes for easy visualization.
		:return: it returns the printed class with its attributes and values listed as a dictionary.

		>> This function is called as follows:
		>> print(self)
		"""
		from pprint import pformat
		return pformat(vars(self), indent=4, width=1)

	def get_status(self):
		return self.status

	def get_origin(self):
		return self.fBus

	def get_dest(self):
		return self.tBus

	def add_xml_child_hfgt(self, parent):
		"""
		This creates an XML branch for the railroad object with functionality.
		"""

		transporter = ET.SubElement(parent, 'Transporter', OrderedDict([('name', self.lineName), ('controller',', '.join(self.controller))]))
		for k1 in self.refinement:
			method_port1 = ET.SubElement(transporter, 'MethodxPort', OrderedDict([('name', 'transport'), ('status', 'true'), ('origin', self.fBus), ('dest', self.tBus), ('operand',k1), ('output',k1), ('ref', k1)]))
			method_port2 = ET.SubElement(transporter, 'MethodxPort', OrderedDict([('name', 'transport'), ('status', 'true'), ('origin', self.tBus), ('dest', self.fBus), ('operand',k1), ('output',k1), ('ref', k1)]))

	def add_xml_child_hfgt_dofs(self, parent, resourceCount, resourceIdx):
		"""
		This creates an XML branch for the railroad object with functionality.
		"""
		resource = sum(resourceCount)
		for k1 in self.refinement:
			method_port1 = ET.SubElement(parent, 'MethodxPort', OrderedDict(
				[('resource', str(resource)), ('name', 'transport'), ('status', 'true'), ('origin', str(resourceIdx[self.fBus])), ('dest', str(resourceIdx[self.tBus])), ('operand', k1),
				 ('output', k1), ('ref', k1), ('controller',', '.join(self.controller))]))
			method_port2 = ET.SubElement(parent, 'MethodxPort', OrderedDict(
				[('resource', str(resource)), ('name', 'transport'), ('status', 'true'), ('origin', str(resourceIdx[self.tBus])), ('dest', str(resourceIdx[self.fBus])), ('operand', k1),
				 ('output', k1), ('ref', k1), ('controller',', '.join(self.controller))]))
		resourceCount[2] += 1
		resourceIdx[self.lineName] = resource
		return resourceCount