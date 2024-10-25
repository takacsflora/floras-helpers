from pathlib import Path 
import numpy as np
import json

class Bunch(dict):
    """ taken from iblutil
    A subclass of dictionary with an additional JavaSrcipt style dot syntax."""

    def __init__(self, *args, **kwargs):
        super(Bunch, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def copy(self):
        """Return a new Bunch instance which is a copy of the current Bunch instance."""
        return Bunch(super(Bunch, self).copy())

    def save(self, npz_file, compress=False):
        """
        Saves a npz file containing the arrays of the bunch.

        :param npz_file: output file
        :param compress: bool (False) use compression
        :return: None
        """
        if compress:
            np.savez_compressed(npz_file, **self)
        else:
            np.savez(npz_file, **self)

    @staticmethod
    def load(npz_file):
        """
        Loads a npz file containing the arrays of the bunch.

        :param npz_file: output file
        :return: Bunch
        """
        if not Path(npz_file).exists():
            raise FileNotFoundError(f"{npz_file}")
        return Bunch(np.load(npz_file))
    
    
def save_dict_to_json(dict,path):
    """
    util function to save dictionaries to json
    """
    message = json.dumps(dict)
    errfile = open(path,"w")
    errfile.write(message)
    errfile.close()



def get_subfolders(folder_path):
    folder = Path(folder_path)
    subfolders = [subfolder for subfolder in folder.iterdir() if subfolder.is_dir()]
    return subfolders
