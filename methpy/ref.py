from methpy.__init__ import Reference, create_reverse
import os
import sys

def ref ():

    """Creates and saves the txt file of the reference, both forward and reverse"""
    #generates a popup asking for the reference info
    reference = Reference ().response
    #converts the forward into upper case
    forward = reference["sequence"].upper ()
    reverse = ""

    #converts the forward reference into the reverse complement
    reverse, no_nucleotides_list = create_reverse (forward)

    #if there is a letter that is not a nucleotide it prints a warning
    if len (no_nucleotides_list) == 1:
        print ("There is a ", no_nucleotides_list[0], "in your references")
    elif len (no_nucleotides_list) > 1:
        print ("There are the following letters in your references: \n", no_nucleotides_list)

    #takes the reference directory from the current directory
    #creates the txt files and then saves them
    script_path = os.getcwd ()
    reference_path = os.path.join (script_path, "References")
    forward_file = os.path.join (reference_path, reference["name"] + "F.txt")
    reverse_file = os.path.join (reference_path, reference["name"] + "R.txt")

    #if there is another file with the same name, it adds a number at the end of the reference name
    number = 1
    name_file = str(reference["name"])
    if name_file != "" or forward != "":
        while os.path.isfile(forward_file) or os.path.isfile(reverse_file) == True:
            forward_file = os.path.join (reference_path, reference["name"] + "(" + str(number) + ")" + "F.txt")
            reverse_file = os.path.join (reference_path, reference["name"] + "(" + str(number) + ")" + "R.txt")
            name_file = name_file +"(" + str(number) + ")"
            number += 1 

        with open (forward_file, "x") as f:
            f.write (forward)

        
        with open (reverse_file, "x") as f:
            f.write (reverse)

        print ("Saved " + name_file)
    else: print ("You didn't write any name or sequence")

sys.modules[__name__] = ref