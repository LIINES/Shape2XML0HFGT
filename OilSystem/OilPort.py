#!/usr/bin/python3
"""
Copyright (c) 2018-2023 Laboratory for Intelligent Integrated Networks of Engineering Systems
@author: Dakota J. Thompson, Amro M. Farid
@lab: Laboratory for Intelligent Integrated Networks of Engineering Systems
@Modified: 09/29/2023
"""

from ElectricGrid.ElectricNode import ElectricNode
# from lxml import etree as ET
import xml.etree.ElementTree as ET
from collections import OrderedDict


class OilPort(ElectricNode):
	"""
	This class represents all power systems controllable generators.

	Attributes:
		portNum     terminal number (positive integer)
		portName    generator name
		portClass   terminal class
		status      machine status, >0 = machine in-service, 0 = machine out-of-service
		maxOil      maximum processed oil output
		minOil      minimum processed oil output
		fuelType    fuel type of output

	"""

	def __init__(self):
		"""
		This class creates an instance of the oilPort class with each attribute set to none type.
		"""
		ElectricNode.__init__(self)
		self.nodeType = self.__class__.__name__
		self.nodeName = None
		self.portName = None
		self.portClass = None
		self.portNum = None
		self.maxOil = None
		self.minOil = None
		self.fuelType = None
		self.status = None
		self.controller = []


	def add_xml_child_hfgt(self,parent):
		"""
		This creates an XML branch for the port object with functionality.
		"""

		machine = ET.SubElement(parent, 'Machine', OrderedDict([('name', self.nodeName), ('gpsX', str(self.gpsX)), ('gpsY', str(self.gpsY)),('controller',', '.join(self.controller))]))
		method_form = ET.SubElement(machine, 'MethodxForm', OrderedDict([('name', 'import crude oil'), ('operand',''),('output', 'crude oil'), ('status',self.status)]))
		method_form = ET.SubElement(machine, 'MethodxForm', OrderedDict([('name', 'export crude oil'), ('operand','crude oil'),('output', ''), ('status',self.status)]))
		method_form = ET.SubElement(machine, 'MethodxForm', OrderedDict([('name', 'import processed oil'), ('operand',''),('output', 'processed oil'), ('status',self.status)]))
		method_form = ET.SubElement(machine, 'MethodxForm', OrderedDict([('name', 'export processed oil'), ('operand','processed oil'),('output', ''), ('status',self.status)]))
		method_port = ET.SubElement(machine, 'MethodxPort', OrderedDict([('name', 'store'), ('operand', 'processed oil'), ('output', 'processed oil'),('origin', self.nodeName), ('dest', self.nodeName), ('ref', 'processed oil'),('status', self.status)]))


	def add_xml_child_hfgt_dofs(self, parent, resourceCount, resourceIdx):
		"""
		This creates an XML branch for the port object with functionality.
		"""
		resource = resourceCount[0]
		method_form = ET.SubElement(parent, 'MethodxForm', OrderedDict(
			[('resource', str(resource)), ('gpsX', str(self.gpsX)), ('gpsY', str(self.gpsY)),
			 ('name', 'import crude oil'), ('operand', ''), ('output', 'crude oil'), ('status', self.status),('controller',', '.join(self.controller))]))
		method_form = ET.SubElement(parent, 'MethodxForm', OrderedDict(
			[('resource', str(resource)), ('gpsX', str(self.gpsX)), ('gpsY', str(self.gpsY)),
			 ('name', 'export crude oil'), ('operand', 'crude oil'), ('output', ''), ('status', self.status),('controller',', '.join(self.controller))]))
		method_form = ET.SubElement(parent, 'MethodxForm', OrderedDict(
			[('resource', str(resource)), ('gpsX', str(self.gpsX)), ('gpsY', str(self.gpsY)),
			 ('name', 'import processed oil'), ('operand', ''), ('output', 'processed oil'),
			 ('status', self.status),('controller',', '.join(self.controller))]))
		method_form = ET.SubElement(parent, 'MethodxForm', OrderedDict(
			[('resource', str(resource)), ('gpsX', str(self.gpsX)), ('gpsY', str(self.gpsY)),
			 ('name', 'export processed oil'), ('operand', 'processed oil'), ('output', ''),
			 ('status', self.status),('controller',', '.join(self.controller))]))
		method_port = ET.SubElement(parent, 'MethodxPort', OrderedDict(
			[('resource', str(resource)), ('gpsX', str(self.gpsX)), ('gpsY', str(self.gpsY)), ('name', 'store'),
			 ('operand', 'processed oil'), ('output', 'processed oil'),
			 ('origin', str(resource)), ('dest', str(resource)), ('ref', 'processed oil'),
			 ('status', self.status), ('controller', ', '.join(self.controller))]))

		resourceCount[0] += 1
		resourceIdx[self.nodeName] = resource
		return resourceCount, resourceIdx