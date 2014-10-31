#########################################################################
# Solves Sudoku puzzles. The input must be a .csv file with 9 lines, each
# containing 9 comma-seperated digits. "0" represents an empty field.
#
# Run by typing "python SudokuSolver.py" in the command line. It will ask
# you to specify the name of the input file.
#
# The output is stored in the file "solution.csv".
#
# Samuel Hertig
# sam.hertig@gmail.com
#########################################################################

class Board:

	"""
	Represents a configuration of the 81 fields. Intances of
	this class are being passed around in the list "boards".
	"""

	def __init__(self, recursiondepth, fields):
		self.fields = fields # A list of 81 lists. If a sublist has only one element, the field is known. 
		self.recursiondepth = recursiondepth # An integer indicating how many guesses have been made (a.k.a backtracking)
		self.haswrongguess = False # This attribute is set to True when we know that a wrong guess has been made
		self.progress = True # This informs us about whether we made progress eliminating values analytically (w/o guessing)

	def optimize(self):
		""" This methods tries to eliminate possible values analytically (without guessing). """
		while self.progress:
			while self.progress:
				self.findallowed()
				if self.haswrongguess:
					return
			self.narrowdown()
		
	def findallowed(self):
		""" Finds allowed values of fields and detects a guess that led to an impossible configuration. """
		allvalues = set(range(1,10))
		for i, f in enumerate(self.fields):
			if len(f) > 1:
				allneighbors = rowmembers(i) + columnmembers(i) + squaremembers(i)
				neighborvalues = set()
				for j in allneighbors:
					if len(self.fields[j]) == 1:
						neighborvalues.add(self.fields[j][0])
				allowedvalues = list(allvalues - neighborvalues)
				if len(allowedvalues) == 0:					
					self.haswrongguess = True
					return
				self.fields[i] = allowedvalues
				if len(allowedvalues) == 1:
					self.progress = True
					return
		self.progress = False			
		
	def narrowdown(self):
		""" Eliminates possible values of fields analytically by applying the basic Sudoku rules. """
		from collections import Counter
		# Check rows:
		for i in range(0,9):
			allvalues = []
			for j in range(0,9):
				if len(self.fields[i*9+j]) > 1:
					allvalues = allvalues + self.fields[i*9+j]
			histo = Counter(allvalues)		
			uniquevalues = [key for key,value in histo.items() if value==1]
			for v in uniquevalues:
				for j in range(0,9):
					if v in self.fields[i*9+j]:
						self.fields[i*9+j] = [v]
						self.progress = True
						return
		# Check columns:
		for i in range(0,9):
			# gather all values
			allvalues = []
			for j in range(0,81,9):
				if len(self.fields[i+j]) > 1:
					allvalues = allvalues + self.fields[i+j]
			histo = Counter(allvalues)		
			uniquevalues = [key for key,value in histo.items() if value==1]
			for v in uniquevalues:
				for j in range(0,81,9):
					if v in self.fields[i+j]:
						self.fields[i+j] = [v]
						self.progress = True
						return
		# Check 3x3 squares:	
		for i in [0,3,6,27,30,33,54,57,60]:
			allvalues = []
			indices = squaremembers(i)+[i]		
			for k in indices:
				if len(self.fields[k]) > 1:
					allvalues = allvalues + self.fields[k]
			histo = Counter(allvalues)		
			uniquevalues = [key for key,value in histo.items() if value==1]
			for v in uniquevalues:
				for k in indices:
					if v in self.fields[k]:
						self.fields[k] = [v]
						self.progress = True
						return
		self.progress = False						

	def wins(self):
		""" If all 81 fields have a single value, we are done. """
		badfields = [f for f in self.fields if len(f) > 1]
		return len(badfields) == 0

	def output(self):
		""" Writes the board to an output file. """
		fout = open('solution.csv', 'w')
		for i in range(10):
			line = [f[0] for f in self.fields[i*9:9+i*9]]
			line = ','.join(map(str, line)) + '\n'
			fout.write(line)
		fout.close()

	def sanitycheck(self):
		""" Used to check the initial board and for debugging. """
		for i in range(81): # checking some areas more than once, but that's ok
			rowvalues = [self.fields[i][0] for i in rowmembers(i)+[i] if len(self.fields[i])==1]
			if len(rowvalues) != len(set(rowvalues)):
				print "Error: numbers appear in row %d more than once." % ((i/9) + 1)
				return False
			colvalues = [self.fields[i][0] for i in columnmembers(i)+[i] if len(self.fields[i])==1]
			if len(colvalues) != len(set(colvalues)):
				print "Error: numbers appears in column %d more than once." % (i + 1)
				return False
			squarevalues = [self.fields[i][0] for i in squaremembers(i)+[i] if len(self.fields[i])==1]
			if len(squarevalues) != len(set(squarevalues)):
				print "Error: numbers appear in a 3x3 square more than once."
				return False		
		return self


def rowmembers(i):
	""" Finds field indices of the same row as i. """
	rownr = i/9
	neighbors = [j+rownr*9 for j in range(0,9)]
	neighbors.remove(i)
	return neighbors

def columnmembers(i):
	""" Finds field indices of the same column as i. """
	columnnr = i%9
	neighbors = range(0+columnnr,81+columnnr,9)
	neighbors.remove(i)
	return neighbors

def squaremembers(k):
	""" Finds field indices of the same 3x3 subsquare as i. Yes, one line is rather ugly... """
	j = k/27
	i = (k%9)/3
	neighbors = [0+i*3+j*27,1+i*3+j*27,2+i*3+j*27,9+i*3+j*27,10+i*3+j*27,11+i*3+j*27,18+i*3+j*27,19+i*3+j*27,20+i*3+j*27]
	neighbors.remove(k)
	return neighbors

def createguessedboards(b):
	"""
	If we don't make any progress with the optimize() method,
	we need to make a guess and create N new boards, where N
	is the number of options we have for the first field of 
	board b that had more than one possible value.
	"""
	newboards = []
	newrecdepth = b.recursiondepth + 1
	for i,f in enumerate(b.fields):
		choices = len(f)
		if choices > 1:
			for c in range(choices):
				newboard = Board(newrecdepth, b.fields[:])
				newboard.fields[i] = [f[c]][:]
				newboards.append(newboard)				
			return newboards			

def finddeepestboards(boards):
	"""
	Finds the boards with the highest recursion depth, i.e.
	those that contain the highest number of guesses.
	"""
	maxrnum = max([b.recursiondepth for b in boards])
	return [b for b in boards if b.recursiondepth == maxrnum]

def solve(boards):
	"""
	This is our main recursive routine for finding the solution.
	"""
	validboards = [b for b in boards if not b.haswrongguess]	
	currentboards = finddeepestboards(validboards) # these are the boards we need to explore
	for b in currentboards:
		b.optimize() # try to find a solution without guessing
		if not b.haswrongguess:	
			if b.wins():
				print "Solution found (recursion depth: %d)." % (b.recursiondepth)
				b.output()
				return True
			else: 
				newboards = createguessedboards(b) # make a guess and create new boards			
				boards += newboards
				if solve(boards): # recursive call
					return True		
	return False			

def createinitialboard(filename):
	"""
	Reads in the file and creates the initial board. Runs a
	sanity check to detect violations in the input puzzle.
	"""
	fin = open(filename, 'r')
	fields = []
	for line in fin:
		row = line.strip('\n').split(',')
		fields = fields + row
	# replace the zeros with a field with all 9 options
	for i, f in enumerate(fields):
		if f == '0':
			fields[i] = range(1,10) 
		else:
			fields[i] = [int(f)]	
	b = Board(0, fields)
	fin.close()
	return b.sanitycheck()
	
def main():
	"""
	The highest-level routine that calls createinitialboard() and solve().
	"""
	filename = raw_input('Please enter the filename of your (least) favorite Sudoku puzzle:\n')
	b = createinitialboard(filename)
	if not b:
		print "Not a valid input puzzle."
		return
	boards = []	
	boards.append(b)
	if not solve(boards):
		print "Failed to find a valid solution."

if __name__ == '__main__':
	main()	