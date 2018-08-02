import pdataset as ds
import pconfig as cf
import generator as gen

oconfig = cf.PConfig('config.json')
task = oconfig.tasks[0]

odataset = ds.PDataset(task['input_file'])

ogenerator = gen.Generator()
ogenerator.generate('merc', task, odataset,'','figure')