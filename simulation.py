from ursina import * 
from math import *
#scale en Mm alors que le reste est en m et et kg
import matplotlib.pyplot as plt
cs = 5
def vecteurv(a,b) :
    global skip
    dx = (a[0].x-b[0].x)*1e6
    dy = (a[0].y-b[0].y)*1e6
    dz = (a[0].z - b[0].z)*1e6
    dist = round(sqrt(dx**2 + dy **2 + dz **2), cs)
    Fab = round(G*a[1]*b[1]/dist**2, cs)
    # F = m*a
    aacc = Fab/a[1]
    bacc = Fab/b[1]

    b[2][0] +=round(bacc * (dx/dist)*time.dt * skip, cs)
    b[2][1] +=round(bacc * (dy/dist)*time.dt * skip, cs)
    b[2][2] += round(bacc * (dz/dist)*time.dt * skip, cs)

    dx = (b[0].x-a[0].x)*1e6
    dy = (b[0].y-a[0].y)*1e6
    dz = (b[0].z - a[0].z)*1e6


    a[2][0] += round(aacc * (dx/dist) *time.dt * skip, cs)
    a[2][1] += round(aacc * (dy/dist)*time.dt * skip, cs)
    a[2][2] += round(aacc * (dz/dist)*time.dt * skip, cs)





ua = 150000
skip = 1
G = 6.6e-11
app = Ursina()
#SCALE EN Mm et Masse en Kg et position en Mm
sun = [Entity(model = 'Sphere', color = color.yellow, scale = 6, position= (8,-1)),2e17,[0,1,0]]
terre = [Entity(model = 'Sphere', color = color.blue, scale = 6, position = (8,8,0)),2e17, [-1,0,0]]

lune = [Entity(model = 'Sphere', color = color.white, scale =  6, position = (-45,45,0)),2e17, [0,0,0]]

texte  = Text(text=f'Timeskip : {skip}', position=(-0.5, 0.5), scale=1)

focus = False
cible = sun[0]
textefocus = Text(text=f'Cam focus : {focus}', position=(-0.75, 0.5), scale=1)

objetceleste = [sun,terre,lune]

def update() :
    global focus
    global cible

    #Toutes les relations
    vecteurv(sun, terre)
    vecteurv(lune, terre)
    vecteurv(lune, sun)
    for astre in objetceleste :

        astre[0].x += astre[2][0]
        astre[0].y += astre[2][1]
        astre[0].z += astre[2][2]


    if focus : 
        ec.position = cible.position




camera.clip_plane_near = 0.1
camera.clip_plane_far = 10000000
ec = EditorCamera()
def input(key):
    global skip
    global cible
    global focus
    if key == 't' :
        ec.position = terre[0].position
        cible = terre[0]
    if key == 's' :
        ec.position = sun[0].position
        cible = sun[0]
    if key == 'l' :
        ec.position = lune[0].position
        cible = lune[0]
    if key == "f" :
        if focus : 
            focus = False
        else :
            focus = True
        textefocus.text =f'Cam focus : {focus}'
    if key =='+' :
        skip = skip *10
        texte.text = f'Timeskip : {skip}'
    if key == '-' :
        skip = skip /10
        texte.text = f'Timeskip : {skip}'

    if key == 'escape':
        app.quit()

app.run()      