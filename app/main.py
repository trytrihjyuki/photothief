from utils import *
import random

import time

def init(configs):
    set_run_info({'loss': 0, 'step': 0, 'finished': False})

def run_algo():
    configs = get_configs()

    for i in range(configs['num_steps']):
        if i%100 == 0:
            time.sleep(2)
            loss = random.random()
            set_run_info({'loss': loss, 'step': i, 'finished': False})
            simulate_algo(i)
    set_run_info({'loss': loss, 'step': configs['num_steps'], 'finished': True})
# if __name__ == '__main__':
#     run()