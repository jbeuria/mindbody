from cmath import sqrt
import functools
from math import floor
import pygame
from pygame.locals import *
import random
import time,sys
import itertools

pygame.init()

def draw_grid():
    for y in range(0, m+1, 1):#horizontal lines
        pygame.draw.line(screen, BLACK, (left, y*cellw + top), (sw-right, y*cellw + top), 1)
    for x in range(0,n+1,1):#vertical lines
        pygame.draw.line(screen, BLACK, (x*cellw + left, top), (x*cellw  + left, sh-bottom), 1)

def draw_cell(i,j,color,off=[0,0]):
    pygame.draw.rect(screen,color, [left+ (j-1+off[1])*cellw, top+ (i-1+off[0])*cellw,cellw,cellw],0 )

def draw_geo(geo,colors=[],off=[0,0]):
    index=0
    for el in geo:
        if(len(colors)==0):
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            rgb = [r,g,b]
        else:
            rgb=colors[index]
        index+=1
        draw_cell(el[0],el[1],rgb,off)

def resetScreen():
    pygame.draw.rect(screen,bg, [0,0,sw,sh],0 )
    draw_grid()

def randomiseGeo(geo):
    new_geo=[]
    for el in geo:
        temp= random.choice(list(filter(lambda ele: new_geo.count(ele) == 0, grid)))
        new_geo.append(temp)
        #draw_cell(el[0],el[1],bg,center)
    
    #pygame.display.update()
    resetScreen()
    draw_geo(new_geo)
    return new_geo

def next_step(geo):
    nn = [(1,-1), (0,-1), (-1,-1),(-1,0),(-1,1),(0,1), (1,1), (1,0)]
    
    def gen_rand(el,new):
        n=random.choice(nn) 
        if new.count((el[0]+n[0], el[1]+n[1])) >0 or el[0]+n[0] <0 or el[1]+n[1] <0:
            return gen_rand(el,new)
        else:
            return (el[0]+n[0], el[1]+n[1])
    
    new_geo = []
    for el in geo:
        new_geo.append(gen_rand(el,new_geo))

    return new_geo

   
def dynamics(geo,colors=[],sim=(0.0,0.0)):

    geo_new=next_step(geo)
    sim_new=similarity(geo_new,geo_ref_pos)
    #if( sim_new < sim ):
    if(sim_new[0]< sim [0] ): # or sim_new[1] > sim [1]):
        return [geo,sim] #dynamics(geo,colors,sim)
    else:
        sim=sim_new
        resetScreen()
        draw_geo(geo_new,colors)
        return [geo_new,sim]

    #time.sleep(0.1)
    
def norm(x):
    val=0.0
    for el in x:
        val+=el*el
    return sqrt(val).real 


def similarity(x,y):
    sim=0.0
    
    xc=functools.reduce(lambda a,b: (a[0]+b[0],a[1]+b[1]), x)
    xc=[xc[0]/len(x), xc[1]/len(x)]

    yc=functools.reduce(lambda a,b: (a[0]+b[0],a[1]+b[1]), y)
    yc=[yc[0]/len(y), yc[1]/len(y)]

    x = [(a-xc[0],b-xc[1])  for (a,b) in x ]
    y = [(a-yc[0],b-yc[1])  for (a,b) in y ]

    """
    print(xc,yc)
    """
    xf=list(itertools.chain(*x))
    yf=list(itertools.chain(*y))

    if(len(xf) != len(yf)):
        return 0.0

    for i in range(0,len(xf)):
        sim += xf[i]* yf[i]
    
    sim = abs(sim/(norm(xf) * norm(yf)))
    distV= [e1-e2  for (e1, e2) in zip(xf, yf)]
    #if(sim > 0.999):
        #print(sim,norm(distV))
    return (sim, norm(distV))

########################################    
begin = pygame.time.get_ticks()
left=20; right=10; top=25; bottom=30; 
#m rows, n columns
m=60; n=70; cellw=10

sw=left+ right+ n*cellw
sh=top + bottom + m*cellw
ox = 0; oy = 0; 
center=[floor(m/2),floor(n/2)]
autorun=True

grid = [(x,y) for x in range(m) for y in range(n)] 
#########################
geo_ref=[(0,1),(0,-1),(0,0),(1,0),(-1,0)]
geo_ref_pos= list(map(lambda x: ( x[0]+center[0], x[1]+center[1] ), geo_ref))
colors=[]
for el in geo_ref:
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    rgb = (r,g,b)
    colors.append(rgb)
#########################
YELLOW = (255, 255, 55)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE=(255,255,255)
bg = (255, 255, 255)
#########################
# clock = pygame.time.Clock()
screen = pygame.display.set_mode((sw, sh))
screen.fill(bg)

draw_grid()
draw_geo(geo_ref,[],center)

geo_random=randomiseGeo(geo_ref)
hasStarted=False
step=0
geo_now=geo_random
sim_now=(0.0,0.0)
while True:
    # event = pygame.event.wait()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit(0)
        
    [geo_now,sim_now] = dynamics(geo_now,colors,sim_now)
    pygame.display.flip()  
    #step+=1
    
  

