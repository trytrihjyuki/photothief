from utils import *
import random

def init(configs):
    pass

def run():
    configs = get_configs()
    init(configs)

    for i in range(configs['num_steps']):
        if i%100 == 0:
            loss = random.random()
            set_run_info({'loss': loss, 'step': i})
            simulate_algo(i)
            print('GOWNO W DUPIE')

if __name__ == '__main__':
    run()