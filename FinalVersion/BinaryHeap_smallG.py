class MinBinaryHeap_smallG:
	def __init__(self):
		self.__heap = []
		self.__last_index = -1

	def __len__(self):
		return self.__last_index + 1

	def cleanup_heap(self):
		self.__heap = []
		self.__last_index = -1

	def push(self, node):
		self.__last_index += 1
		self.__heap.append(node)
		self.__siftup(self.__last_index)

	def __siftup(self, index):
		while index > 0:
			parent_index, parent_node = self.__get_parent(index)
			# use small-G to break ties
			if parent_node.f < self.__heap[index].f:
				break
			elif (parent_node.f == self.__heap[index].f) and (parent_node.g <= self.__heap[index].g):
				break
			self.__swap(parent_index, index)
			index = parent_index

	def __get_parent(self, index):
		if index == 0:
			return None, None
		parent_index = int((index - 1) / 2)
		return parent_index, self.__heap[parent_index]

	def __swap(self, i, j):
		temp = self.__heap[i]
		self.__heap[i] = self.__heap[j]
		self.__heap[j] = temp

	def get_min_node(self):
		if self.__last_index == -1:
			return None
		return self.__heap[0]

	def pop(self):
		if self.__last_index == -1:
			return None
		min_node = self.__heap[0]
		self.__heap[0] = self.__heap[self.__last_index]
		self.__heap.pop(self.__last_index)
		self.__last_index -= 1
		if self.__last_index > 0:
			self.__siftdown(0)
		return min_node

	def __siftdown(self, index):
		while (index >= 0) and (index <= self.__last_index):
			index_node = self.__heap[index]
			left_child_index, left_child_node = self.__get_left_child(index, index_node)
			right_child_index, right_child_node = self.__get_right_child(index, index_node)
			left_child_is_less = 0
			if left_child_index and \
				((index_node.f > left_child_node.f) or ((index_node.f == left_child_node.f) and (index_node.g > left_child_node.g))):
				left_child_is_less = 1
			right_child_is_less = 0
			if right_child_index and \
				((index_node.f > right_child_node.f) or ((index_node.f == right_child_node.f) and (index_node.g > right_child_node.g))):
				right_child_is_less = 1
			if left_child_is_less == 0 and right_child_is_less == 0:
				break
			if left_child_is_less == 1 and right_child_is_less == 0:
				new_index = left_child_index
				self.__swap(index, left_child_index)
				index = new_index
			elif left_child_is_less == 0 and right_child_is_less == 1:
				new_index = right_child_index
				self.__swap(index, right_child_index)
				index = new_index
			elif left_child_is_less == 1 and right_child_is_less == 1:
				if (left_child_node.f < right_child_node.f) or ((left_child_node.f == right_child_node.f) and (left_child_node.g < right_child_node.g)):
					new_index = left_child_index
					self.__swap(index, left_child_index)
					index = new_index
				else:
					new_index = right_child_index
					self.__swap(index, right_child_index)
					index = new_index

	def __get_left_child(self, index, default_value):
		left_child_index = 2 * index + 1
		if left_child_index > self.__last_index:
			return None, default_value
		return left_child_index, self.__heap[left_child_index]

	def __get_right_child(self, index, default_value):
		right_child_index = 2 * index + 2
		if right_child_index > self.__last_index:
			return None, default_value
		return right_child_index, self.__heap[right_child_index]

	def find_node(self, node):
		for i in range(len(self.__heap)):
			if self.__heap[i] == node:
				return i, self.__heap[i]
		return None, None

	def remove_element(self, index):
		if (self.__last_index == -1) or (index > self.__last_index):
			return
		if index == self.__last_index:
			self.__heap.pop(self.__last_index)
			self.__last_index -= 1
			return
		self.__swap(index, self.__last_index)
		self.__heap.pop(self.__last_index)
		self.__last_index -= 1
		parent_index, parent_node = self.__get_parent(index)
		if parent_index:
			if (parent_node.f > self.__heap[index].f) or ((parent_node.f == self.__heap[index].f) and (parent_node.g > self.__heap[index].g)):
				self.__siftup(index)
			else:
				self.__siftdown(index)

