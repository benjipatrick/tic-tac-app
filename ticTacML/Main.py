from Utils import *

args = dotdict({
    'iterations': 10,
    'episodes': 10,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxQueueLength': 200000,
    'mctsSims': 5,
    'arenaCompare': 40,
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('temp','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20
})

if __name__=="__main__":
    do = 'something'