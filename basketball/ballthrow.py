'''
ballthrow.py
Simple basketball view using pyopengl 

Implementation of projectile motion
Added Basket Ring
Added Ground and walls

Enabling GL_LIGHTING and AMBIENT light
Added spot light
Added trigger
Added feature of Camera View Change

Added Collision of ball with walls, ground and basket ring

Added reset feature
Change camera manually using keyboard key 'c'

Added textures using Image library 
texture functions taken from example program CubeT1.py

Modify camera and added custom camera view


'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL.Image import *
from math import *
import time

#v0 = 150		#initial velocity
#angle = 45	#initial direction
v0 = input("ENter velocity: ") #150		#initial velocity
angle = input("Enter direction: ") #45	#initial direction	
radangle = (angle*3.14)/180  # degree to radians
temp_vel=v0
t = 0
a=-3	#initial x-coord of ball position
b=-2	#initial y-coord of ball position
movx = a
movy = b
x=-3
y=-8
shoulder = 0.0  #robot arm variables
elbow = 0.0

start=0	#trigger
final_view = 0
wallcollide=0   #collision control
camera=0	#camera control

eye_x,eye_y,eye_z = 0,0,15
center_x,center_y,center_z = 0,0,0
up_x,up_y,up_z = 0,1,0

def CreateTexture(imagename, number):
        global textures

        image = open(imagename)
        ix = image.size[0]
        iy = image.size[1]
        image = image.tostring("raw", "RGBX", 0, -1)

        glBindTexture(GL_TEXTURE_2D, int(textures[number]))   

        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        
def CreateLinearFilteredTexture(imagename, number):
        global textures

        image = open(imagename)
        ix = image.size[0]
        iy = image.size[1]
        image = image.tostring("raw", "RGBX", 0, -1)

        glBindTexture(GL_TEXTURE_2D, int(textures[number]))   
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

def CreateMipMappedTexture(imagename, number):
        global textures

        image = open(imagename)
        ix = image.size[0]
        iy = image.size[1]
        image = image.tostring("raw", "RGBX", 0, -1)

        glBindTexture(GL_TEXTURE_2D, int(textures[number]))
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 3, ix, iy, GL_RGBA, GL_UNSIGNED_BYTE, image)

def LoadTextures(number):
	global texture_num, textures

	textures = glGenTextures(number)
	CreateTexture("texturedyellow.jpg",0)
	CreateLinearFilteredTexture("nha.jpg", 1)
	CreateMipMappedTexture("bathroomfloor.png",2)


def InitGL(Width, Height): 
	
	LoadTextures(3)
	glEnable(GL_TEXTURE_2D)     
	glClearDepth(1.0)                       
	glDepthFunc(GL_LESS)                    

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
	global a,b,movx,movy,x,y,elbow,shoulder,start,final_view
	global textures
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(0,-4,-10)
	glEnable(GL_LIGHTING)
	glLight(GL_LIGHT0, GL_POSITION, (25,20,10,0.0))
	
	camera_view()	#different camera shots

	glBindTexture(GL_TEXTURE_2D, int(textures[0]))
	glBegin(GL_QUADS)                               # Start Drawing The Cube

	# Yellow wall
	glTexCoord2f(0.0, 0.0); glVertex3f(-18.0, -10.0,  -12.0)    # Bottom Left Of The Texture and Quad
	glTexCoord2f(1.0, 0.0); glVertex3f( 45.0, -10.0,  -12.0)    # Bottom Right Of The Texture and Quad
	glTexCoord2f(1.0, 1.0); glVertex3f( 45.0,  30.0,  -12.0)    # Top Right Of The Texture and Quad
	glTexCoord2f(0.0, 1.0); glVertex3f(-18.0,  30.0,  -12.0)    # Top Left Of The Texture and Quad

	glEnd()
	
	glBindTexture(GL_TEXTURE_2D, int(textures[1]))
	glBegin(GL_QUADS)                               # Start Drawing The Cube

	# nha  Green Wall
	glTexCoord2f(0.0, 0.0); glVertex3f(40.0, -15.0,  -13.0)    # Bottom Left Of The Texture and Quad
	glTexCoord2f(1.0, 0.0); glVertex3f( 40.0, -15.0,  28.0)    # Bottom Right Of The Texture and Quad
	glTexCoord2f(1.0, 1.0); glVertex3f( 40.0,  30.0,  28.0)    # Top Right Of The Texture and Quad
	glTexCoord2f(0.0, 1.0); glVertex3f(40.0,  30.0,  -13.0)    # Top Left Of The Texture and Quad

	glEnd()

	glBindTexture(GL_TEXTURE_2D, int(textures[2]))
	glBegin(GL_QUADS)                               # Start Drawing The Cube

	#Floor
	glTexCoord2f(0.0, 0.0); glVertex3f(-18.0, -8.5,  -13.0)    # Bottom Left Of The Texture and Quad
	glTexCoord2f(1.0, 0.0); glVertex3f( -18.0, -8.5,  28.0)    # Bottom Right Of The Texture and Quad
	glTexCoord2f(1.0, 1.0); glVertex3f( 40.0,  -8.5,  28.0)    # Top Right Of The Texture and Quad
	glTexCoord2f(0.0, 1.0); glVertex3f(40.0,  -8.5,  -13.0)    # Top Left Of The Texture and Quad

	glEnd()		
	
	'''
	#Stand
	glPushMatrix()
	glLineWidth(5)
	glTranslate(40,4.5,0)
	glScale(1,15,0.2)
	glutWireCube(1)
	glPopMatrix()
	'''
	
	glDisable(GL_TEXTURE_2D)
	# Side Wall
	glPushMatrix()
	glTranslate(42,5,0)
	glScale(3,40,30)
	glColor3f(1.0, 0.7, 0.0)
	glutSolidCube(1)
	glPopMatrix()

	
	#Back Wall
	glPushMatrix()
	glTranslate(18,8,-15)
	glScale(56,45,0.2)
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
	glScale(55,2,26)
	glColor3f(1.0, 1.0, 0.0)
	#glutSolidCube(1)
	glPopMatrix()
	
	#BasketRing
	glPushMatrix()
	glTranslate(38,10,0)
	glRotate(90,1,0,0)
	glScale(1,1.5,0)
	glColor3f(0.7, 0.2, 0.3)
	glutSolidTorus(0.5, 1.1, 20, 15)
	glPopMatrix()
	
	#trigger
	if start==0:
		time.sleep(0.09)
		shoulder = (shoulder + 5) % 360
		elbow = (elbow + 5) % 360
		if shoulder>350:
			start=1
	else:	
		move()			#performs projectile motion
		
	glPushMatrix()
	glTranslatef (-6.0, -8.0, 0.0)
	glRotatef (shoulder, 0.0, 0.0, 1.0) # shoulder robot
	glTranslatef (1.0, 0.0, 0.0)

	glPushMatrix()
	glScalef (2.0, 0.4, 1.0)
	glutSolidCube (1.0)
	glPopMatrix()

	glTranslatef (1.0, 0.0, 0.0)
	glRotatef (elbow, 0.0, 0.0, 1.0)	# elbow   robot
	glTranslatef (1.0, 0.0, 0.0)

	glPushMatrix()
	glScalef (2.0, 0.4, 1.0)
	glutSolidCube (1.0)
	glPopMatrix()

	glPopMatrix()	
	
	#Ball
	glTranslatef(0,-6,0)
	glColor3f(0.9,0.0,0.0)
	glTranslatef(movx,movy,0)
	glutSolidSphere(0.5,20,10)
	glEnable(GL_TEXTURE_2D)

	glFlush()
	glutSwapBuffers()

	
def move():
	global v0,t,angle,movx,movy,a,b,radangle,wallcollide,tx,ty
	time.sleep(0.02)  #delay
	if wallcollide==0:
		if radangle > 0 :
			
			vx = v0*cos(radangle)		#velocity in x- direction
			vy = v0*sin(radangle) - 9.8*t	#velocity in y-direction
			movx = a+v0*t*cos(radangle)	#instantaneous x - position
			movy = b+v0*t*sin(radangle) - 4.9*t*t #instantaneous y-position
			
			if movx >=38:
				tx = movx
				ty = movy
				wallcollide = 1
				#t=0
				
			if vx!=0:
				radangle = atan(vy/vx)	#instantaneous angle
			
			if movx >= 35.8 and movx <= 36.5:
				if movy >=15.1 and movy <=16.3:
					wallcollide = 2
				
			#print movx,movy		
		#Momentum Conservation
		else:
			v0 = v0/1.5
			radangle =45*3.14/180
			a = movx
			b = movy 
			t=0
	elif wallcollide==1:
		#time.sleep(0.2)
		
		vx = v0*cos(radangle)		#velocity in x- direction
		vy = v0*sin(radangle) - 9.8*t	#velocity in y-direction
		tempx = a+v0*t*cos(radangle)	#instantaneous x - position
		tempy = b+v0*t*sin(radangle) - 4.9*t*t #instantaneous y-position
			
		movx = tx - (tempx - tx)
		movy = ty + (tempy - ty)
			
		if vx!=0:
			radangle = atan(vy/vx)	#instantaneous angle
			
				#print wallcollide	
			
		if movy<=-2 or movx<0 :
			wallcollide = 3	
			movx = tx - (tempx - tx)
			movy = ty + (tempy - ty)
		#print movx,movy		
		#movx = movx-3
	elif wallcollide==2:
		if movy>=b:			
			movy -= 0.1
			
		if movy<=-2 or movx<0 :
			wallcollide = 3	

	else:
		time.sleep(3)
		reset_game()
		pass
	t=t+0.001
	glutPostRedisplay()
	
def reset_game():
	global v0,t,angle,movx,movy,a,b,radangle,x,y,wallcollide,tx,ty,start
	global shoulder,elbow,temp_vel
	t=0
	v0 = temp_vel
	a,b = -3,-2
	movx,movy = a,b
	radangle = (angle*3.14)/180
	x,y = -3,-8
	wallcollide = 0
	start = 0
	shoulder =0 
	elbow = 0
	final_view = 0
	
			
def camera_view():
	global camera
	global eye_x,eye_y,eye_z
	global up_x,up_y,up_z
	global center_x,center_y,center_z
	
	if camera==0:
		glTranslate(12,2,5)
		eye_x,eye_y,eye_z,center_x,center_y,center_z,up_x,up_y,up_z = 0,0,15,0,0,0,0,1,0
	elif camera==1:
		eye_x,eye_y,eye_z,center_x,center_y,center_z,up_x,up_y,up_z = 0,0,15,0,0,0,0,1,0
		gluLookAt(0,5,5,-8,-8,0,0,1,-5,)
		#gluLookAt(0,0,5,-5,-5,0,0,1,0,)
	elif camera==2:
		eye_x,eye_y,eye_z,center_x,center_y,center_z,up_x,up_y,up_z = 0,0,15,0,0,0,0,1,0
		gluLookAt(0,10,5,0,-5,0,0,1,0,)
	elif camera==3:
		eye_x,eye_y,eye_z,center_x,center_y,center_z,up_x,up_y,up_z = 0,0,15,0,0,0,0,1,0	
		glRotate(30,1,0,0)
		glRotate(110,0,1,0)
	elif camera==4:
		gluLookAt(0,0,15,0,0,0,0,1,0,)
		#eye_x,eye_y,eye_z,center_x,center_y,center_z,up_x,up_y,up_z = 0,0,15,0,0,0,0,1,0
	elif camera==5:	
		gluLookAt(eye_x,eye_y,eye_z,center_x,center_y,center_z,up_x,up_y,up_z)
	else:
		gluLookAt(0,0,15,0,0,0,0,1,0,)	
					
		
def keyboard(key, x, y):
	global camera
	global eye_x,eye_y,eye_z
	global center_x,center_y,center_z
	global up_x,up_y,up_z



	if key == chr(27): sys.exit(0)
	elif key == 'c':
		camera = (camera + 1)%7
		glutPostRedisplay()
	elif key == 'C':
		camera = (camera - 1)%7
		glutPostRedisplay()
	elif key == '1':
		eye_x = eye_x + 0.1
		glutPostRedisplay()
	elif key == '!':
		eye_x = eye_x - 0.1
		glutPostRedisplay()	
	elif key == '2':
		eye_y = eye_y + 0.1
		glutPostRedisplay()
	elif key == '@':
		eye_y = eye_y - 0.1
		glutPostRedisplay()
	elif key == '3':
		eye_z = eye_z + 0.1
		glutPostRedisplay()
	elif key == '#':
		eye_z = eye_z - 0.1
		glutPostRedisplay()	
	elif key == '4':
		center_x = center_x + 0.1
		glutPostRedisplay()
	elif key == '$':
		center_x = center_x - 0.1
		glutPostRedisplay()	
	elif key == '5':
		center_y = center_y + 0.1
		glutPostRedisplay()
	elif key == '%':
		center_y = center_y - 0.1
		glutPostRedisplay()
	elif key == '6':
		center_z = center_z + 0.1
		glutPostRedisplay()
	elif key == '^':
		center_z = center_z - 0.1
		glutPostRedisplay()
	elif key == '7':
		up_x = up_x + 0.1
		glutPostRedisplay()
	elif key == '&':
		up_x = up_x - 0.1
		glutPostRedisplay()	
	elif key == '8':
		up_y = up_y + 0.1
		glutPostRedisplay()
	elif key == '*':
		up_y = up_y - 0.1
		glutPostRedisplay()
	elif key == '9':
		up_z = up_z + 0.1
		glutPostRedisplay()
	elif key == '(':
		up_z = up_z - 0.1
		glutPostRedisplay()		

def main():
 
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(1000,700)
	glutInitWindowPosition(0,0)	
	glutCreateWindow('BasketBall')
	
	glutDisplayFunc(projectile)
	glutIdleFunc(projectile)
	glutKeyboardFunc(keyboard)
	InitGL(640, 480)
	glutMainLoop()
        
if __name__ == "__main__":
	main() 
