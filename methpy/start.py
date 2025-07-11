import os
import sys
def start ():

    """Creates directories used by MethPy"""
    #takes the path opened in the terminal
    script_path =  os.getcwd ()
    #creates all the directories used by other modules
    os.mkdir (os.path.join(script_path, "Input"))
    os.mkdir (os.path.join(script_path, "References"))
    os.mkdir (os.path.join(script_path, "Tables"))
    os.mkdir (os.path.join(script_path, "Output in word"))
    os.mkdir (os.path.join(script_path, "Output in txt"))
    os.mkdir (os.path.join(script_path, "Charts"))

    print ("End of initialization")

sys.modules[__name__] = start