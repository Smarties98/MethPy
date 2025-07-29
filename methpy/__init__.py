import os
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.colorchooser import askcolor
import methpy
import os
import sys
import json

def create_reverse (sequence):
    #given a forward sequence, it creates a reverse
    sequence_reverse = ""
    no_nucleotide = []
    for i in sequence:
        if i == "A":
            sequence_reverse = "T" + sequence_reverse
        elif i == "C":
            sequence_reverse = "G" + sequence_reverse
        elif i == "G":
            sequence_reverse = "C" + sequence_reverse
        elif i == "T":
            sequence_reverse = "A" + sequence_reverse 
        else:
            sequence_reverse = i + sequence_reverse
            no_nucleotide.append(i)

    return sequence_reverse,no_nucleotide

def right_position_sequence (position_in_reference, start_sequence):
    #given some positions in the reference and the first position of a sequence it calculates the positions in the sequence
    right_position = []
    for i in position_in_reference:
        right_position.append (i-start_sequence-1)
    return right_position

def seq_demethylated (sequence, position_methylated):
    #given a sequence and positions of methylated Cs
    #it returns the sequence with Cs where they are methylated and Ts where they are not
    for each in range (len(sequence)):
        #to check where there's a position non methylated
        if each not in position_methylated and (sequence[each] == "C"):
            #changes that position with a T
            sequence = sequence [:each] + "T" + sequence [each+1:]
    return sequence

class Reference:
    def __init__ (self):
        
        self.response = {"name":"", "sequence":""}
        #the popup takes the name and sequence of the reference
        def save ():
            self.response ["name"] = entry_name.get ()
            self.response ["sequence"] = entry_sequence.get ()

            if sys.platform.startswith ('darwin'): 
                popup.quit ()
            else: popup.destroy ()

        #popup characteristics
        if sys.platform.startswith ('darwin'): 
            font = ("", 15)
        else: font = ("", 13)
        popup = tk.Tk ()
        popup.geometry ("600x150")
        popup.title ("References creation")
        label_name = ttk.Label (popup, text = "Reference name", font = font)
        label_name.grid (row = 0, column = 0, padx = 10, pady = 10, ipadx = 10)
        entry_name = ttk.Entry (popup)
        entry_name.grid (row = 0, column = 1, padx = 10, pady = 10, ipadx = 80)
        label_sequence = ttk.Label (popup, text = "Reference sequence", font = font)
        label_sequence.grid (row = 1, column = 0, padx = 10, pady = 10, ipadx = 10)
        entry_sequence = ttk.Entry (popup)
        entry_sequence.grid (row = 1, column = 1, padx = 10, pady = 10, ipadx = 80)
        save_button = ttk.Button (popup, text = "Save", width = 10, command = save)
        save_button.place (rely = 0.75,relx = 0.5, anchor = "center")
        if sys.platform.startswith ('darwin'): 
            popup.destroy ()

        tk.mainloop ()

#to check all the positions where a substring is present
def find_all (string, substring): 
    position = 0
    list_positions = []
    list_positions_table = [] 

    while position < len (string):
        #takes a substring as a new string
        new_string = string [position:]
        #check in the new string if it finds the substring
        indeces = new_string.find (substring)
        #if it doesn't find anything, there is a break
        if indeces == -1:
            break
        else:
            #takes the position found
            to_add = position + indeces
            to_add_table = position + indeces + 1 
            #position is a new one that excludes where the substring was found
            position = position + indeces + 1
        list_positions.append (to_add)
        list_positions_table.append (to_add_table)
    return list_positions, list_positions_table

#takes gene name and sequence to analyze
class Gene_name:

    def __init__ (self):
        #takes all the references to shown them into a drop down menu
        script_path = os.getcwd ()
        reference_path = os.path.join (script_path,"References")
        list_reference = os.listdir (reference_path)
        list_without_FRtxt = []

        #takes the reference names
        for i in list_reference:
            if i.find ("F.txt") != -1:
                new_i = i.replace ("F.txt", "")
            elif i.find ("R.txt") != -1:
                new_i = i.replace ("R.txt", "")

            list_without_FRtxt.append (new_i)
            list_without_FRtxt = list (dict.fromkeys(list_without_FRtxt))
        
        #takes the input path
        input_path = os.path.join (script_path,"Input")
        self.response = {}
        
        #searches for the sequence to analyze
        def open_window ():
            seq_path = filedialog.askopenfilename (initialdir = input_path, title = "Select the sequence to analyze")
            entry.delete (0, tk.END)
            entry.insert (0, seq_path)
 
        def enter():
            self.response ["reference"] = clicked.get ()
            self.response ["file"] = entry.get ()
            root.destroy () 
        
        #popup characteristics
        root = tk.Tk ()
        if sys.platform.startswith ('darwin'): 
            font = ("", 15)
        else: font = ("", 13) 
        root.geometry ("730x130")
        root.title ("Choose the sequence to analyze")
        label_name = tk.Label (root, text = "Gene name", font = font)
        label_name.grid (row = 0, column = 0, padx = 10, pady = 10, ipadx = 10)
        clicked = tk.StringVar ()
        list_without_FRtxt.insert (0, "Select")
        drop = ttk.OptionMenu (root, clicked, *list_without_FRtxt)
        drop.place (x = 340, y = 22, anchor="center")
        entry = ttk.Entry (root)
        entry.grid (row = 1, column = 1, padx = 10, pady = 10, ipadx = 80)
        label_sequence = ttk.Label (root, text = "Path of the sequence", font = font)
        label_sequence.grid (row = 1, column = 0, padx = 10, pady = 10, ipadx = 10)
        button_path = ttk.Button (root, text = "Search", width = 10, command = open_window)
        button_path.grid (row = 1, column = 2, padx = 10, pady = 10, ipadx = 10)
        button = ttk.Button (root, text = "Enter", width = 10, command = enter)
        button.place (rely = 0.75,relx = 0.5, anchor = "center")

        tk.mainloop ()

#takes the forward and reverse of the reference, the sequence along the range of lenght to check
def find_start (reference_forward, reference_reverse, sequence, number):

    #creates the popup to check if there is the right start
    class StartSequence: 

        def __init__(self):
            self.response = {"stop":""}
    
            #if the start is right, the popup closes and goes on with the check
            def right():
                right_start = sequence [position_to_use]
                self.response ["button"] = right_start
                self.response ["stop"] = True
                self.response ["position_to_use"] = position_to_use
                self.response ["reference_position"] = reference_position
                root.quit ()
            
            #if it is the wrong start, the popup closes and it checks for another possible start
            def wrong ():
                root.quit ()

            #if you cannot find a start, it just closes everything and prints a warning
            def start_not_found ():
                self.response ["button"] = "Start not found"
                self.response ["stop"] = True
                root.quit ()

            m = position_to_use
            n = reference_position
            check = ""

            #65 are the nucleotides shown in the popup that asks for the right start
            for i in range (65):
                #checks if between sequence and reference the bases are the same, or if they can be the result of the bisulfite assay convertion
                if  ((m+i) < (len(sequence))) and ((n+i) < (len(reference))) and ((sequence[m+i] == reference[n+i]) or (reference == reference_forward and sequence[m+i] == "T" and reference[n+i] == "C") or (reference == reference_reverse and sequence[m+i] == "A" and reference[n+i] == "G")):
                    #if they are the same, it adds an X
                    check = check + "X"
                #otherwise it adds a blank space
                else: check = check + " "

                #counts how many X there are
                right_count = check.count ("X")
                #the first line of the popup is a part of the sequence
                first_line = "Sequence " + sequence [m:m+65] 

                #the second line of the popup is a part of the reference
                if reference == reference_forward:
                    second_line = "Forward  " + reference [n:n+65]
                elif reference == reference_reverse:
                    second_line = "Reverse  " + reference [n:n+65]

                #the third line is an X where the nt are the same
                third_line = 9*" " + check
                #the forth line is how many nucleotide are the same of the 65 visualized
                fourth_line = str (right_count) + "/65"
                
                #to add spaces where needed
                if len(first_line) == len (second_line):
                    text = first_line + "\n" + second_line + "\n" + third_line + "\n" + fourth_line
                else:
                    spaces = len (second_line) - len (first_line)
                    text =  first_line + spaces*" " + "\n" + second_line +  "\n" +third_line+ "\n" +fourth_line


            #if there are more than 40 Xs, it shows the popup
            #this is to exclude when reference and sequence are not very similar
            if right_count > 40 :  

                root = tk.Tk ()
                root.geometry ("830x150")
                root.wm_title ("Is this the right start?")
                if sys.platform.startswith ('darwin'): 
                    font = ("Courier New", 16)
                else: font = ("Courier New", 13)       
                label = tk.Label (root, text = text, font = font)
                label.grid (row = 0, column = 0, padx = 10, pady = 10, ipadx = 20)
                style_b1 = ttk.Style()
                style_b1.configure ("B1.TButton", foreground = "green")
                button1 = ttk.Button (root, text = "Yes", width = 10, command = right, style = "B1.TButton")
                button1.place (rely = 0.75, relx = 0.25, anchor = "center")
                style_b2 = ttk.Style ()
                style_b2.configure ("B2.TButton" , foreground = "red")
                button2 = ttk.Button (root, text = "No", width = 10, command = wrong, style = "B2.TButton")
                button2.place (rely = 0.75, relx = 0.75, anchor = "center" )
                style_b3 = ttk.Style()
                style_b3.configure ("B3.TButton" , foreground = "black")
                button3 = ttk.Button (root, text = "Cannot find the start", command = start_not_found, style = "B3.TButton")
                button3.place (rely = 0.75, relx = 0.5, anchor = "center")

                tk.mainloop ()
                root.destroy ()

    try: 
        #it checks a range of 10nt at the start
        #if it doesn't find the start it decreases by one, until it reaches a=2
        a = 10

        while a > 2:

            for i in number :
                #first it checks for the forward
                forward_indeces = i
                #checks to see if there are substring of the reference present in the sequence
                startf = find_all (sequence, reference_forward[(i):(i+a)])[0]

                #if startf has a length, it means that a start has been found
                if len (startf):
                    reference = reference_forward
                    stop = False

                    while stop == False:

                        for j in range (len(startf)):
                            #takes the position of the forward and creates the popup to see if it is the right start
                            position_to_use = startf [j]
                            reference_position = forward_indeces
                            output = StartSequence().response
                            stop = output["stop"]
                            
                            if stop:
                                #if "start not found"
                                if output ["button"] == "Start not found":
                                    return None
                                else:
                                    #takes the positions for the start, in both the sequence and the reference
                                    position_to_use = output ["position_to_use"]
                                    reference_position = output ["reference_position"]
                                    return position_to_use, reference_position, reference
                                              
                startr = find_all (sequence, reference_reverse[(i):(i+a)])[0]
                reverse_indeces = i

                if len (startr):
                    reference = reference_reverse
                    stop = False

                    while stop == False:

                        for j in range (len(startr)):
                            position_to_use = startr [j]
                            reference_position = reverse_indeces
                            output = StartSequence ().response
                            stop = output ["stop"]

                            if stop:

                                if output ["button"] == "Start not found":
                                    return None
                                else:
                                    position_to_use = output ["position_to_use"]
                                    reference_position = output ["reference_position"]
                                    return position_to_use, reference_position, reference
                      
            a = a-1

    except: return None

#takes the info to create the csv file
class Table_info:

    def __init__ (self):
        global xlsx_file
        self.response = {"gene name" : "", "start position" : "", "xlsx file" : 0}
        script_path = os.getcwd ()
        output_txt_path = os.path.join (script_path,"Output in txt")
        reference_path = os.path.join (script_path,"References")
        list_reference = os.listdir (reference_path)
        list_without_FRtxt = []
        xlsx_file = 0

        #permits to search the folder to plot
        def open_window ():
            folder_path = filedialog.askdirectory (initialdir = output_txt_path, title = "Select the folder")
            entry2.delete (0, tk.END)
            entry2.insert (0, folder_path)

        #to create a list of references, without duplicates
        for i in list_reference:
            if i.find ("F.txt") != -1:
                new_i = i.replace ("F.txt", "")
            elif i.find ("R.txt") != -1:
                new_i = i.replace ("R.txt", "")

            list_without_FRtxt.append (new_i)

        list_without_FRtxt = list (dict.fromkeys(list_without_FRtxt))
 
        def enter ():
            self.response ["gene name"] = clicked1.get () 
            self.response ["condition path"] = entry2.get ()
            self.response ["start position"] = entry3.get ()
            root.destroy () 
        def choose_xlsx_file ():
            global xlsx_file
            if xlsx.get ():
                xlsx_file = 1
            else: xlsx_file = 0
            self.response ["xlsx file"] =  xlsx_file

        #popup characteristics
        root = tk.Tk ()
        root.geometry ("750x250")
        if sys.platform.startswith ('darwin'): 
            font = ("", 15)
        else: font = ("", 13) 
        clicked1 = tk.StringVar ()
        list_without_FRtxt.insert (0, "Select")
        drop1 = ttk.OptionMenu (root, clicked1, *list_without_FRtxt)
        drop1.place (x = 363, y = 22, anchor="center")
        label1 = tk.Label (root, text = "Gene name", font = font)
        label1.grid (row = 0, column = 0, padx = 10, pady = 10, ipadx = 10)
        entry2 = ttk.Entry (root)
        entry2.grid (row = 1, column = 1, padx = 10, pady = 10, ipadx = 80)
        label2 = tk.Label (root, text = "Condition's Folder", font = font)
        label2.grid(row = 1, column = 0, padx = 10, pady = 10, ipadx = 10)
        entry3 = ttk.Entry (root)
        entry3.grid (row = 2, column = 1, padx = 10, pady = 10, ipadx = 30)
        label3 = tk.Label(root, text = "Reference start position", font = font)
        label3.grid (row = 2, column = 0, padx = 10, pady = 10, ipadx = 10)
        entry3.focus_set ()
        button_path = ttk.Button (root, text = "Search", width = 10, command = open_window)
        button_path.grid (row = 1, column = 2, padx = 10, pady = 10, ipadx = 10)
        label4 = tk.Label(root, text = "Do you want an xlsx file?", font = font)
        label4.grid (row = 3, column = 0, padx = 10, pady = 10, ipadx = 10)
        xlsx = tk.IntVar (root, value = xlsx_file)
        button_xlsx = tk.Checkbutton (root, variable = xlsx, command = choose_xlsx_file)
        button_xlsx.grid (row = 3, column = 1, padx = 10, pady = 10, ipadx = 10)
        button = ttk.Button (root, text = "Enter", width = 10, command = enter)
        button.grid (row = 4, column = 1, padx = 10, pady = 10, ipadx = 10)

        tk.mainloop ()

#info about the csv or xlsx file to plot into the graphs
class Chart_info:
    
    def __init__ (self):

        global text_start, text_end, text_error_standard, text_list_errors, bg_cpg, bg_non_cpg, setting_json, value_cap, text_over_bar
        path = os.getcwd ()
        path_table = os.path.join (path, "Tables")
        list_files = os.listdir (path_table)
        list_exel = list (dict.fromkeys (list_files))
        list_extensions = ["tif", "tif", "pdf", "jpg"]
        self.response =  {}
        text_start = ""
        text_end = "" 
        text_error_standard = ""
        text_list_errors = ""
        value_cap = 0
        text_over_bar = 0

        #takes where the package is saved
        package_path = os.path.split (methpy.__file__) [0]
        setting_json = os.path.join (package_path, "last_choosen.json")

        #if a json file already exists, takes its informations
        if os.path.isfile (setting_json):
            with open(setting_json) as f:
                settings = json.load(f)
            
            bg_cpg = settings ["color_cpg"]
            bg_non_cpg = settings ["color_non_cpg"]
            value_cap = settings ["error_cap"]
            text_over_bar = settings ["mean over bar"]

        else:
            bg_cpg = "red"
            bg_non_cpg = "gray"

        def enter ():
            self.response ["path table"] = os.path.join (path_table, clicked.get ())
            self.response ["gene name"] = entry_gene_name.get ()
            self.response ["condition name"] = entry_condition_name.get ()
            self.response ["extension"] = clicked_extensions.get ()
            self.response ["resolution"] = entry_resolution.get ()
            root.destroy ()
        
        #popup to choose the color for both CpG and non-CpG
        def popup_color ():
            global error_cap
            def choose_color_cpg ():
                global bg_cpg
                color_cpg = askcolor (title = "Choose color for CpG", parent = window_color)
                if type(color_cpg) == tuple and color_cpg[1] is not None:
                    self.response ["cpg color"] = color_cpg [1]
                    bg_cpg = self.response ["cpg color"] 
                else: 
                    try: 
                        bg_cpg = bg_cpg
                    except:
                        if os.path.isfile (setting_json):                       
                            self.response ["cpg color"] = settings ["color_cpg"]
                            bg_cpg = settings ["color_cpg"]
                        else:
                            self.response ["cpg color"] = "red"
                            bg_cpg = "red"  
                button_color_cpg.configure (background = bg_cpg)
                
            def choose_color_non_cpg ():
                global bg_non_cpg
                color_non_cpg = askcolor (title = "Choose color for non-CpG", parent = window_color)
                if type(color_non_cpg)==tuple and color_non_cpg[1] is not None:
                    self.response ["non cpg color"] = color_non_cpg [1]
                    bg_non_cpg = self.response ["non cpg color"]
                else: 
                    try:
                        bg_non_cpg=bg_non_cpg
                    except:
                        if os.path.isfile (setting_json):                       
                            self.response ["non cpg color"] = settings ["color_non_cpg"]
                            bg_non_cpg = settings ["color_non_cpg"]
                        else:
                            self.response ["color_non_cpg"] = "gray"
                            bg_non_cpg = "gray"
                button_color_non_cpg.configure (background = bg_non_cpg)
            
            def choose_text ():
                global text_over_bar
                if mean_over_bar.get (): 
                    text_over_bar = 1
                else: text_over_bar = 0
                self.response ["mean over bar"] = text_over_bar

            def save_colors_popup ():
                window_color.destroy ()
            
            if sys.platform.startswith ('darwin'): 
                font = ("", 15)
            else: font = ("", 13)            
            window_color = tk.Toplevel(root)
            window_color.geometry ("580x220")
            label_color_cpg = ttk.Label (window_color, text = "Color of CpG", font = font)
            label_color_cpg.grid (row = 0, column = 0, padx = 10, pady = 10, ipadx = 10)
            button_color_cpg = tk.Button (window_color, text = "Color of CpG", command = choose_color_cpg, bg = bg_cpg)
            button_color_cpg.grid (row = 0, column = 1, padx = 10, pady = 10, ipadx = 70)
            label_color_non_cpg = ttk.Label (window_color, text = "Color of non-CpG", font = font)
            label_color_non_cpg.grid (row = 1, column = 0, padx = 10, pady = 10, ipadx = 10)
            button_color_non_cpg = tk.Button (window_color, text = "Color of non-CpG", command = choose_color_non_cpg, bg = bg_non_cpg)
            button_color_non_cpg.grid (row = 1, column = 1, padx = 10, pady = 10, ipadx = 70)
            label_mean_over_bar = ttk.Label (window_color, text = "Display the percentage for each bar", font = font)
            label_mean_over_bar.grid (row = 3, column = 0, padx = 10, pady = 10, ipadx = 10)
            mean_over_bar = tk.IntVar (window_color, value = text_over_bar)    
            button_mean_over_bar = tk.Checkbutton (window_color, variable = mean_over_bar, command = choose_text)
            button_mean_over_bar.grid (row = 3, column = 1, padx = 10, pady = 10, ipadx = 80)
            save_colors = ttk.Button (window_color, text = "Enter", command = save_colors_popup)
            save_colors.grid (row = 4, column = 1, padx = 10, pady = 10, ipadx = 10)  
            
        def setting_popup ():

            def save_info ():
                global text_start, text_end, text_error_standard, text_list_errors
                self.response ["first base"] = entry_start.get()
                text_start = entry_start.get ()
                text_end = entry_end.get ()
                text_error_standard = entry_error_standard.get ()
                text_list_errors = entry_list_errors.get ()
                self.response ["last base"] = entry_end.get()
                self.response ["default errors"] = entry_error_standard.get()
                self.response ["custom errors"] = entry_list_errors.get()
                window_setting.destroy ()
                
            def choose_cap_error ():
                global value_cap
                if error_cap.get (): 
                    value_cap = 1
                else: value_cap = 0
                self.response ["error cap"] = value_cap

            window_setting = tk.Toplevel(root)
            if sys.platform.startswith ('darwin'): 
                font = ("", 15)
            else: font = ("", 13)
            window_setting.geometry ("850x270")
            label_start = ttk.Label (window_setting, text = "First base", font =  font)
            label_start.grid (row = 0, column = 0, padx = 10, pady = 10, ipadx = 10)
            entry_start = ttk.Entry (window_setting)
            entry_start.insert (0, text_start)
            entry_start.grid (row = 0, column = 1, padx = 10, pady = 10, ipadx = 40)
            label_end = ttk.Label (window_setting, text = "Last base", font =  font)
            label_end.grid (row = 1, column = 0, padx = 10, pady = 10, ipadx = 10)
            entry_end = ttk.Entry (window_setting)
            entry_end.insert (0, text_end)
            entry_end.grid (row = 1, column = 1, padx = 10, pady = 10, ipadx = 40)
            label_error_standard = ttk.Label (window_setting, text = "Same error value for all the bases", font = font)
            label_error_standard.grid (row = 2, column = 0, padx = 10, pady = 10, ipadx = 10)
            entry_error_standard = ttk.Entry (window_setting)
            entry_error_standard.insert (0, text_error_standard)
            entry_error_standard.grid (row = 2, column = 1, padx = 10, pady = 10, ipadx = 40)
            label_list_errors = ttk.Label (window_setting, text = "Custom errors for each base; enter a comma-separated list of numbers", font = font)
            label_list_errors.grid (row = 3, column = 0, padx = 10, pady = 10, ipadx = 10)
            entry_list_errors = ttk.Entry (window_setting)
            entry_list_errors.insert (0, text_list_errors)
            entry_list_errors.grid (row = 3, column = 1, padx = 10, pady = 10, ipadx = 40)
            label_error_cap = ttk.Label (window_setting, text = "Display the error cap", font = font)
            label_error_cap.grid (row = 4, column = 0, padx = 10, pady = 10, ipadx = 10)
            error_cap = tk.IntVar (window_setting, value = value_cap)
            button_error_cap = tk.Checkbutton (window_setting, variable = error_cap, command = choose_cap_error)
            button_error_cap.grid (row = 4, column = 1, padx = 10, pady = 10, ipadx = 80)
            save_setting = ttk.Button (window_setting, text = "Enter", command = save_info)
            save_setting.grid (row = 5, column = 1, padx = 10, pady = 10, ipadx = 10)               
            
        #main popup characteristics
        if sys.platform.startswith ('darwin'): 
            font = ("", 15)
        else: font = ("", 13)
        root = tk.Tk ()
        root.geometry ("770x420")
        clicked = tk.StringVar ()
        list_exel.insert (0, "Select")
        label_file_name = ttk.Label (root, text = "Table file name", font = font)
        label_file_name.grid (row = 0, column = 0, padx = 10, pady = 10, ipadx = 10)
        drop = ttk.OptionMenu (root, clicked, *list_exel)
        drop.config (width = 30)
        drop.grid (row = 0, column = 1)
        entry_gene_name = ttk.Entry (root)
        entry_gene_name.grid (row = 1, column = 1, padx = 10, pady = 10, ipadx = 70)
        label_gene_name = ttk.Label (root, text = "Gene name", font = font)
        label_gene_name.grid (row = 1, column = 0, padx = 10, pady = 10, ipadx = 10)
        entry_condition_name = ttk.Entry (root)
        entry_condition_name.grid (row = 2, column = 1, padx = 10, pady = 10, ipadx = 70)
        label_condition_name = ttk.Label (root, text = "Experimental condition", font = font)
        label_condition_name.grid (row = 2, column = 0, padx = 10, pady = 10, ipadx = 10)
        label_resolution = ttk.Label (root, text = "Enter an integer value for the chart's DPI (default: 200)", font = font)
        label_resolution.grid (row = 3, column = 0, padx = 10, pady = 10, ipadx = 10)
        entry_resolution = ttk.Entry (root)
        entry_resolution.grid (row = 3, column = 1, padx = 10, pady = 10, ipadx = 70)
        label_extensions = ttk.Label (root, text = "Extensions of the output charts", font = font)
        label_extensions.grid (row = 4, column = 0, padx = 10, pady = 10, ipadx = 10)
        clicked_extensions = tk.StringVar () 
        drop_extensions = ttk.OptionMenu (root, clicked_extensions, *list_extensions)
        drop_extensions.grid (row = 4, column= 1, padx = 10, pady = 10, ipadx = 30)
        label_custom_setting = ttk.Label (root, text = "Custom settings for base range and errors", font = font)
        label_custom_setting.grid (row = 5, column = 0, padx = 10, pady = 10, ipadx = 10)
        button_custom_setting = ttk.Button (root, text = "Click me!", command = setting_popup)
        button_custom_setting.grid (row = 5, column = 1, padx = 10, pady = 10, ipadx = 10, ipady = 10)
        label_custom_colors = ttk.Label (root, text = "Custom chart colors", font = font)
        label_custom_colors.grid (row = 6, column = 0, padx = 10, pady = 10, ipadx = 10)
        button_custom_colors = ttk.Button (root, text = "Click me!", command = popup_color)
        button_custom_colors.grid (row = 6, column = 1, padx = 10, pady = 10, ipadx = 10, ipady = 10)
        button = ttk.Button (root, text = "Enter", width = 10, command = enter)
        button.grid (row = 7, column = 1, padx = 10, pady = 10, ipadx = 10)
        
        tk.mainloop ()
