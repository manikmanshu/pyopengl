'''

clock.py

Analog Clock created using OpenGL library
'''


# All imports
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os
import time
import datetime
from math import sin, cos

#initialization of global variables
def globals_var():
	global x,y,n,now,sync,syncmin,synchour
	x = []
	y = []
	n = 60
	now = datetime.datetime.now()
	sync = now.second
	syncmin = now.minute
	synchour = (now.hour % 12) * 5

# initializtion of opengl window
def InitGL(Width, Height): 
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0) 
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)   
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)


# Set up point at circle co-ordinate
def drawpoint():
	global n,sync,syncmin,synchour
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(0,0,-10)
	glColor(0.8,0.8,0.1)
	
	for i in range(0,n):
		if i%5 != 0 :
			vertex(x[i],y[i])
		else:
			vertex_hour(x[i],y[i])	

	vertex(0,0)
	
	glColor(0.9,0.4,0.1)
	hand(x[sync],y[sync],0,0,5)	#Second hand
		
	x_min = x[syncmin]*0.85
	y_min = y[syncmin]*0.85
	glColor(0.4,0.5,0.8)
	hand(x_min,y_min,0,0,5)	# minutes hand
	
	x_hour = x[synchour]*0.5
	y_hour = y[synchour]*0.5
	glColor(0.2,0.7,0.8)
	hand(x_hour,y_hour,0,0,12) # hour hand
	
	now = datetime.datetime.now()
	sync = now.second
	syncmin = now.minute
	synchour = (now.hour % 12) * 5 + (syncmin/12)
		
	glutSwapBuffers()

# Draw the Vertex at specified x,y	
def vertex(x,y):
	glColor(0.8,0.8,0.1)
	glPointSize(10)
	glBegin(GL_POINTS)
	glVertex2f(x, y)
	glEnd()	
	glFlush()
	
def vertex_hour(x,y):
	glColor(0.4,0.9,0.2)
	glPointSize(20)
	glBegin(GL_POINTS)
	glVertex2f(x, y)
	glEnd()	
	glFlush()	

# Clock hands sec,min,hour
def hand(x,y,a,b,thickness):
	glLineWidth(thickness)
	glBegin(GL_LINES)
	glVertex(x,y)
	glVertex(a,b)
	glEnd()
	glFlush()


# minutes co-ordintes	
def coordinates():
	global n,x,y
	r=3		#radius
	PI = 3.14
	for i in range(0,n):
		x.append(0)
		y.append(0)
		x[i] = 0 + r * sin(2.0*PI*i/n);
		y[i] = 0 + r * cos(2.0*PI*i/n);



# main function
def main(): 
	global window
	globals_var()
	coordinates()
		
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(640,480)
	glutInitWindowPosition(50,0)	
	window = glutCreateWindow('CLOCK')
	
	glEnable( GL_POINT_SMOOTH )
	glEnable(GL_LINE_SMOOTH)
	glEnable( GL_BLEND )
	glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
	
	glutDisplayFunc(drawpoint)
	glutIdleFunc(drawpoint)
	InitGL(640, 480)
	glutMainLoop()
        
if __name__ == "__main__":
	main() 
