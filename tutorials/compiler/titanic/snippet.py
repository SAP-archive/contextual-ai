import os
import sys

import json
import pandas as pd
sys.path.append('../../../')


from xai.compiler.base import Configuration, Controller


def original():
    print("this is the original compiler")
    json_config = 'basic-report.json'
    controller = Controller(config=Configuration(json_config))
    print(controller.config)
    controller.render()
    print("[DONE] the original compiler")


def v2():
    print("this is the v2 compiler")
    # -- Read/load the working file --
    train_data_csv = pd.read_csv('train_data.csv')
    model_pkl = pd.read_pickle('model.pkl')

    # -- * Make sure the config json updated correct --
    json_config = 'basic-report-with-dataobject.json'
    with open(json_config) as file:
        config = json.load(file)

    controller = Controller(config=Configuration(config, locals()))
    controller.render()
    print("[DONE] the v2 compiler")

if __name__== "__main__":
  #original()
  v2()