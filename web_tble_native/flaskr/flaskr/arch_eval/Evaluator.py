import numpy
import json
import csv
import sys

class Evaluator(object):
	"""docstring for Evaluator"""
	def __init__(self):
		super(Evaluator, self).__init__()
		self.points = []
		with open('docs/raw_combined_data.csv', 'rt') as csvfile:
			data = csv.reader(csvfile, delimiter = ',')
			next(data)
			for row in data:
				self.points.append(row)

		self.cache = {}
		for i in range(61):
			self.cache[i] = []

		for point in self.points:
			num_instr = sum([int(val) for val in list(point[0])])
			self.cache[num_instr].append(point)

		estimation_params = json.load(open('docs/model_params.json'))
		self.science_i = estimation_params["science_i"]
		self.science_w = numpy.array(estimation_params["science_w"], dtype = float)
		self.cost_i = estimation_params["cost_i"]
		self.cost_w = numpy.array(estimation_params["cost_w"], dtype = float)


	def eval_arch(self, bitString):
		cache_cost, cache_science = self.searchCache(bitString)
		if cache_science != None and cache_cost != None:
			return (float(cache_cost),float(cache_science), False)
		else:
			bs_vect = numpy.array(list(bitString), dtype = float)
			science = numpy.dot(bs_vect.T, self.science_w) + self.science_i
			cost = numpy.dot(bs_vect.T, self.cost_w) + self.cost_i
			return(cost, science, True)


	def searchCache(self, bitString):
		instr_count = sum([int(val) for val in list(bitString)])
		sub_points = self.cache[instr_count]
		for point in sub_points:
			if Evaluator.compArchs(point[0], bitString):
				return (point[2], point[1])
		return (None, None)

	@staticmethod
	def compArchs(arch1, arch2):
		return str(arch1) == str(arch2)