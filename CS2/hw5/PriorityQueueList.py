# Priority Queue Abstract Data Type implemented with Python lists

class PriorityQueueList:
    def __init__(self):
        self.contents = []

    def insert(self, item):
        """ inserts item into the priority queue """
        self.contents.append(item)
        
    def deleteMin(self):
        """ removes minimum item from the priority queue and returns it. 
        returns None if the priority queue is empty. """
        if self.contents == []: return None
        else:
            smallestItem = min(self.contents)
            self.contents.remove(smallestItem)
            return smallestItem