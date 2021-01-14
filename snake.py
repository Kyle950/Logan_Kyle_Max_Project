import pygame,math,random
import numpy as np

black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
white=(255,255,255)
gray=(120,120,120)

space=0
body=1
head=2
apple=3

class game:

    def __init__(self,x,y):
        self.running=False
        self.x=x
        self.y=y
        self.bw=60
        self.w=x*self.bw
        self.h=y*self.bw
        self.center=(int(x/2),int(y/2))
        self.highscore=1
        self.steps=0
        self.matrix=[[space for _ in range(x)] for _ in range(y)]

    def start(self):
        pygame.init()
        self.clock=pygame.time.Clock()
        self.display=pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('AI Snake')
        self.font=pygame.font.Font('freesansbold.ttf',24)
        py=snake(self.center)
        self.player=py
        self.matrix[self.player.y][self.player.x]=head
        self.genApple()
        self.running=True
    
    def genApple(self):
        sp=[]
        for y in range(self.y):
            for x in range(self.x):
                if self.matrix[y][x]==space:
                    sp.append((x,y))
        self.apple=random.choice(sp)
        self.matrix[self.apple[1]][self.apple[0]]=apple

    def update(self):
        op=(self.player.x,self.player.y)
        self.player.move()
        pos=(self.player.x,self.player.y)
        self.matrix[op[1]][op[0]]=space
        self.matrix[pos[1]][pos[0]]=head
        if pos==self.apple:
            self.player.length+=1
            self.body.append(op)
        elif pos in self.player.body or pos[0]<0 or pos[0]==self.x or pos[1]<0 or pos[1]==self.y:
            self.running=False

    def draw(self):
        self.display.fill(black)
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if self.matrix[y][x]==head:
                    color=blue
                elif self.matrix[y][x]==body:
                    color=green
                elif self.matrix[y][x]==apple:
                    color=red
                else:
                    color=black
                pygame.draw.rect(self.display,color,(x*self.bw,y*self.bw,self.bw,self.bw))
        for x in range(self.x+1):
            pygame.draw.rect(self.display,gray,(x*self.bw-2,0,4,self.w))
        for y in range(self.y+1):
            pygame.draw.rect(self.display,gray,(0,y*self.bw-2,self.h,4))

        render=self.font.render('Score: '+str(self.player.length),True,white)
        self.display.blit(render,(10,10))

        render=self.font.render('Highscore: '+str(self.highscore),True,white)
        self.display.blit(render,(10,40))

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                raise SystemExit

        pygame.display.update()    

class snake:

    def __init__(self,pos):
        self.x,self.y=pos
        self.body=[]
        self.length=1
        self.dir=0

    def move(self):
        if self.body:
            for b in range(len(self.body)-1,0,-1):
                self.body[b]=self.body[b-1]
            self.body[0]=(self.x,self.y)
        if self.dir=='up':
            self.y-=1
        elif self.dir=='down':
            self.y+=1
        elif self.dir=='left':
            self.x-=1
        elif self.dir=='right':
            self.x+=1

def main():
    g=game(9,9)
    g.start()
    while g.running:
        g.draw()
        g.clock.tick(5)
        g.update()

if __name__=='__main__':
    main()