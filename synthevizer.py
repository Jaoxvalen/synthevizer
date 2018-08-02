import pconfig as cf
import generator as gen
import os
import sys
from tqdm import tqdm

def main():

    if len(sys.argv) < 2:
        print("missing a config file arg")
        print("example: systhevizer config.json")
        sys.exit()
    
    config_path = str(sys.argv[1])

    oconfig = cf.PConfig(config_path)

    for i in range(len(oconfig.tasks)):
        pathfolder = oconfig.output_folder +'task'+str(i)+'/'
        if not os.path.exists(pathfolder):
            os.mkdir(pathfolder)
        task = oconfig.tasks[i]
        for projection in task['projections']:
            print('Generating task '+str(i)+', Total:'+ str(task['number_per_proj'])+' '+projection+' maps')
            for nfig in tqdm(range(task['number_per_proj'])):
                ogenerator = gen.Generator()
                fig_name = 'map_'+projection+'_'+str(nfig)
                ogenerator.generate(projection, task, pathfolder, fig_name)


main()