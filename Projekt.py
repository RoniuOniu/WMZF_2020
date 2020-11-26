from vpython import *
from random import uniform
import numpy as np
import matplotlib as mp
# inicjowanie atomow
scene.caption ="""by obracać kamerą, przeciągnij trzymając prawy przycisk myszki lub Ctrl-drag.
by powiększyć, przeciągnij środkowym myszki albo użyj scrolla myszki. ."""

side = 4.0
thk = 0.3
s2 = 2*side - thk
s3 = 2*side + thk
# tworzenie pudełka
wallR = box (pos=vector( side, 0, 0), size=vector(thk, s2, s3),  color = color.red)
wallL = box (pos=vector(-side, 0, 0), size=vector(thk, s2, s3),  color = color.red)
wallU = box (pos=vector(0, -side, 0), size=vector(s3, thk, s3),  color = color.blue)
wallD = box (pos=vector(0,  side, 0), size=vector(s3, thk, s3),  color = color.blue)
wallB = box(pos=vector(0, 0, -side), size=vector(s2, s2, thk), color = color.gray(0.7))

# tworzenie atomów
no_particles=10
ball_radius=0.2
maxpos=side-thk/2-ball_radius
maxv=1
ball_list=[]
dt = 0.3


for i in range(no_particles):
    ball=sphere(color=color.green,radius=ball_radius,retain=100)
    ball.pos=maxpos*vector(uniform(-1,1),uniform(-1,1),uniform(-1,1))
    ball.velocity=maxv*vector(uniform(-1,1),uniform(-1,1),uniform(-1,1))
    ball_list.append(ball)
    ball.mass = 1.0
    ball.p = vector(-0.15, -0.23, +0.27)
# pętla sprawdzająca
while (1==1):
    rate(100)
    timestep=0.1
    for ball in ball_list:
        ball.pos = ball.pos + ball.velocity*timestep
            #prawa ściana
        if ball.pos.x > maxpos:
            ball.velocity.x = -ball.velocity.x  # odbijaj prędkość
            ball.pos.x = 2 * maxpos - ball.pos.x  # odbijaj pozycje
            # lewa ściana
        if ball.pos.x < -maxpos:
            ball.velocity.x = -ball.velocity.x
            ball.pos.x = -2 * maxpos - ball.pos.x
            # sufit
        if ball.pos.y> maxpos:
            ball.velocity.y = -ball.velocity.y
            ball.pos.y = 2 * maxpos - ball.pos.y
            # podłoże wall
        if ball.pos.y < -maxpos:
            ball.velocity.y = -ball.velocity.y
            ball.pos.y = -2 * maxpos - ball.pos.y
            # przednia ściana
        if ball.pos.z > maxpos:
            ball.velocity.z = -ball.velocity.z
            ball.pos.z = 2 * maxpos - ball.pos.z
            # tylna ściana
        if ball.pos.z < -maxpos:
            ball.velocity.z = -ball.velocity.z
            ball.pos.z = -2 * maxpos - ball.pos.z
 # sprawdź kolizje ze ścianami
# Detekcja zderzeń atomów
 # zapętlanie przez wszystkie pary
    for i in range(no_particles):
        for j in range(i+1,no_particles):
            distance=mag(ball_list[i].pos-ball_list[j].pos)
            # sprawdzanie kolizji
            if distance<(ball_list[i].radius+ball_list[j].radius):
                #unit vector in collision direction
                    direction=norm(ball_list[j].pos-ball_list[i].pos)
                    vi=dot(ball_list[i].velocity,direction)
                    vj=dot(ball_list[j].velocity,direction)
                    # prędkość zderzenia
                    exchange = vj - vi
                    # wymiana momentum
                    ball_list[i].velocity = ball_list[i].velocity + exchange * direction
                    ball_list[j].velocity = ball_list[j].velocity - exchange * direction
                    overlap = 2 * ball_radius - distance
                    ball_list[i].pos = ball_list[i].pos - overlap * direction
                    ball_list[j].pos = ball_list[j].pos + overlap * direction