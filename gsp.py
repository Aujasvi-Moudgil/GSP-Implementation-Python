import os
import codecs
import itertools
import operator

class GSP:
	'''GSP algorithm implementation'''
	def __init__(self, min_sup, path):
		self.min_sup = min_sup
		self.path = path
		self.unique_words, self.word_list, self.data = self.parse_data()
		self.items = {}
		self.num_users = len(self.data)

	def parse_data(self):
		files = os.listdir(self.path)
		files = [self.path + file for file in files]
		unique_words = {} # contains unique words in the data files
		unique_counter = 0 # ID number assigned to each unique word
		seqs = []
		word_list = []

		for filename in files:
			# read user data
			lines = []
			f = codecs.open(filename, encoding='utf-8')
			for line in f:
				lines.append(line.encode('utf-8'))
			ans = {} # contains final time series dictionary
			seq = {}
			seq['file'] = filename
			s1 = []
			s2 = []
			# for each line in data file
			for X in lines:
				Y = X.strip().split(';')
				time = Y[0].split(' ')[1]
				# extract time info
				x = []

				# extract useful info at a given time stamp
				for i,data in enumerate(Y):
					if i > 0: 
						word = data.split('#')[1]

						# check if word is unique or not
						# if not, assign a new ID number
						if word not in unique_words:
							unique_counter = unique_counter + 1
							unique_words[word] = unique_counter
							word_list.append(word)
						x.append(unique_words[word])
				# if x is not empty
				if x:
					ans[time] = x
					s1.extend(x)
					s2.append(tuple(x))
			seq['data'] = ans
			seq['seq_individual'] = s1
			seq['seq_combined'] = s2
			seqs.append(seq)

		return unique_words, word_list, seqs

	def is_subseq(self, x, y):
		it = iter(y)
		return all(c in it for c in x)


	def find_support(self, item, flag):
		count = 0
		if flag == 1:
			for i in range(self.num_users):
				if self.is_subseq(item, self.data[i]['seq_individual']):
					count += 1
		else:
			for i in range(self.num_users):
				if item in self.data[i]['seq_combined']:
					count += 1
		return count


	def get_support_items(self, level):
		# Step 1: Find items that meet min. threshold requirement
		print('Number of users = %d' % (self.num_users))
		for word in self.unique_words:
			l = [self.unique_words[word]]
			sup = self.find_support(l, 1)
			if sup >= self.min_sup:
				self.items[tuple(l)] = sup

		# If we need only 1-grams, we print those here and exit.
		if level == 1:
			sorted_patterns = sorted(self.items.items(), key=operator.itemgetter(1), reverse=True)
			for t in sorted_patterns:
				p = []
				for i in t[0]:
					print self.word_list[i - 1] + ' ', 
				print t[1]
			return

		# We now generate permutations of size 2.
		keys = [x[0] for x in self.items.keys()]
		perms = itertools.permutations(keys, 2)
		self.perms = list(perms)

		self.items = {}

		'''for p in self.perms:
			sup = self.find_support(p, 2)
			if sup >= self.min_sup:
				self.items[(p, )] = sup'''

		for k in keys:
			self.perms.append((k, k))	

		for p in self.perms:
			sup = self.find_support(list(p), 1)
			if sup >= self.min_sup:
				self.items[p] = sup

		level -= 2 # processing done till level 2

		# processing for level > 2
		while level > 0:
			prev_items = dict(self.items)
			self.items = {}
			for item in prev_items:
				for k in self.unique_words:
					key = list(item)
					key.append(self.unique_words[k])
					key = tuple(key)
					sup = self.find_support(list(key), 1)
					if sup >= self.min_sup:
						self.items[key] = sup
			level -= 1

		sorted_patterns = sorted(self.items.items(), key=operator.itemgetter(1), reverse=True)


		for t in sorted_patterns:
			p = []
			for i in t[0]:
				print self.word_list[i - 1] + ' ',
			print t[1]

		return
			
