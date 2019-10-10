from Node import *

class MinHeap:
	def __init__(self):
		self.heap = []

	def insert(self, node):
		self.heap.append(node)
		self.siftUp(len(self.heap) - 1)

	def siftUp(self, i):
		length = len(self.heap)
		while(self.hasParent(i) and self.heap[i].f < self.heap[self.getParent(i)].f):
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
			if(self.heap[maxChildIndex].f < self.heap[i].f):
				self.swap(i, maxChildIndex)
				i = maxChildIndex
			else:
				break

	def getMaxChildIndex(self, i):
		if(self.hasLeftChild(i)):
			leftChild = self.getLeftChild(i)
			if(self.hasRightChild(i)):
				rightChild = self.getRightChild(i)
				if(self.heap[leftChild].f < self.heap[rightChild].f):
					return leftChild
				else:
					return rightChild
		else:
			return 

	def removeElement(self, target):
		i = 0
		for elements in self.heap:
			if elements == target:
				self.swap(i, len(self.heap)-1)
				self.heap.remove(self.heap[len(self.heap)-1])
				if self.getParent(i) <= self.heap[i].f:
					self.siftUp(i)
				else:
					self.siftDown
				i = i+1

	def findGValue(self, val):
		i = 0
		for x in self.heap:
			if self.heap[i].g == val:
				return self.heap[x]
			i = i+1

	def findState(self, state):
		i = 0
		for x in self.heap:
			if self.heap[i].position == state:
				return self.heap[x]
			i = i+1

	def printHeap(self):
		i = 0
		for x in self.heap:
			print(self.heap[i].f, end = ' ')
			i = i+1
		print()

	def getLeftChild(self, i):
		return 2 * i + 1

	def getRightChild(self, i):
		return 2 * i + 2

	def hasRightChild(self, i):
		return self.getRightChild(i) < len(self.heap)

	def hasLeftChild(self, i):
		return self.getLeftChild(i) < len(self.heap)

minHeap = MinHeap()
node = Node(None, None)
node.g = 54
node.h = 30
node.f = 20
node2 = Node(None, None)
node2.g = 30
node2.h = 18
node2.f = 56
#array = [45, 99, 63, 27, 29, 57, 42, 35, 12, 24]

# for i in array:
# 	minHeap.insert(i)

minHeap.insert(node)
minHeap.insert(node2)

minHeap.printHeap()
minHeap.deleteRoot()
minHeap.printHeap()
# minHeap.removeElement(29)
# minHeap.printHeap()
# minHeap.removeElement(24)
# minHeap.printHeap()
