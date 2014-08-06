import commands,sys
def lookup():
	f=open('/home/kehl/bash_sample/tmp.log','r')
	line = f.readline().strip()
	f.close()
	commands.getstatusoutput('rm /home/kehl/bash_sample/tmp.log')
	status,output = commands.getstatusoutput('screen -ls')
	screens = output.split('\n')[1:-2]
	if len(screens)==0:
		print 'nop_'+line
		return
	for screen in screens:
		screen  = screen.strip()
		screen = screen[screen.index('.')+1:screen.index('(')-1]
		if screen == line:
			print 'yes_'+line
			return
	print 'nop_'+line

if __name__=='__main__':
	lookup()
