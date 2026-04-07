import os 
import functools
import sys
import readchar
from readchar import key

#clear terminal
class IterableArray:
	def __init__( self, arr ):
		self.arr = arr
		self.index = 0
		self.index_max = len( self.arr ) - 1
		self.used = False

	def next( self ):
		self.used = True
		if self.index == self.index_max:
			self.index = 0
			return self.arr[ self.index ]
		self.index += 1
		return self.arr[ self.index ]
	
	def prev( self ):
		self.used = True
		if self.index == 0:
			self.index = len( self.arr )
		self.index -= 1
		return self.arr[ self.index ]

	def restart( self ):
		self.index = 1

	def get(self):
		return self.arr[ self.index ]
	def is_max(self):
		return self.index == self.index_max
	def is_min(self):
		return self.index == 0
	def first(self):
		self.index = 0
	def last(self):
		self.index = self.index_max

class Navigation:
	next = 'NEXT'
	prev = 'PREV'

def getInput():
	userInput = ''
	while True:
		ch = readchar.readkey()
		# Map Arrow Keys to your internal logic
		if ch in (key.UP, key.LEFT):
			return Navigation.prev
		
		elif ch in (key.DOWN, key.RIGHT):
			return Navigation.next
		
		elif ch == key.ENTER:
			# Return the text typed so far
			return userInput
		elif ch == key.BACKSPACE:
			if len(userInput) > 0:
				userInput = userInput[:-1]
				# Standard way to "erase" a character in terminal: 
				# Backspace, Space, Backspace
				sys.stdout.write('\b \b')
				sys.stdout.flush()
		
		elif ch == key.CTRL_C:
			# Good practice to handle manual interrupts
			raise KeyboardInterrupt

		elif len(ch) == 1:
			# Regular character input
			userInput += ch
			sys.stdout.write(ch)
			sys.stdout.flush()

#clear terminal
def clearScreen( ):
	os.system('cls' if os.name == 'nt' else 'clear')

#wait for user to press enter
def pause( text = 'Press enter to continue...'):
	input( text )

class simpleMenu( ):
	#default back function that enables loop exit
	def Back( self ):
		self.run = False

	#deletes the first default option and sets the offset to 1
	def delBackAndOffset( self ):
		del self.menuOptions[ '0' ]
		self.currentAutoIndex = 1

	def reset( self, title ):
		#sets default values
		#creates menuOptions used to store the functions related to the menu
		#creates menuNames that stores user readable name
		#with the same index as the function related to it

		self.menuOptions = 	{ '0': [ self.Back, 'Back' ] }
		if ( title != '' ):
			self.title = title
		
		#prints afther the menu
		self.description = ''

		#should it still run
		self.run = True

		#for breaking outside the loop
		self.breaking = False

		#for adding space in between the option
		self.spacing = []

		#for currect indexing when a str is added as a key
		self.currentAutoIndex = 1

		self.menuOptionsExtra = {}

		self.menuOptionsExtra_onSelection  = {}
		self.menuOptionsExtra_always = {}
		self.menuPrintableList = []
		
	def __init__( self, title, defaultFunction = False, depth=0 ):
		#sets title calls reset to set values
		self.title = title
		self.reset( title )
		self.defaultFunction = defaultFunction
		self.depth = depth
		self.parent=None
	
	def add_subMenu(self, name, subMenu, onSelection=False, always=False, key=None):
		if(type(key) is type(None)):
			key=str(self.currentAutoIndex)
			self.currentAutoIndex += 1
		self.menuOptionsExtra[key] = subMenu
		self.add_depth(subMenu)
		subMenu.parent = self
		if(onSelection):
			self.menuOptionsExtra_onSelection[key] = True
		if(always):
			self.menuOptionsExtra_always[key]=True
		self.menu_option_add(None, name, customKey=str(key))
	
	def add_depth(self, menu):
		menu.depth = self.depth + 1
		menu.add_subMenu_depths()
		menu.menu_build()
	
	def add_subMenu_depths(self):
		for key,subMenu in self.menuOptionsExtra.items():
			self.add_depth(subMenu)

	def get_MenuOptions(self):
		return self.menuOptions

	def outside_loop_break(self):
		self.run = False
		self.breaking = True

	def change_back_to_outside_loop_break(self, name = 'Back'):
		self.menuOptions['0'] = [ self.outside_loop_break, name ]

	def change_backFunction( self, key, func, name, args=False ):
		#replaces key value function for the first value
		if( args ):
			func_custom = functools.partial( func, args )
		else:
			func_custom = func
		
		self.menuOptions[ key ] = self.menuOptions['0']
		del self.menuOptions['0']
		self.menuOptions[ key ] = [ func_custom,name ]

	def menu_option_add( self, func, name, customKey=False, args=False ):
		#adds a new function to menuOptions with a int key
		#and stores a user readable name with same index
		
		#checks if args are present
		if( args ):
			func_custom = functools.partial( func, args )
			
		else:
			func_custom = func
		
		if( customKey ):
			self.menuOptions.update( { str(customKey) : [ func_custom,name ] } )
		
		else:
			#sets the key value to be the next number in line
			self.menuOptions.update( { str(self.currentAutoIndex) : [ func_custom, name ] } )
			self.currentAutoIndex += 1
	
	def menu_option_remove( self, key ):
		del self.menuOptions[ key ]

	def defaultFunction_SetTo( self, func, args = False):
		if( args ):
			func_custom = functools.partial( func, args )
		else:
			func_custom = func
		self.defaultFunction = func_custom

	def set_menuPrintableList(self, choiceOverwrite=None):
		self.menuPrintableList=[]
		currentChoice = self.choiceIteration.get()
		for key,value in self.menuOptions.items():
			keyStr=str(key)
			if(keyStr in self.spacing):
				self.menuPrintableList.append ( '' )
			temp=' '*(6*self.depth)
			if(currentChoice == str( key ) and choiceOverwrite==None):
				temp += '->'
			elif(choiceOverwrite== str( key )):
				temp += '->'
			else:
				temp += '  '
			temp += '[' + keyStr + ']'
			self.menuPrintableList.append ( temp + '' + value[1] )
			if(self.menuOptionsExtra_always.get(keyStr,False) or (self.menuOptionsExtra.get( keyStr, False ) and currentChoice == keyStr)):
				subMenu=self.menuOptionsExtra[keyStr]
				for item in subMenu.menuPrintableList:
					self.menuPrintableList.append ( item )
		if(self.description!=''):
			self.menuPrintableList.append ( '' )
			self.menuPrintableList.append ( ' '*(6*self.depth)+self.description )
			self.description = ''

	def menu_print( self):
		#prints the title and adds '-' as a seperator
		#with the length as the title
		print( self.title )
		seperator = ''
		for _ in self.title:
			seperator +='-'
		print( seperator )
		
		for menuItem in self.menuPrintableList:
			print(menuItem)
	
	def set_Iterator(self):
		self.choiceIteration = IterableArray( list( self.menuOptions.keys() ) )

	def getPath(self):
		path = [self.title]
		current = self.parent
		while current is not None:
			path.insert(0, current.title)
			current = current.parent
		return path

	def setInput(self, inp, childInp=False):
		if (self.menuOptionsExtra.get( self.choiceIteration.get(), False ) and not childInp):
			subMenu=self.menuOptionsExtra[self.choiceIteration.get()]
			subMenu.setInput(inp)
			self.set_menuPrintableList()
			return
		if ( inp == Navigation.next):
			if (self.choiceIteration.is_max()):
				if(type(self.parent) is not type(None)):
					self.parent.setInput(inp, childInp=True)
				self.choiceIteration.first()
			else:
				self.choiceIteration.next()
		elif ( inp == Navigation.prev):
			if (self.choiceIteration.is_min()):
				if(self.parent is not None):
					self.parent.setInput(inp, childInp=True)
				else:
					self.choiceIteration.last()
			else:
				self.choiceIteration.prev()
		else:
			if( inp != '' ):
				menuOption = self.menuOptions.get( inp, False )
			# If inp is empty string, it means 'Enter' was pressed
			else:
				menuOption = self.menuOptions.get( self.choiceIteration.get(), False )
			#first option is always back, call back in parent menu
			if (self.choiceIteration.is_min()):
				if(self.parent is not None):
					self.parent.setInput(Navigation.prev, childInp=True)
			elif( menuOption ):
				menuOption[ 0 ]()
			else:
				print( inp, 'is not on list' )
				pause()
		self.set_menuPrintableList()
		
	def menu_build(self):
		self.set_Iterator()
		self.set_menuPrintableList()

	def menu_start( self ):
		while ( True ):
			#if the loop should still run
			if(self.run):
				
				#clears terminal
				clearScreen()

				if(self.defaultFunction):
					self.defaultFunction()
				
				#prints the menu
				self.menu_print()
				print( 'Choice -> ', end = '', flush = True )
				inp = getInput()
				#send next, prev, enter to child
				self.setInput(inp)

			else:
				break