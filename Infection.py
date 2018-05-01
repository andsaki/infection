from tkinter import *
import time,random

pixel = 8
w = 7
h = 5
FIELD_X,FIELD_Y = w*pixel,h*pixel
width = FIELD_X*pixel
height = FIELD_Y*pixel
tk = Tk()
canvas = Canvas(tk,width=FIELD_X*pixel,height=FIELD_Y*pixel)
canvas.pack()


class World:
    def __init__(self):
        self.players = []
        self.infections = []
        self.play_posi = []
        self.count = 0
        self.vaccines = set()
        self.vaccine = Vaccine(self)

        

    def check_vaccines(self,x,y):
        if (x,y) in self.vaccines:
            return True
        else:
            return False
        
        

    def add_survivor(self,Class,x,y,state):
        if state == "uninfection":
            self.players.append(Class(x,y,state,self))
        else:
            self.infections.append(Class(x,y,state,self))
        
        

    def step(self):

        self.count = self.count + 1
        
        infec_posi = []
        self.play_posi = []
        for infec in self.infections:
            infec_posi.append((infec.x, infec.y))

        for player in self.players:
            self.play_posi.append((player.x, player.y))
        
        for player in self.players:
            if (player.x, player.y) in infec_posi:
                print("get!")
                player.state = "infection"
                self.infections.append(player)
                self.players.remove(player)

        for infec in self.infections:
            if (infec.x, infec.y) in self.vaccines:
                print("cure!")
                infec.state = "uninfection"
                self.players.append(infec)
                self.infections.remove(infec)
                self.vaccines.remove((infec.x, infec.y))
                
    
        for player in self.players:
            player.move()
        for infec in self.infections:
            infec.move()

        if self.count%100 == 0:
            self.vaccine.create_vaccine()
            self.vaccine.create_vaccine()

        
        self.vaccine.show()
        print("感染者: {}".format(len(self.infections)))
        print("非感染者: {}".format(len(self.players)))
                
                
        for player in self.players:
            player.color = "black"
            player.render()

        for infec in self.infections:
            infec.color = "red"
            infec.render()


        
        tk.update()
        tk.update_idletasks()
        canvas.delete("all")
        time.sleep(0.04)

    def start(self,n_steps): 
        
        self.add_survivor(Player,40,35,"uninfection")
        self.add_survivor(Player,10,10,"uninfection")
        self.add_survivor(Player,0,150,"uninfection")
        self.add_survivor(Player,13,130,"uninfection")
        self.add_survivor(Player,129,0,"uninfection")
        self.add_survivor(Player,45,15,"uninfection")
        self.add_survivor(Player,10,100,"uninfection")
        self.add_survivor(Player,100,150,"uninfection")
        self.add_survivor(Player,123,190,"uninfection")
        self.add_survivor(Player,123,10,"uninfection")
        self.add_survivor(Player,300,190,"infection")
        for x in range(n_steps):
            self.step()

    def chase_players(self,x,y):
        if (x,y) in self.play_posi:
            return True
        else:
            return False       

   

class Abstractperson:
    def __init__(self,x,y,state,world):
        self.x, self.y = x, y
        self.vx, self.vy = 1, 1
        self.world = world
        self.state = state
        self.color = "black"
        self.chase = "standard"
        

    def move(self):
        self.change_dir()
        self.x = (self.x + self.vx)%FIELD_X
        self.y = (self.y + self.vy)%FIELD_Y
        

    def change_dir(self):
        raise NotImplementedError("subclass responsibility")

    def render(self):
        canvas.create_rectangle(self.x*8, self.y*8,
                                self.x*8+8, self.y*8+8, fill = self.color, outline = self.color)

    def __str__(self):
        return "{}:pos =({}, {})".format(self.__class__.__name__,
                                         self.x, self.y) 


class Player(Abstractperson):
    def __init__(self,x,y,state,world):
        super(Player,self).__init__(x,y,state,world)

    def search_players(self):
        to_check = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        for x in to_check:
            check_x = (self.x + x[0])%FIELD_X 
            check_y = (self.y + x[1])%FIELD_Y
            if self.world.chase_players(check_x,check_y):
                return x
        return -1

    def change_dir(self):
        if self.state == "uninfection":
            
            self.uninfection()
                

        elif self.state == "infection":
            infec_dir = self.search_players()

            if infec_dir != -1:
                r1 = random.random()
                if r1 < 0.9:
                    self.vx = infec_dir[0]
                    self.vy = infec_dir[1]
                    r2 = random.random()
                    if self.chase == "chase":
                        self.vx = 2*infec_dir[0]
                        self.vy = 2*infec_dir[1]
                        self.infec_chase()
                        
                    if r2 < 0.1:
                        self.chase = "chase"
                        self.vx = 2*infec_dir[0]
                        self.vy = 2*infec_dir[1]


                else:
                    self.infec_chase()
                        
            else:
                self.infec_chase()
                
                
    
        
    def uninfection(self):
        dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        ind=dirs.index((self.vx,self.vy))
        r=random.random()
        if r<0.2:
            if r<0.1:
                newInd=(ind+1)%8
            else:
                newInd=(ind-1)%8
        else:
            newInd=ind
        self.vx,self.vy = dirs[newInd]
        
    def infection(self):
        dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        ind=dirs.index((self.vx,self.vy))
        r=random.random()
        if r<0.55:
            if r<0.5:
                newInd=(ind+1)%8
            else:
                newInd=(ind-1)%8
        else:
            newInd=ind
        self.vx,self.vy = dirs[newInd]

        
            
    def infec_chase(self):
        if self.chase == "standard":
            self.infection()

        elif self.chase == "chase":
            self.vx = self.vx/2
            self.vy = self.vy/2
            self.chase = "standard"
            self.infection()

    

    def render(self):
        canvas.create_rectangle(self.x*8, self.y*8,
                                self.x*8+8, self.y*8+8, fill = self.color, outline = self.color)


class Vaccine:
    def __init__(self,world):
        self.world = world
        

    def show(self):
        for A in self.world.vaccines:
            canvas.create_rectangle(A[0]*pixel,A[1]*pixel,
                               A[0]*pixel+pixel,A[1]*pixel+pixel,outline="pink",fill="pink")

    def remove(self,x,y):
        if (x,y) in self.world.vaccines:
                self.vaccines.remove((x,y))

    def create_vaccine(self):
        xr = random.randint(0,width)%FIELD_X
        yr = random.randint(0,height)%FIELD_Y
        
        self.world.vaccines.add((xr,yr))
        
        

        
        
world = World()
world.start(10000)
