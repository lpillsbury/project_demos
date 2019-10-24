#!/usr/bin/env python3
#copyright 2018 Leah Pillsbury leahp@bu.edu


import sys
import numpy
import math

DEBUG=False

class Disk():
    "this class contains the information for the balls that move in infinite space and sometimes collide"
    #the only things in the Disk class are the object initialization, setitem, str and overload repr with str. all the other functions are separate since this is the only program using this class
    
    def __init__(self,disk): 
        "initialize the disk dictionary"
        self.ID=disk[0]
        self.pos=[0,0]
        self.vel=[0,0]
        self.pos[0]=disk[1] #x and y position coordinates
        self.pos[1]=disk[2]
        self.vel[0]=disk[3] #x and y velocities
        self.vel[1]=disk[4]

    def __setitem__(self, index, value):
        self.pos[index]=value
        self.vel[index]=value
        self.ID=value

    def __str__(self):
        return " p="+str(self.pos)+" v="+str(self.vel)

    __repr__ =__str__

"input and output functions. includes input error checking"

def get_timestamp():
    "get in timestamp from command line"
    timestamp=[]
    for i in range (1,len(sys.argv)):
        try:
            time=float(sys.argv[i])
        except:
            sys.exit(2)
        #check for negative timestamp values
        if time<0:
            continue
        else:
            timestamp.append(time)
    #check for empty timestamp
    if timestamp==[]:
        sys.exit(2)
    timestamp=sorted(timestamp)
    return(timestamp)

def process_input(all_inputs): 
    "read in all inputs as strings, put each name, xy position anelocity in its own object type Disk"
    "make an array of objects type Disk and return that"
    inlines=all_inputs.splitlines()
    all_disks=[]
    for singleline in inlines:
        fields=singleline.split()
        #check to make sure the four number inputs are number inputs and make them floats
        if len(fields)==5:
            for item in range(1,len(fields)):
                try:
                    fields[item]=float(fields[item])
                except ValueError:
                    sys.exit(1)  
 
            #make a list of objects each of type disk
            each_disk=Disk(fields)
            all_disks.append(each_disk)
        else:
            sys.exit(1) #exit code 2
    return(all_disks)
   
def print_output(time):
    print(time)
    for i in range(len(disk_list)):
        str_to_print=str(disk_list[i].ID)+" "+str(disk_list[i].pos[0])+" "+str(disk_list[i].pos[1])+" "+str(disk_list[i].vel[0])+" "+str(disk_list[i].vel[1])
        print(str_to_print)

"move and collision functions"
def will_collide(ind1,ind2):
    "this function returns dot product of difference between any two balls and says whether they are going towards each other"
    "they could go towards each other but never hit if they are going towards each other farther away from their radii"
    pos_diff=numpy.subtract(disk_list[ind1].pos, disk_list[ind2].pos)
    vel_diff=numpy.subtract(disk_list[ind1].vel,disk_list[ind2].vel)
    wc=numpy.dot(pos_diff,vel_diff)
    return wc

def calc_next_coll():
    "calculates when the next collision will be and returns that time"
    #calculate collision time pairwise for each 2 balls; save the lowest time see if its lower than last time
    #return the time of collision and which balls collided
    #what happens if 3 collide at same time? change momentum of 2 and then hit the third?
    length=len(disk_list)
    for z in range(len(disk_list)-1):
        #test whether there will even be a collision
        i=0
        j=1
        counter=0
        #initialize which_hit and possible_time to -1 so that if nothing real happens can return that nothing collided
        which_hit=-1
        possible_time=-1

        for i in range(len(disk_list)):
            for j in range(len(disk_list)):
                if i==j:
                    continue
                else: 
                    pos_diff=numpy.subtract(disk_list[i].pos, disk_list[j].pos)
                    vel_diff=numpy.subtract(disk_list[i].vel,disk_list[j].vel)
                    c=numpy.dot(pos_diff,pos_diff)-100
                    b=2*numpy.dot(pos_diff,vel_diff)
                    a=numpy.dot(vel_diff,vel_diff)
                    x=b**2-4*a*c
                    wc=will_collide(i,j)
                    #if DEBUG:
                        #print("i, j: ", i, j)
                        #print("a: ",a, "b: ", b, "c: ", c)
                        #print("x: ", x)
                    if (x>=0 and wc<0):
                        t1=(-b-math.sqrt(b**2-4*a*c))/(2*a)
                        #t2=float((-b-math.sqrt(b**2-4*a*c))/(2*a)) #don't care about second root
                        if (t1>0 or abs(t1)<1e-8):
                            if abs(t1)<1e-8:
                                t1=0
                            if (counter==0 or t1<possible_time):
                                possible_time=t1
                                which_hit=[i,j]
                            #if DEBUG:
                                #print("possible_time: ", possible_time)
                                #print("which_hit", which_hit)
                counter=counter+1
        return(possible_time,which_hit)

def move(time):
    "moves all the disks from their starting position to a final position time seconds later"
    for i in range(len(disk_list)):
        new_vcoords=[v*time for v in disk_list[i].vel]
        disk_list[i].pos[0]=disk_list[i].pos[0]+new_vcoords[0]
        disk_list[i].pos[1]=disk_list[i].pos[1]+new_vcoords[1]

def collision(which_hit):
    "computes transfer of momentum at collision at exactly the time of hit. no instantaneous position change"
    #new velocity first disk
    pos_diff=numpy.subtract(disk_list[which_hit[0]].pos, disk_list[which_hit[1]].pos)
    vel_diff=numpy.subtract(disk_list[which_hit[0]].vel,disk_list[which_hit[1]].vel)
    numerator=numpy.dot(vel_diff,pos_diff)
    denominator=numpy.dot(pos_diff,pos_diff)
    new_v1=disk_list[which_hit[0]].vel-numpy.dot((numerator/denominator),pos_diff)

    #new velocity second disk
    pos_diff=numpy.subtract(disk_list[which_hit[1]].pos, disk_list[which_hit[0]].pos)
    vel_diff=numpy.subtract(disk_list[which_hit[1]].vel,disk_list[which_hit[0]].vel)
    numerator=numpy.dot(vel_diff,pos_diff)
    denominator=numpy.dot(pos_diff,pos_diff)
    new_v2=disk_list[which_hit[1]].vel-numpy.dot((numerator/denominator),pos_diff)

    #save new velocities to global disk_list
    disk_list[which_hit[0]].vel=new_v1
    disk_list[which_hit[1]].vel=new_v2   

    if DEBUG:
        print("calculated the collision momentum trans for ball indices: ", which_hit)
        print("at master time: ", master_time)
     
#don't have a main so that all the variables declared here are global
"put all the entered timestamp values in timestamp array"
timestamp=get_timestamp()
"input IDs and initial positions and velocities for each disk"
"store them as an array of type disk"
#f=open("ball_test2.coordinates",'r')
#all_inputs=f.read() #this is for input testing from a file
#f.close()
all_inputs=sys.stdin.read() #this is for input from user
disk_list=process_input(all_inputs)  #global variable 

master_time=0 #master time running since the beginning rather than local time which is just amount of time since last action
if(len(disk_list)==1):
    "don't worry about collisions if there is only one disk"
    for i in range(len(timestamp)):
        move(timestamp[i]-master_time)
        print_output(timestamp[i])
        master_time=timestamp[i]

else:
    for i in range(len(timestamp)):
        "compare first collision time to timestamp. move to whichever action is first. if collision is first, "
        "collide and then see if more collisions before next timestamp"

        "calculate when next collision is and which balls hit"
        [collision_time,which_hit]=calc_next_coll() #return -1 for collision_time and which_hit if there isn't another collision before the next timestamp
        if DEBUG:
            print("collision time: ", collision_time)
            print("which hit: ", which_hit, "\n")

        #move to subsequent future collisions at different times or at the same time
        while((collision_time+master_time)<=timestamp[i] and collision_time>=0):
            #deal with collisions that happen at the same time:
            master_time=master_time+collision_time
            while(collision_time==0):
                collision(which_hit)
                [collision_time,which_hit]=calc_next_coll()
            if collision_time>0:
                move(collision_time)
                collision(which_hit)
                [collision_time,which_hit]=calc_next_coll()
        time_forward=float(timestamp[i]-master_time)
        if DEBUG:
            print("time_forward: ", time_forward)
            print("timestamp: ", timestamp[i])
            print("master time", master_time)
        move(time_forward)
        master_time=timestamp[i]
        print_output(timestamp[i])