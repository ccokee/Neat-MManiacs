from __future__ import print_function

import Racer

import neat
import numpy as np
import os
import pickle
import sys

import checkpoint_plus


actions_list = [0,1,2,3]

timeout_constant = 250
scale = 1
radius=3
random_seed = 20
display = False

best_genome = None
best_fitness = 0
checkpointer = None
stats = None
pop = None
racer = None

def eval_genome(genome, config):
  global pyboy, best_fitness, best_genome, racer
  net = neat.nn.FeedForwardNetwork.create(genome, config)
  
  inputs, x, y, realx = racer.reset()
  
  rightmost = realx
  timeout = timeout_constant
  current_frame = 0
  fitness = 0
  done = False
  
  while not done:
    
    inputs = inputs.flatten()
    output = net.activate(inputs)
    a = np.argmax(output)
    action = 0
    if (output[a] > 0):
      action = actions_list[a]

    inputs, xn, yn, realxn, caido = racer.step(action)
  
    if (realxn > rightmost):
      rightmost = realxn
      timeout = timeout_constant
        
    timeout = timeout - 1
    timeout_bonus = current_frame / 4

    fitness = rightmost - current_frame / 2
    
    if (rightmost > 6000):
      fitness = fitness + 1000

    if (timeout + timeout_bonus <= 0):
      fitness = -1
      break;
    
    current_frame = current_frame + 1
    
  if (fitness > best_fitness):
    best_fitness = fitness
    best_genome = genome
    print('best_fitness = {0}'.format(best_fitness))
  print('rightmost = {0}'.format(rightmost))
  
  return fitness


def eval_genomes(genomes, config):
  filename = 'neat-checkpoint'
  
  for genome_id, genome in genomes:
    print('genome[{0}].fitness = {1}'.format(genome_id, genome.fitness))
    
    if (genome.fitness == None):
      genome.fitness = eval_genome(genome, config)   
      ##checkpointer.save_checkpoint(pop, best_genome, stats, filename)
      print('genome[{0}].fitness = {1}'.format(genome_id, genome.fitness))
  
  if (checkpointer.current_generation % 5 == 0):
    checkpointer.save_checkpoint(pop, best_genome, stats, '{0}-{1}'.format(filename, checkpointer.current_generation))


def run():
  global pop, stats, best_genome, checkpointer, best_fitness, racer
  
  racer = Racer.Racer(scale, radius, random_seed)
  
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, 'config')
  config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path) 
  pop = neat.Population(config)
  stats = neat.StatisticsReporter()
  
  filename = 'neat-checkpoint'
  
  if (os.path.isfile(filename)):
    pop, stats =  checkpoint_plus.CheckpointerPlus.restore_checkpoint(filename)
    best_genome = pop.best_genome
    best_fitness = best_genome.fitness
    print('best_fitness = {0}'.format(best_fitness))
    
  pop.add_reporter(neat.StdOutReporter(True))
  pop.add_reporter(stats)
  checkpointer = checkpoint_plus.CheckpointerPlus()
  pop.add_reporter(checkpointer)
  
  winner = pop.run(eval_genomes)

  with open('winner', 'wb') as f:
    pickle.dump(winner, f)

  print(winner)

if __name__ == "__main__":
  if (not os.path.isfile('winner')):
    run()
