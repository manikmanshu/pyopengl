'''
ballthrow.py
Simple basketball view using pyopengl 

Implementation of projectile motion
Added Basket Ring
Added Ground and walls

Enabling GL_LIGHTING and AMBIENT light
Added spot light

'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
import time

v0 = 150		#initial velocity
angle = 45	#initial direction	
radangle = (angle*3.14)/180  # degree to radians
t = 0
a=-3	#initial x-coord of ball position
b=-2	#initial y-coord of ball position
movx = a
movy = b
x=-3
y=-8

def InitGL(Width, Height): 

	glClearColor(0.3, 0.3, 1.0, 0.5) 
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(75.0, float(Width)/float(Height), 1, 100.0)
	#gluLookAt()
	glMatrixMode(GL_PROJECTION)
	#gluLookAt(0,0,5,2,0.5,0,0,1,0,)
	glTranslate(-18,0,-15)
	glMatrixMode(GL_MODELVIEW)
	
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_COLOR_MATERIAL)
	glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS,20)
	
	mat_shininess = [30.0]
	white_light = [0.8, 0.8, 0.8, 1.0]
	glShadeModel(GL_SMOOTH)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, white_light)
	glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
	glEnable(GL_CULL_FACE)
	glCullFace(GL_BACK)
	

def projectile():
	global a,b,movx,movy,x,y
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(0,-4,-10)
	
	glLight(GL_LIGHT0, GL_POSITION, (25,20,10,0.0))

	
	'''
	#Stand
	glPushMatrix()
	glLineWidth(5)
	glTranslate(40,4.5,0)
	glScale(1,15,0.2)
	glutWireCube(1)
	glPopMatrix()
	'''
	
	# Wall
	glPushMatrix()
	glTranslate(42,5,0)
	glScale(3,30,2)
	glColor3f(1.0, 0.7, 0.0)
	glutSolidCube(1)
	glPopMatrix()
	
	#BackGroundFLoor
	glPushMatrix()
	glTranslate(18,8,-10)
	glScale(62,45,0.2)
	glColor3f(0, 1, 1)
	glutSolidCube(1)
	glPopMatrix()
	
	
	position =  [0.0, 0.0, 0.0, 1.0]
	
	#glutWireCube (1)
	glPushMatrix ()
	glLightfv (GL_LIGHT0, GL_POSITION, position)
	glDisable (GL_LIGHTING)
	glColor3f (0.0, 1.0, 1.0)
	#glutWireCube (1)
	glEnable (GL_LIGHTING)
	glPopMatrix ()
	
	#Spot Lighting 
	glPushMatrix()
	pos = [movx, movy,4, 1]
	direction = [0.0, -5.0, 0.0]
	spotAngle = 40
	
	glLightfv(GL_LIGHT0, GL_POSITION, pos)
	glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, spotAngle)
	glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, direction)
	glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 1)
	glPopMatrix()
	
	#FLoor
	glPushMatrix()
	glTranslate(18,-9.5,0)
	glScale(48,2,2)
	glColor3f(1.0, 1.0, 0.0)
	glutSolidCube(1)
	glPopMatrix()
	
	#BasketRing
	glPushMatrix()
	glTranslate(38,10,0)
	glRotate(90,1,0,0)
	glScale(1,1.5,0)
	glColor3f(0.7, 0.2, 0.3)
	glutSolidTorus(0.5, 1.1, 20, 15)
	glPopMatrix()
		
	move()			#performs projectile motion
	
	#Ball
	glTranslatef(0,-6,0)
	glColor3f(0.9,0.0,0.0)
	glTranslatef(movx,movy,0)
	glutSolidSphere(0.5,20,10)

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
