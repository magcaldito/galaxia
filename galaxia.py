#!/usr/bin/env python3
import sys
import time
import pygame
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

fps=60
reloj = pygame.time.Clock()

white=pygame.Color(255,255,255)
green=pygame.Color(0,255,0)        
yellow=pygame.Color(255,255,0)      
cyan=pygame.Color(0,255,255)      
blue=pygame.Color(0,0,255)
black=pygame.Color(0,0,0)
pink=pygame.Color(255,100,100)
sonidodisparo = pygame.mixer.Sound("sonidos/TIRO.WAV")
sonidomatao = pygame.mixer.Sound("sonidos/MATAO.WAV")
sonidoexplode = pygame.mixer.Sound("sonidos/EXPLODE.WAV")

ANCHOP=1020
ALTOP=710

Xc=ANCHOP/2
Yc=ALTOP/2+300

Xm01=ANCHOP/2
Ym01=0.0

H=70
B=60
L=10

saltonave=10
saltodisparo=20

pygame.display.set_caption('Galaxia')
ventana= pygame.display.set_mode((ANCHOP,ALTOP))
                                 

def distancia(x0, y0, x1, y1):
    distancia = ((x1-x0)**2 + (y1-y0)**2)**0.5
    return distancia

              
def marcador(x):
    fuente = pygame.font.SysFont('times new roman', 20)
    marcador_surface = fuente.render('  Marcador = '+ str(x)+'  ', True, yellow)
    marcador_rect = marcador_surface.get_rect()
    marcador_rect.midtop = (ANCHOP*0.9, ALTOP/20)
    pygame.draw.rect(ventana,black,marcador_rect)
    ventana.blit(marcador_surface, marcador_rect)
    #show_score(0, red, 'times', 20)
    return marcador
    

def dibunave01(x,y,color):
    pygame.draw.line(ventana,color,(x-B/2,y+H/2),(x+B/2,y+H/2),width=1)
    pygame.draw.line(ventana,color,(x-B/10,y+H/2),(x-B/10,y-H/10),width=1)
    pygame.draw.line(ventana,color,(x+B/10,y+H/2),(x+B/10,y-H/10),width=1)
    pygame.draw.line(ventana,color,(x-B/10,y-H/10),(x+B/10,y-H/10),width=1)
    pygame.draw.line(ventana,color,(x-B/2,y+H/2),(x-B/10,y-H/10),width=1)
    pygame.draw.line(ventana,color,(x+B/2,y+H/2),(x+B/10,y-H/10),width=1)
    pygame.draw.line(ventana,color,(x-B/10,y-H/10),(x,y-H/2),width=1)
    pygame.draw.line(ventana,color,(x+B/10,y-H/10),(x,y-H/2),width=1)
#    pygame.display.flip()
    

def dibumalo01(x,y,color):
    rectelip = pygame.Rect(x-10,y-5,20,10)
    pygame.draw.ellipse(ventana,color,rectelip,width=1)
    pygame.draw.line(ventana,color,(x-20,y),(x+20,y),width=1)
    pygame.draw.line(ventana,color,(x-20,y-10),(x-20,y+10),width=1)
    pygame.draw.line(ventana,color,(x+20,y-10),(x+20,y+10),width=1)
#    pygame.display.flip()
    

def dibudisparo01(x,y,color):
    pygame.draw.line(ventana,color,(x,y+L/2),(x,y-L/2),width=2)
#    pygame.display.flip()
    
 
def finaliza():
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


for i in range (101):
    pygame.draw.circle(ventana,white,(random.random()*ANCHOP,random.random()*ALTOP),1)
    pygame.display.flip()


disparo=0
Score=0
contador=0
Xd=0.0
Yd=0.0
AXm01=0.0
AYm01=0.0
VXm01=0.0
VYm01=0.0
dXc=0

running = True
while running:
    
    marcador (Score)
    dibunave01(Xc,Yc,green)
    pygame.display.update()
    dibudisparo01(Xd,Yd,yellow)
    pygame.display.update()
    dibumalo01(Xm01,Ym01,pink)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #pygame.quit
            #sys.exit()
            running=False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_q:
                finaliza()
            if event.key == pygame.K_p:
                dXc=saltonave
            if event.key == pygame.K_i:
                dXc=-saltonave
            if event.key == pygame.K_o:
                dXc=0
            if event.key == pygame.K_d:
                disparo=1  
                pygame.mixer.Sound.play(sonidodisparo)

    if disparo == 1 and Yd == Yc - H/2 - L/2:
        pygame.mixer.Sound.play(sonidodisparo)

    time.sleep(0.006)
    dibumalo01(Xm01, Ym01, black)

    dt=1
    da=0.1
    ca=0.85

    AXm01=AXm01+random.random()*da - da/2
    AYm01=AYm01+random.random()*da - da/2*ca

    VXm01=VXm01+AXm01*dt
    VYm01=VYm01+AYm01*dt

    Xm01=Xm01+VXm01*dt+0.5*dt**2
    Ym01=Ym01+VYm01*dt+0.5*dt**2

    if Ym01 > ALTOP:
        Xm01=ANCHOP/2
        Ym01=0
        AXm01=0
        AYm01=0
        VXm01=0
        VYm01=0
        Score=Score - 1


    if distancia(Xm01, Ym01, Xd, Yd) <= 30.0:
        dibudisparo01 (Xd, Yd, black)
        pygame.draw.circle(ventana,yellow,(Xm01,Ym01),30,width=1)
        pygame.display.flip()
        time.sleep(0.2) 
        pygame.draw.circle(ventana,black,(Xm01,Ym01),30,width=1)
        Xm01=ANCHOP/2
        Ym01=0
        AXm01=0
        AYm01=0
        VXm01=0
        VYm01=0
        Score=Score+5
        pygame.mixer.Sound.play(sonidomatao)
        disparo=0

    if distancia (Xc, Yc, Xm01, Ym01) <= 90.0:
        dibunave01(Xc,Yc,black)
        dibudisparo01(Xd,Yd,black)
        pygame.draw.circle(ventana,yellow, (Xc,Yc),50,width=1)
        pygame.display.flip()
        pygame.mixer.Sound.play(sonidoexplode)

        time.sleep(0.5)
        pygame.draw.circle(ventana,black, (Xc,Yc),50,width=1)
        time.sleep(0.5)
        pygame.draw.circle(ventana,yellow, (Xc,Yc),100,width=1)
        pygame.display.flip()
        time.sleep(0.5)
        pygame.draw.circle(ventana,black,(Xc,Yc),100,width=1)
        time.sleep(0.5)
        pygame.display.flip()
        time.sleep(0.5)
        
        fuente = pygame.font.SysFont('times new roman', 60)
        gameover_surface = fuente.render('GAME OVER', True, yellow)
        gameover_rect = gameover_surface.get_rect()
        gameover_rect.midtop = (ANCHOP/2, ALTOP/2)
        #ventana.fill(black)
        ventana.blit(gameover_surface, gameover_rect)
        pygame.display.flip()
        marcador(Score)
        time.sleep(1)
        finaliza()

    dibunave01(Xc,Yc,black)
    dibudisparo01(Xd,Yd,black)
    
    Xc = Xc + dXc
    if Xc > ANCHOP:
        Xc = ANCHOP
    if Xc < 0:
        Xc = 0

    if Yd < 50:
        disparo = 0

    if disparo == 0:
        Xd = Xc
        Yd = Yc-H/2-L/2
  
    if disparo == 1: 
        Yd = Yd - saltodisparo


    contador = contador+5

    reloj.tick(fps)


