import sys,commands
def go():
	status,output = commands.getstatusoutput('screen -ls')
	screens = output.split('\n')[1:-2]
	if len(screens)==0:
		print 'no'
		return
	for screen in screens:
		screen = screen.strip()
		screen = screen[screen.index('.'):]
		if screen==sys.argv[1]:
			print screen
			return
	print 'no'
if __name__=='__main__':
	go()
