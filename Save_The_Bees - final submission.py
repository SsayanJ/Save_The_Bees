import copy
import datetime
import math
import logging
import random
from collections import Counter
from types import new_class
from pprint import pprint
import sys
import ntpath
import os

# Team 2
# Members:
# POPPE, Alexander 
# BENHAIM, Jean-François 
# NGUYEN, Van Tien 
# BRAVO MARCIAL, David Raphael 

######## Classes

class Bee:
    def __init__(self, id_bee, max_weight):
        self.id_bee = id_bee
        self.max_weight = max_weight
        self.pollen = {}
        self.current_weight = 0
        self.mvts = []
        self.time = 0
        self.coordinates = None

    def add_mvt(self, hive, flower, pollen_weights):
        # print(hive.needed_pollen.items())
        for pol, amount in hive.needed_pollen.items():
            if amount > 0:
                # print(pol, amount)
                # print(pol in flower.available_pollen)
                # print(flower.available_pollen[pol] >= amount)
                # print(flower.available_pollen[pol] >= amount and self.current_weight + amount * pollen_weights[pol] <= self.max_weight)
                if flower.available_pollen[pol] >= amount and self.current_weight + amount * pollen_weights[pol] <= self.max_weight:
                    self.pollen[pol] = amount 
                    self.mvts.append(['G', flower.id_flower, pol, amount])
                    flower.available_pollen[pol] -= amount
                    self.current_weight += amount * pollen_weights[pol]
                
                # elif not self.pollen and flower.available_pollen[pol] >= 1 and self.current_weight + pollen_weights[pol] <= self.max_weight:
                #     self.pollen[pol] = 1
                #     self.mvts.append(['G', flower.id_flower, pol, 1])
                #     flower.available_pollen[pol] -= 1
                #     self.current_weight = pollen_weights[pol]
                    
                # else:
                #     return True
                elif flower.available_pollen[pol] >= 1 and self.current_weight + 1 * pollen_weights[pol] <= self.max_weight:
                    self.pollen[pol] = 1 
                    self.mvts.append(['G', flower.id_flower, pol, 1])
                    flower.available_pollen[pol] -= 1
                    self.current_weight += 1 * pollen_weights[pol]
                    
                    # if not len(self.pollen):
                    #     # if flower.available_pollen[pol] >= 1 and self.current_weight + 1 * pollen_weights[pol] <= self.max_weight:
                    #     # self.pollen[pol] = 1 
                    #     # self.mvts.append(['G', flower.id_flower, pol, 1])
                    #     # flower.available_pollen[pol] -= 1
                    #     # self.current_weight += 1 * pollen_weights[pol]
                    #     return True 
    
                # else:
                #     print('dlt')
                #     return True
        # if sum([pollen_weights[pol] for pol in self.pollen.keys()]) > 200:
        #     print('ERROR')
        # print(self.id_bee, [(pol, amount) for pol, amount in self.pollen.items()], [pollen_weights[pol] for pol in self.pollen.keys()], sum([pollen_weights[pol] for pol in self.pollen.keys()]))
        time_travel = distance(self, flower)
        self.coordinates = flower.coordinates
        time_travel += distance(self, hive)
        time_get_drop = 2*len(self.pollen)
        self.time = time_travel + time_get_drop
        self.coordinates = hive.coordinates 

        for pol, amount in self.pollen.items():
            self.mvts.append(['F', hive.id_hive, pol, amount])
            hive.needed_pollen[pol] -= amount
            # print(hive.neede_pollen[pol])

        self.pollen = {}
        self.current_weight = 0
        if sum([amount for pol, amount in hive.needed_pollen.items()]) == 0:
            return True
        else:
            return False
            # self.pollen[key] -= value
            # if self.pollen[key] == 0:
            #     self.pollen.pop(key)
                


    # def get_pollen(self, flower, pollen, pollen_weights, hive_id):
    #     for pol in pollen:
    #         new_weight = pollen_weights[pol]
    #         if new_weight + self.current_weight <= max_weight:
    #             self.current_weight += new_weight
    #             print(pol)
    #             self.mvts.append(f"{self.id_bee} G {flower.id_flower} {pol} 1")
    #             if pol in self.pollen:
    #                 self.pollen[pol] += 1
    #             else:
    #                 self.pollen[pol] = 1
    #             pollen.remove(pol)
        
    #     for key, value in self.pollen.items():
    #         self.mvts.append(f"{self.id_bee} F {hive_id} {key} {value}")
    #     return pollen

    def __repr__(self):
        return f"Bee({self.id_bee}, {self.max_weight}, {self.pollen}, {self.current_weight}, {self.mvts}, {self.time})"

class Hive:
    def __init__(self, id_hive, coordinates, needed_pollen, nb_needed_pollen, weight_sum):
        self.id_hive = id_hive
        self.coordinates = coordinates
        self.needed_pollen = dict(Counter(needed_pollen))
        self.needed_pollen_calc = dict(Counter(needed_pollen))
        self.nb_needed_pollen = nb_needed_pollen 
        self.nb_needed_pollen_calc = nb_needed_pollen
        self.weight_sum = weight_sum
        self.distance_flower = []
        self.providing_flowers = []
        self.provided = False
        self.total_distance = 0

    def drop_pollen(self, pollen):
        for pol in pollen:
            if pol in self.needed_pollen:
                # self.needed_pollen.remove(pol)
                self.needed_pollen[pol] = self.needed_pollen[pol] - 1
                if self.needed_pollen[pol] == 0 : del self.needed_pollen[pol]
        # self.nb_needed_pollen = len(self.needed_pollen)

    def __repr__(self):
        return f"Hive({self.id_hive}, {self.distance_flower}, {self.providing_flowers}, {self.provided}, {self.coordinates}, {self.needed_pollen}, {self.nb_needed_pollen}, {self.total_distance})"

class Flower:
    def __init__(self, id_flower, coordinates, available_pollen):
        self.id_flower = id_flower
        self.coordinates = coordinates
        self.available_pollen = {i:v for i,v in enumerate(available_pollen)}
        self.available_pollen_calc = {i:v for i,v in enumerate(available_pollen)}
        self.nb_available_pollen = len(available_pollen)
        
    def take_pollen(self, pollen):
        for pol in pollen:
            if pol in self.available_pollen:
                self.available_pollen.pop(pol)
        self.nb_available_pollen = len(self.available_pollen)

    def __repr__(self):
        return f"Flower({self.id_flower}, {self.coordinates}, {self.available_pollen}, {self.nb_available_pollen})"


######## Parser

def parse(filepath):
  dataset = {}
  with open(filepath, 'r') as fi:
    rows, columns, nb_bees, time_max, weight_max = map(int,fi.readline().split())

    bees = [Bee(bee_id, weight_max) for bee_id in range(nb_bees)]

    pollen_types = int(fi.readline().strip())
    pollen_weights = [int(weight.strip()) for weight in fi.readline().split()]
    nb_flowers = int(fi.readline().strip())
    flowers = []
    for flower_id in range (nb_flowers):
      coordinates = tuple([int(coordinate) for coordinate in fi.readline().split()])
      available_pollen = [int(polen) for polen in fi.readline().split()]
      flowers.append(Flower(flower_id, coordinates, available_pollen))
    
    coo = flowers[0].coordinates
    for bee in bees:
        bee.coordinates = coo

    hives = []
    nb_hives = int(fi.readline().strip())
    for hive_id in range (nb_hives):
      coordinates = tuple([int(coordinate) for coordinate in fi.readline().split()])
      nb_needed_pollen = int(fi.readline().strip())
      needed_pollen = [int(polen) for polen in fi.readline().split()]

      weight_sum = sum([pollen_weights[pollen] for pollen in needed_pollen])

      hives.append(Hive(id_hive=hive_id, 
                        coordinates=tuple(coordinates), 
                        needed_pollen= needed_pollen, 
                        nb_needed_pollen = nb_needed_pollen, weight_sum=weight_sum))

    dataset = {
      "grid" : (columns,rows), 
      "nb_bees" : nb_bees, 
      "bees" : bees,
      "time_max" : time_max,
      "weight_max" : weight_max,
      "nb_pollen_types" : pollen_types,
      "pollen_weights" : pollen_weights,
      "nb_flowers" : nb_flowers,
      "flowers" : flowers,
      "nb_hives" : nb_hives,
      "hives" : hives
      }
  return dataset


######## Write the output file
def writeFile(output_file, res):
    with open(output_file,'w') as writer:
        n = len(res)
        writer.write(str(n))
        writer.write("\n")

        for command in res:
            writer.write(' '.join(map(str, command)))
            writer.write('\n')


######## Checker

# Called by 'scoring_hive_based' when 'log_result'=True
#Logs score output  ---- WARNING requires a 'logs' folder
def writeLog(output_file,total_score,success_feed,hives,bees_timing):
    with open(output_file,'w') as writer:
       
        writer.write('TOTAL SCORE: '+str(total_score))
        writer.write("\n\n")
        # success_feed([slowest_bee,b.id_bee,h_id_hive,m,hive_score])

        writer.write('########### BEES STATS   ##########\n')
        for b in bees_timing:
            writer.write(f"Bee #{b[0]} worked {b[1]} and made following commands: 'G':{b[2]}   'F':{b[3]}   'W':{b[4]}   'D':{b[5]} ")
            writer.write('\n')
        writer.write('\n\n\n')
        writer.write('########### SUCCESSFUL FEEDS   ##########\n')
        for command in success_feed:
            writer.write(f'T={command[0]}: Bee #{command[1]} completed Hive #{command[2]} with {command[3]} --> {command[4]} Points')
            writer.write('\n')
    
        writer.write('\n\n\n')
        writer.write('########### INCOMPLETE HIVES  ##########\n')
        incomplete_hives=[h for h in hives  for p in h.needed_pollen.values() if p>0]
        complete_hives=[h for h in hives  for p in h.needed_pollen.values() if p==0]
        for h in incomplete_hives:
            writer.write(f'Hive #{h.id_hive}: ')
            writer.write(' '.join(map(str, [[k,v] for k,v in h.needed_pollen.items()])))
            writer.write('\n')

        # print status of hives
        writer.write('\n\n\n')
        writer.write('########### COMPLETED HIVES    ##########\n')
        for h in complete_hives:
            writer.write(f'Hive #{h.id_hive}: ')
            writer.write(' '.join(map(str, [[k,v] for k,v in h.needed_pollen.items()])))
            writer.write('\n')
            
# Scoring file, takes a dataset and scores it. Still under test.
# Result very close to the judge ones (P2: This scorer:74171 VS  Online Judge:74325)
def scoring_hive_based(bees,log_result=False):
    n=len(bees)
    if n==20:
        out_name='P2'
        check_dataset=parse('./Data/problem2.txt')    
    elif n==25:
        out_name='P1'
        check_dataset=parse('./Data/problem1.txt')    
    elif n==30:
        out_name='P3'
        check_dataset=parse('./Data/problem3.txt') 
    else:
        print('ERROR the number of bees does not match any of the file Problem1, Problem2, Problem3. Scoring cannot be used')
        return -1
    hives,flowers=check_dataset['hives'], check_dataset['flowers']
    pollen_weights=check_dataset['pollen_weights']
    weight_max=check_dataset['weight_max']
    hives_copy=copy.deepcopy(hives)
    time_max=check_dataset['time_max']

    # Check simulation time used by the solution and that no bees is overloaded or pick up impossible
    used_time=0
    slowest_bee=-1    
    bees_timing=[]
    for i,b in enumerate(bees):
        run_time=0
        bee_weight=0
        
        nb_feed,nb_gather,nb_wait,nb_drop=0,0,0,0
        current_loc=flowers[0]
        for m in b.mvts:
            # check the next location            
            if m[0] == 'G':
                nb_gather+=1
                next_loc=flowers[m[1]]
                bee_weight+=pollen_weights[m[2]] * m[3]
                if bee_weight>weight_max:
                    print(f'ERROR Bee #{i} is overloaded by mvt {m}, {bee_weight}/{weight_max} (bee_weight/weight_max)')
                # Check pollen is available
                if flowers[m[1]].available_pollen[m[2]]<m[3]:
                    print(f'ERROR Bee #{i} is trying to gather {m[3]} of pollen {m[2]} but only {flowers[m[1]].available_pollen[m[2]]} is available. this is mvt {m}')
                flowers[m[1]].available_pollen[m[2]]-=m[3]
            elif m[0] == 'D':
                nb_drop+=1
                next_loc=flowers[m[1]]
                bee_weight-=pollen_weights[m[2]]* m[3]
            elif m[0]=='F':
                nb_feed+=1
                next_loc=hives[m[1]]
                bee_weight-=pollen_weights[m[2]]* m[3]
            #add flying time to the 
           
            run_time+=element_distance(current_loc,next_loc)+1
            current_loc=next_loc
            if m[0]=='W':
                nb_wait+=1
                run_time+=int(m[1])
        bees_timing.append([b.id_bee,run_time,nb_gather,nb_feed,nb_wait,nb_drop])
        if used_time<run_time:   
            used_time=run_time
            slowest_bee=i
    print(f'Simulation time used {used_time}/{time_max} - Bee #{slowest_bee}')
    
    total_score=0
    success_feed=[]
    for h in hives_copy:
        delivering_bees=[]
        max_command=[]
        used_for_hive=False #
        # List all feeding for each hives
        for b in bees:
            used_for_hive=False
            for i,m in enumerate(b.mvts):
                if m[0]=='F' and m[1]==h.id_hive:
                    used_for_hive=True
                    curr_move=i
                    # delivering_bees.append(b)
                    # max_command.append(i)
                    try:
                        h.needed_pollen[m[2]]-=m[3]
                    except:
                        print('ERROR the pollen {} is not required by hive {} - bee {}'.format(m[2],h.id_hive,b.id_bee))
                        return -1
                    # print(m)
                    if h.needed_pollen[m[2]]<0:
                        print('ERROR hive {} does not need that much pollen {} - bee {}'.format(h.id_hive,m[2],b.id_bee))
                        return -1
            if used_for_hive:
                delivering_bees.append(b)
                max_command.append(curr_move)
        # Using all the bees delivering to this hive, if every need is fulfilled calculate the score
        
        if sum([v for _,v in h.needed_pollen.items() ])==0:
            success_bee=-1
            success_move=[]
            current_loc=flowers[0]
            slowest_bee_time=-1
            for i,b in enumerate(delivering_bees):
                run_time=0
                for j in range(max_command[i]+1):
                    # check the next location
                    m=b.mvts[j]
                    if m[0] in ['G','D']:
                        next_loc=flowers[m[1]]
                    elif m[0]=='F':
                        next_loc=hives[m[1]]
                    #add flying time to the 
                    run_time+=element_distance(current_loc,next_loc)+1
                    current_loc=next_loc
                    if m[0]=='W':
                        run_time+=int(m[1])
                if slowest_bee_time<run_time:   
                    slowest_bee_time=run_time
                    success_bee=b.id_bee
                    success_move=m

                # print(m, b.id_bee, run_time,element_distance(current_loc,next_loc))
            if slowest_bee_time>=0:                
                hive_score=math.ceil((time_max-slowest_bee_time)/time_max*100)
                total_score+=hive_score
            success_feed.append([slowest_bee_time,success_bee,h.id_hive,success_move,hive_score])
    now=datetime.datetime.now()
    success_feed=sorted(success_feed, key=lambda x: x[0])
    print(f'Hives Completed {len(success_feed)}/{len(hives)}  -- {len(success_feed)/len(hives)*100}%')
    if log_result: writeLog("./logs/Log_{:02d}{:02d}{:02d}{:02d}_{}_{}.txt".
                format(now.day, now.hour, now.minute, now.second, out_name,total_score),total_score,
                success_feed,hives_copy,bees_timing)

    return total_score

######## Tools

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# return the list of command from the list of bees
def get_mvts(bees):
    res = []
    for bee in bees:
        for mvt in bee.mvts:
            res.append([bee.id_bee] + mvt)
    return res


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def distance(elem1, elem2):
    return math.ceil(math.sqrt((elem1.coordinates[0] - elem2.coordinates[0])**2 + (elem1.coordinates[1] - elem2.coordinates[1])**2))


def calculate_distance(coord1, coord2):
    x_diff = abs(coord1[0]-coord2[0])
    y_diff = abs(coord1[1]-coord2[1])
    return int(math.ceil(math.sqrt((x_diff*x_diff) + (y_diff*y_diff))))
    
def element_distance(element1, element2):
    return calculate_distance(element1.coordinates, element2.coordinates)

def hives_per_amount_of_fetches(hives):
    hives_number_robee = {}

    for hive in hives:
        number = math.ceil(hive.weight_sum / bees[0].max_weight)
        if number in hives_number_robee:
            hives_number_robee[number].append(hive)
        else:
            hives_number_robee[number] = [hive]

    return hives_number_robee

def hives_sorted_fetch_flower(hives_number_robee, flowers):   
    hives_robees = []
    for x in range(1, len(hives_number_robee)):
        hives_x_robee = {}
        for hive in hives_number_robee[x]:
            min_flower = None
            min_d = 100000000
            for flower in flowers:
                if all([value >= flower.available_pollen[key] for key, value in hive.needed_pollen.items()]):
                    d = distance(flower, hive)
                    if d < min_d:
                        min_d = d
                        min_flower = flower
            if min_flower:
                idx = min_flower.id_flower
                hive.distance_flower = min_d
                if idx in hives_x_robee:
                    hives_x_robee[idx].append(hive)
                else:
                    hives_x_robee[idx] = [hive]
                for key, value in hive.needed_pollen.items():
                    min_flower.available_pollen[key] -= value
                    


        for key, value in hives_x_robee.items():
            value.sort(key=lambda x: x.distance_flower, reverse=False)
        hives_robees.append(hives_x_robee)
    return hives_robees

# sorts the hives per flower and every list in terms of distance
def hives_per_flower(hives):

    hives_per_flower = {}
    for hive in hives:
        min_flower = None
        min_d = 100000000
        for flower in flowers:
            d = distance(flower, hive)
            if d < min_d:
                min_d = d
                min_flower = flower

        idx = min_flower.id_flower
        if idx in hives_per_flower:
            hives_per_flower[idx].append(hive)
        else:
            hives_per_flower[idx] = [hive]
        hive.distance_flower = (idx, min_d)

            
    for key, value in hives_per_flower.items():
        value.sort(key=lambda x: x.distance_flower[1], reverse=False)

    return hives_per_flower

def sort_flowers_by_distance_per_hive(hives, flowers):
    for hive in hives:
        hive.distance_flower = []
        for flower in flowers:
            d = distance(hive, flower)
            hive.distance_flower.append((flower.id_flower, d))
        hive.distance_flower = sorted(hive.distance_flower, key=lambda x: x[1])

def list_flowers_provide(hives, flowers):
    for hive in hives:
        hive.provided = False
        hive.providing_flowers = []

        # for pol, amount in hive.needed_pollen_calc.items():
        #     for flowerid, d in hive.distance_flower:
        #         if flowers[flowerid].available_pollen_calc[pol] >= amount:
        #             hive.providing_flowers.append([flowerid, pol, amount])
        #             flowers[flowerid].available_pollen_calc[pol] -= amount
        #             hive.needed_pollen_calc[pol] -= amount
        #             hive.nb_needed_pollen_calc -= amount

        for flowerid, d in hive.distance_flower:
            for pol, amount in hive.needed_pollen_calc.items():
                if amount > 0:
                    # current_flower = None
                    current_index = 0
                    for index in range(len(flowers)):
                        if flowers[index].id_flower == flowerid:
                            current_index = index
                    # for flower in flowers:
                    #     if flower.id_flower == flowerid:
                    #         current_flower = flower
                    if flowers[current_index].available_pollen_calc[pol] >= amount:
                        hive.providing_flowers.append(['G', flowerid, pol, amount])
                        hive.providing_flowers.append(['F', hive.id_hive, pol, amount])
                        flowers[current_index].available_pollen_calc[pol] -= amount
                        hive.needed_pollen_calc[pol] -= amount
                        hive.nb_needed_pollen_calc -= amount


        # for flowerid, d in hive.distance_flower:
        #     for pol, amount in hive.needed_pollen_calc.items():
        #         if amount > 0:
        #             if amount <= flowers[flowerid].available_pollen_calc[pol]:
        #                 hive.providing_flowers.append(flowerid)
        #                 hive.needed_pollen_calc[pol] -= amount
        #                 hive.nb_needed_pollen_calc -= amount
        #                 flowers[flowerid].available_pollen_calc[pol] -= amount
        #                 # print(hive)
        if hive.nb_needed_pollen_calc == 0:
            hive.provided = True

def set_total_distance_travel(hives, flowers):
    # go back and forth also if same flower

    # for hive in hives:
    #     hive.total_distance = 0
    #     d = 2 * len(hive.providing_flowers)
    #     for flowerid in hive.providing_flowers:
    #         d += distance(hive, flowers[flowerid])
    #     hive.total_distance = d

    # assumption that everything from one flower can
    # be picked up at once
    
    for hive in hives:
        hive.total_distance = 0
        d = 2 * len(set(hive.providing_flowers))
        for flowerid in set(hive.providing_flowers):
            current_index = 0
            for index in range(len(flowers)):
                if flowers[index].id_flower == flowerid:
                    current_index = index
            d += 2 * distance(hive, flowers[current_index])
        hive.total_distance = d

######## Code

import glob
final_score = 0
for idx, filepath in enumerate(glob.glob('Data/*')):

    print(f"Processing: {filepath}")

    iterations = 1
    score = 0
    final_res = []
    best_seed = 0
    for i in range(iterations):

        filename = path_leaf(filepath[:-4])
        # dataset = parse(f"./Data/{filename}.txt")
        dataset = parse(filepath=filepath)
        current_seed = random.randint(0,100000)
        random.seed(current_seed)

        grid = dataset['grid']
        nb_bees = dataset['nb_bees']
        bees = dataset['bees']
        time_max = dataset['time_max']
        weight_max = dataset['weight_max']
        nb_pollen_types = dataset['nb_pollen_types']
        pollen_weights = dataset['pollen_weights']
        nb_flowers = dataset['nb_flowers']
        flowers = dataset['flowers']
        flowers_copy = copy.deepcopy(flowers)
        nb_hives = dataset['nb_hives']
        hives = dataset['hives']

        sort_flowers_by_distance_per_hive(hives, flowers)
        hives.sort(key=lambda x: (x.nb_needed_pollen), reverse=False)

        list_flowers_provide(hives, flowers)

        for hive in hives:
            if not hive.provided:
                print(hive)

        commands = []
        for hive in hives:
            commands.extend(hive.providing_flowers)
        logger.info(len(commands))

        bees = dataset['bees']
        temp_commands = []
        leftovers = []
        bee=bees[0]

        flow_0_index = 0
        for index in range(len(flowers)):
            if flowers[index].id_flower == 0:
                flow_0_index = index
        
        prev_loc=flowers[flow_0_index]
        while commands:
            
            gathers = []
            feeds = []
            over = False
            while (not over and commands):
                if commands:
                    tag, flower, pollen, number = commands[0]
                    
                    if (bee.current_weight + (number*pollen_weights[pollen])) <= weight_max:
                        gather = commands.pop(0)
                        feed = commands.pop(0)
                        gathers.append(gather)
                        feeds.append(feed)
                        bee.current_weight = bee.current_weight + (number*pollen_weights[pollen])
                        
                    elif number*pollen_weights[pollen] > weight_max:
                        # This is because these commands always have 2 pollen
                        commands[0][3] = 1
                        commands[1][3] = 1
                        commands.insert(0,commands[1])
                        commands.insert(0,commands[1])
                        tag, flower, pollen, number = commands[0]
                    
                        if (bee.current_weight + (number*pollen_weights[pollen])) <= weight_max:
                            gather = commands.pop(0)
                            feed = commands.pop(0)
                            gathers.append(gather)
                            feeds.append(feed)
                            bee.current_weight = bee.current_weight + (number*pollen_weights[pollen])
                        else:
                            # Bee is over weight
                            over = True
                    else:
                        # Out of commands
                        over = True
                        
            for _ in range(len(gathers)):
                current_gather=gathers.pop(0)
                bee.mvts.append(current_gather)
                current_flow_index = 0
                for index in range(len(flowers)):
                    if flowers[index].id_flower == current_gather[1]:
                        current_flow_index = index
                
                current_loc=flowers[current_flow_index]
                bee.time+=distance(prev_loc,current_loc)+1
                prev_loc=current_loc
            for _ in range(len(feeds)):
                current_feed=feeds.pop(0)
                bee.mvts.append(current_feed)
                current_loc=hives[current_feed[1]]
                bee.time+=distance(prev_loc,current_loc)+1
                prev_loc=current_loc
            bee.current_weight = 0
            bees_time=[b.time for b in bees]
            bee_counter=bees_time.index(min(bees_time)) 
            bee=bees[bee_counter]
            # Reset the bee weight
            bee.current_weight = 0
            
        logger.info(len(commands))
                
        if len(leftovers) > 0:        
            logger.warning(f"Unhandled commands: {len(leftovers)}")

        res = get_mvts(bees)
        new_score=scoring_hive_based(bees)
        # print(f"Current try: {i}, Temp score: {new_score}")

        if new_score > score:
            final_res = res
            score = new_score
            best_seed = current_seed
    
    final_score += score

    try:
        os.makedirs('result')
    except OSError as e:
        pass

    now = datetime.datetime.now()
    print(f"Best score: {score}, seed: {best_seed}\n")
    writeFile("./result/out_{:02d}{:02d}{:02d}{:02d}_{}_{}.txt".format(now.day, now.hour, now.minute, now.second, filename,score),res)

print(f"Final score: {final_score}")
