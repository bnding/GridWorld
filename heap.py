class MinHeap:
	def __init__(self):
		self.heap = []

	def insert(self, key):
		self.heap.append(key)
		self.siftup(len(self.heap) - 1)

	def siftup(self, i):
		length = len(self.heap)
		while(self.hasParent(i) and self.heap[i] < self.heap[self.getParent(i)]):
			self.swap(i, self.getParent(i))
			i = self.getParent(i)

	def getParent(self, i):
		return int((i - 1) / 2)

	def hasParent(self, i):
		return self.getParent(i) >= 0

	def swap(self, i, j):
		temp = self.heap[i]
		self.heap[i] = self.heap[j]
		self.heap[j] = temp

	def deleteRoot(self):
		length = len(self.heap)
		if length == 0:
			return -1
		lastElement = length - 1
		self.swap(0, lastElement)
		root = self.heap.pop()
		self.siftDown(0)
		return root

	def siftDown(self, i):
		while(self.hasLeftChild(i)):
			maxChildIndex = self.getMaxChildIndex(i)
			if(maxChildIndex == -1):
				break
			if(self.heap[maxChildIndex] < self.heap[i]):
				self.swap(i, maxChildIndex)
				i = maxChildIndex
			else:
				break

	def getMaxChildIndex(self, i):
		if(self.hasLeftChild(i)):
			leftChild = self.getLeftChild(i)
			if(self.hasRightChild(i)):
				rightChild = self.getRightChild(i)
				if(self.heap[leftChild] < self.heap[rightChild]):
					return leftChild
				else:
					return rightChild
		else:
			return 

	def printHeap(self):
		print(self.heap)

	def getLeftChild(self, i):
		return 2 * i + 1

	def getRightChild(self, i):
		return 2 * i + 2

	def hasRightChild(self, i):
		return self.getRightChild(i) < len(self.heap)

	def hasLeftChild(self, i):
		return self.getLeftChild(i) < len(self.heap)

minHeap = MinHeap()
array = [45, 99, 63, 27, 29, 57, 42, 35, 12, 24]

for i in array:
	minHeap.insert(i)

minHeap.printHeap()