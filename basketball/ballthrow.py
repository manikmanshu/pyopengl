'''

Implementation of projectile motion

'''

import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *

v0 = 150		#initial velocity
angle = 45	#initial direction	
radangle = (angle*3.14)/180  # degree to radians
t = 0
a=-3	#initial x-coord of ball position
b=-2	#initial y-coord of ball position
movx = a
movy = b

def InitGL(Width, Height): 
 
        glClearColor(0.0, 0.0, 0.0, 1.0) 
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(75.0, float(Width)/float(Height), 1, 100.0)
        #gluLookAt()
        glMatrixMode(GL_PROJECTION)
        #glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 30)
        #glFrustum(-3.0,50.0,-5.0,100.0,10.0,-10.0)
        
        #gluLookAt(0,0,5,2,0.5,0,0,1,0,)
        glTranslate(-18,0,-15)
        glMatrixMode(GL_MODELVIEW)
	


def projectile():
	global a,b,movx,movy
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(0,-6,-10)
	
	move()			#performs projectile motion
	glColor3f(0.9,0.0,0.0)
	glTranslatef(movx,movy,0)
	glutSolidSphere(0.4,20,10)

	glFlush()
	glutSwapBuffers()

	
def move():
	global v0,t,angle,movx,movy,a,b,radangle
	time.sleep(0.02)
	if radangle > 0 :
		vx = v0*cos(radangle)		#velocity in x- direction
		vy = v0*sin(radangle) - 9.8*t	#velocity in y-direction
		movx = a+v0*t*cos(radangle)	#instantaneous x - position
		movy = b+v0*t*sin(radangle) - 4.9*t*t #instantaneous y-position
		if vx!=0:
			radangle = atan(vy/vx)	#instantaneous angle
			
			
	#Momentum Conservation
	else:
		v0 = v0/1.5
		radangle =45*3.14/180
		a = movx
		b = movy 
		t=0
	t=t+0.001
	glutPostRedisplay()
	
def main():
 
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(1000,700)
	glutInitWindowPosition(0,0)	
	glutCreateWindow('PROJECTILE')
	
	glutDisplayFunc(projectile)
	glutIdleFunc(projectile)
	InitGL(640, 480)
	glutMainLoop()
        
if __name__ == "__main__":
	main() 
