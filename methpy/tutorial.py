from methpy.__init__ import create_reverse, right_position_sequence, seq_demethylated 
import os
import sys

def tutorial ():
    """Generates sequences and references to use as a tutorial"""
    #takes the path opened in the terminal
    script_dir =  os.getcwd ()
    #creates folders where the sequences are going to be saved
    os.mkdir (os.path.join (script_dir, "Input", "Sequence tutorial"))
    #this is the forward reference
    ref_forward = 'CACTAGTCCTGGGCTCCGGCACCAATTCCCCAACACAATCGTTCCCAAACTGCCTCCCTCCTATTACATTCACGCGTGAAAGGGACCTCGTCAATGCCTCGCATGTGTCCTGCTGCCCACAGTCCAGTCCAGGGCCTCCAACCAGCTCCGATGGCGTCCTATCGAGCCGATTTCAGTCCATTCCCGCATACGTCGTGGCC'
    
    #creation of the reverse reference
    ref_reverse = ""
    ref_reverse = create_reverse (ref_forward)[0]
    #takes the path of reference folder and saves the forward reference as a txt
    path_references = os.path.join (os.getcwd (), "References")
    file_forward = os.path.join (path_references, "TutorialF.txt") 

    with open (file_forward, "w") as f:
        f.write (ref_forward)

    #saves the reverse reference as a txt
    file_reverse = os.path.join (path_references, "TutorialR.txt")

    with open (file_reverse, "w") as f:
        f.write (ref_reverse)
    
    path_seq_tutorial = os.path.join (os.getcwd (), "Input", "Sequence tutorial")

    #creates the first sequence
    seq_tutorial_1F = ref_forward [31:156]
    path_seq_tutorial_1F = os.path.join (path_seq_tutorial, "Tutorial_1F.seq")
    path_seq_tutorial_1R = os.path.join (path_seq_tutorial, "Tutorial_1R.seq")
    #position with methylated Cs
    meth_1 = [45, 54, 57, 58, 60, 67, 71, 73, 86, 92, 98, 100, 110, 116, 120]
    #position with hemy metilated Cs 
    hemi_meth_1 = [113]

    #calculate the position of Cs to the sequence itself
    meth_1 = right_position_sequence (meth_1, 31)
    hemi_meth_1 = right_position_sequence (hemi_meth_1, 31)

    #create the sequence with Ts in the position of non methylated Cs
    seq_tutorial_1F = seq_demethylated (seq_tutorial_1F, meth_1)
    #change a T with a C where it is hemi methylated
    seq_tutorial_1F_emimethylated = seq_tutorial_1F [:hemi_meth_1[0]] + "C" + seq_tutorial_1F [hemi_meth_1[0]+1:]

    #creates a reverse with the "hemimethylated" sequence -> the reverse will have a C in the position where the F-R will be hemi methylated
    seq_tutorial_1R = create_reverse (seq_tutorial_1F_emimethylated)[0]

    #creates errors: 
    #in the forward there is an insertion of a T
    #in the reverse there is a base change
    seq_tutorial_1F = seq_tutorial_1F [:33] + "T" + seq_tutorial_1F [33:] 
    seq_tutorial_1R = seq_tutorial_1R [:12] + "C" + seq_tutorial_1R [13:]

    #saves both forward and reverse
    with open (path_seq_tutorial_1F, "w") as f:
        f.write (seq_tutorial_1F)
    with open (path_seq_tutorial_1R, "w") as f:
        f.write (seq_tutorial_1R)

    #second sequence
    seq_tutorial_2F = ref_forward [9:181]
    path_seq_tutorial_2F = os.path.join (path_seq_tutorial, "Tutorial_2F.seq")
    path_seq_tutorial_2R = os.path.join (path_seq_tutorial, "Tutorial_2R.seq")

    meth_2 = [45, 46, 53, 54, 57, 71, 86, 92, 98, 102, 110, 116, 120]
    hemi_meth_2 = [100, 113]

    meth_2 = right_position_sequence (meth_2, 9)
    hemi_meth_2 = right_position_sequence (hemi_meth_2, 9)

    seq_tutorial_2F = seq_demethylated (seq_tutorial_2F, meth_2)

    seq_tutorial_2F_emimethylated = seq_tutorial_2F [:hemi_meth_2[0]] + "C" + seq_tutorial_2F [hemi_meth_2[0]+1:hemi_meth_2[1]] + "C" + seq_tutorial_2F [hemi_meth_2[1]+1:]
    seq_tutorial_2R = create_reverse (seq_tutorial_2F)[0]

    #errors:
    #in the forward there is a base deletion
    #in the reverse there is an insertion of a C
    seq_tutorial_2F_emimethylated = seq_tutorial_2F_emimethylated [:80] + seq_tutorial_2F_emimethylated [81:] 
    seq_tutorial_2R = seq_tutorial_2R [:31] + "C" + seq_tutorial_2R [31:] 

    with open (path_seq_tutorial_2F, "w") as f:
        f.write (seq_tutorial_2F_emimethylated)
    with open (path_seq_tutorial_2R, "w") as f:
        f.write (seq_tutorial_2R)

    #third sequence
    seq_tutorial_3F = ref_forward [10:173]
    path_seq_tutorial_3F = os.path.join (path_seq_tutorial, "Tutorial_3F.seq")
    path_seq_tutorial_3R = os.path.join (path_seq_tutorial, "Tutorial_3R.seq")

    meth_3 = [45, 50, 54, 57, 58, 71, 86, 87, 89, 92, 98, 100, 113, 120]
    no_data_3 = [16, 20]

    meth_3 = right_position_sequence (meth_3, 10)
    no_data_3 = right_position_sequence (no_data_3, 10)

    seq_tutorial_3F = seq_demethylated (seq_tutorial_3F, meth_3)
    seq_tutorial_3F = seq_tutorial_3F [:no_data_3[0]] + seq_tutorial_3F [(no_data_3[0]+1):no_data_3[1]] + seq_tutorial_3F [(no_data_3[1]+1):]
    seq_tutorial_3R = create_reverse (seq_tutorial_3F)[0]

    #errors:
    #in the forward there is a base deletion
    #in the reverse there is a base change
    seq_tutorial_3F = seq_tutorial_3F [:80] + seq_tutorial_3F [81:]
    seq_tutorial_3R = seq_tutorial_3R [:66] + "A" + seq_tutorial_3R [67:]

    #it saves the forward as it is a reverse
    #and it saves the reverse as it is a forward
    with open (path_seq_tutorial_3R, "w") as f:
        f.write (seq_tutorial_3F)
    with open (path_seq_tutorial_3F, "w") as f:
        f.write (seq_tutorial_3R)

    #fourth sequence
    seq_tutorial_4F = ref_forward [9:192]
    path_seq_tutorial_4F = os.path.join (path_seq_tutorial, "Tutorial_4F.seq")
    path_seq_tutorial_4R = os.path.join (path_seq_tutorial, "Tutorial_4R.seq")

    meth_4 = [45, 54, 57, 71, 86, 92, 98, 113]
    hemi_meth_4 = [120]

    meth_4 = right_position_sequence (meth_4,9)
    hemi_meth_4 = right_position_sequence (hemi_meth_4,9)

    seq_tutorial_4F = seq_demethylated(seq_tutorial_4F, meth_4)

    for each in hemi_meth_4:
        seq_tutorial_4F_emimethylated = seq_tutorial_4F [:each] + "C" + seq_tutorial_4F [each+1:]

    seq_tutorial_4R = create_reverse (seq_tutorial_4F)[0]

    #errors:
    #in the forward both a change base and a deletion
    #in the reverse both a deletion of a cytosine and a insertion
    seq_tutorial_4F_emimethylated = seq_tutorial_4F_emimethylated [:76] + "G" + seq_tutorial_4F_emimethylated [77:] 
    seq_tutorial_4F_emimethylated = seq_tutorial_4F_emimethylated [:121] + seq_tutorial_4F_emimethylated [122:]
    seq_tutorial_4R  = seq_tutorial_4R [:43] + seq_tutorial_4R [44:] 
    seq_tutorial_4R = seq_tutorial_4R [:96] + "C" + seq_tutorial_4R [96:] 

    with open (path_seq_tutorial_4F, "w") as f:
        f.write (seq_tutorial_4F_emimethylated)
    with open (path_seq_tutorial_4R, "w") as f:
        f.write (seq_tutorial_4R)

    #fifth sequence
    seq_tutorial_5F = ref_forward [14:156]
    path_seq_tutorial_5F = os.path.join(path_seq_tutorial, "Tutorial_5F.seq")
    path_seq_tutorial_5R = os.path.join(path_seq_tutorial, "Tutorial_5R.seq")

    meth_5= [45, 54, 57, 58, 60, 71, 86, 92, 98, 113, 120]
    no_data_5=[23, 143]

    meth_5 = right_position_sequence(meth_5, 14)
    no_data_5 = right_position_sequence(no_data_5, 14)

    seq_tutorial_5F = seq_demethylated(seq_tutorial_5F, meth_5)

    #errors:
    #in the forward both a change base and a deletion of a cytosine (both present also in the reverse)
    #in the reverse there is also an insertion of an A and it ends with a part not present in the reference
    seq_tutorial_5F = seq_tutorial_5F [:no_data_5[0]] + "G" + seq_tutorial_5F [no_data_5[0]+1:]
    seq_tutorial_5F = seq_tutorial_5F [:no_data_5[1]] + seq_tutorial_5F [no_data_5[1]+1:]

    seq_tutorial_5R = create_reverse (seq_tutorial_5F)[0]
    seq_tutorial_5F_longer = seq_tutorial_5F + "AAAATCAAATGCAAAAA"

    seq_tutorial_5R = seq_tutorial_5R [:112] + "A" + seq_tutorial_5R [112:] 

    with open (path_seq_tutorial_5F, "w") as f:
        f.write (seq_tutorial_5F_longer)
    with open (path_seq_tutorial_5R, "w") as f:
        f.write (seq_tutorial_5R)
    print ("Tutorial created")

sys.modules[__name__] = tutorial
