import methpy
from methpy.__init__ import Chart_info
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import load_workbook
import os
import pandas as pd
import seaborn as sns
import sys
import json
import ctypes

#removes a warning from pandas
pd.options.mode.chained_assignment = None
#resolves a graphic problem between tkinter and matplotlib when chart is called more then once
if sys.platform.startswith ("win") : 
    ctypes.windll.shcore.SetProcessDpiAwareness(0)

def plot ():
    """Generates the plot starting from the Excel or csv files"""
    try:
        #gets the info and splits them
        info = Chart_info ().response
        path_table = info ["path table"]
        gene_name = info  ["gene name"]
        condition_name = info ["condition name"]
        extension = info ["extension"]
        resolution = info ["resolution"]
        if resolution == "" :
            resolution = 200        
        package_path = os.path.split (methpy.__file__) [0]
        setting_json = os.path.join (package_path, "last_choosen.json")  
        ##CONTROLLA DA QUI
        try:
            color_cpg = info ["cpg color"]
        except: 
            if os.path.isfile (setting_json):
                with open(setting_json) as f:
                    settings = json.load(f)                
                color_cpg = settings ["color_cpg"]
            else:
                color_cpg = "red"

        try: color_non_cpg = info ["non cpg color"]
        except:             
            if os.path.isfile (setting_json):
                with open(setting_json) as f:
                    settings = json.load(f)                
                color_non_cpg = settings ["color_non_cpg"]
            else:
                color_non_cpg = "gray"
        
        try: error_cap = info ["error cap"]
        except:
            if os.path.isfile (setting_json):
                with open(setting_json) as f:
                    settings = json.load(f)                
                error_cap = settings ["error_cap"]
            else:
                error_cap = 0

        if error_cap == 1:
            capsize = 3
        else: capsize = 0

        try: text_over_bar = info ["mean over bar"]
        except:
            if os.path.isfile (setting_json):
                with open(setting_json) as f:
                    settings = json.load(f)                
                text_over_bar = settings ["mean over bar"]
            else:
                text_over_bar = 0
        
        #rewrites the json file
        settings = {"color_cpg" : color_cpg, "color_non_cpg" : color_non_cpg, "error_cap" : error_cap, "mean over bar" : text_over_bar}
        with open (setting_json, "w") as f:
            json.dump (settings, f)

        table_extension = os.path.splitext (path_table) [1]
        #checks if the input is a csv
        if table_extension == ".csv":
            csv =  pd.read_csv(path_table, delimiter = ";", index_col = 0)
            list_relative_number = csv.loc ["Percentage"][2:]
            list_all_c =["",""]
            for i in list(csv.loc["0"] [2:]):
                list_all_c.append(int(i))
            csv.columns = list_all_c
            list_cpg = csv.loc ["CpG Presence"][csv.loc ["CpG Presence"] == "CpG"].index
            df_all_cs = pd.DataFrame (list_relative_number)
            df_all_cs = df_all_cs.fillna (0.0)
            df_all_cs.index = list_all_c[2:]
            df_all_cs ["Percentage"] = df_all_cs ["Percentage"].astype (float)
        else:
            #opens the excel file and the active sheet
            wb = load_workbook (path_table, data_only = True)
            ws = wb.active

            #where are the last row and column written
            i = 5
            while i > 4:
                #takes the first row empty and adds 2 to it
                if type (ws.cell (i, column = 5).value) == type (None):
                    relative_number_position = i + 2
                    break
                i += 1
            i = 5
            while i > 4:
                #takes the first column empty and goes back by 1
                if type(ws.cell (3, column = i).value) == type(None):
                    last_c_position = i - 1 
                    break
                i += 1

            list_all_c = []
            list_cpg = []
            list_relative_number = []

            #goes over all the Cs
            for i in range (5, last_c_position+1):
                #takes the C in that cell
                cell_c_position = ws.cell (row = 4, column = i)
                list_all_c.append (cell_c_position.value)
                #takes the corresponding relative number
                cell_relative_number = ws.cell (row = relative_number_position, column = i)
                list_relative_number.append (cell_relative_number.value)
                
                #checks if the C is red, so if it is a CpG and creates two different lists
                if type (cell_c_position.font.color.rgb) == str and cell_c_position.font.color.rgb == 'FFFF0000':
                    list_cpg.append (cell_c_position.value)

            #transforms the relative number to a percentage
            for i in range (len (list_relative_number)):
                list_relative_number [i] = list_relative_number [i] * 100

            #creates the dataframe, the index is the C position
            df_all_cs = pd.DataFrame (list_relative_number, index = list_all_c)
            for i in df_all_cs.index:
                if type (df_all_cs.loc[i,0]) == str:
                    df_all_cs.loc[i,0] = 0.0
        
        #to consider only the range inserted into the custom settings
        if ("first base" in info and "last base" in info): 
            if info["first base"] != "" and info["last base"] != "":
                first_c = next(x for x in df_all_cs.index if x >= int(info["first base"]))
                last_c = [item for item in df_all_cs.index if item <= int(info["last base"])][-1]
                df_all_cs = df_all_cs.loc [first_c:last_c]
                list_cpg = list(filter (lambda x: int(info["first base"]) <= x <= int(info["last base"]), list_cpg))
            elif info["first base"] != "":
                first_c = next(x for x in df_all_cs.index if x >= int(info["first base"]))
                df_all_cs = df_all_cs.loc [first_c:]
                list_cpg = list(filter (lambda x: x >= int(info["first base"]), list_cpg))
            elif info["last base"] != "":
                last_c = [item for item in df_all_cs.index if item <= int(info["last base"])][-1]
                df_all_cs = df_all_cs.loc [:last_c]
                list_cpg = list(filter (lambda x: x <= int(info["last base"]), list_cpg))

        #to consider the list of errors
        if table_extension == ".csv":
            column = "Percentage"
        else: column = 0
        try: 
            list_error = info ["custom errors"].replace ("\n", "")
            list_error = list_error.replace (" ", "")
            list_error = list_error.split (",")
            list_error = [float(i) for i in list_error]

            if len (df_all_cs.index) > len (list_error):
                zeros_to_append = [0] * (len (df_all_cs.index) - len (list_error)) 
                list_error.extend (zeros_to_append)
                print ("An error was not provided for each base; for the last positions, 0 was used as the error")
            list_error = pd.Series (list_error, index = df_all_cs.index)

            for i in df_all_cs.index:
                if df_all_cs.loc [i,column] == 100.0 or df_all_cs.loc[i, column] + list_error [i] == 0.0:
                    df_all_cs.loc [i,"negative errors"] = 0.0
                    df_all_cs.loc [i,"positive errors"] = 0.0
                else: 
                    if (df_all_cs.loc[i, column] + list_error [i]) > 100.0:
                        df_all_cs.loc [i, "positive errors"] = 100.0 - df_all_cs.loc [i, column]
                    else: df_all_cs.loc [i, "positive errors"] = list_error [i]
                    if (df_all_cs.loc [i, column] - list_error[i]) < 0.0:
                        df_all_cs.loc [i, "negative errors"] = df_all_cs.loc [i, column]
                    else: df_all_cs.loc [i, "negative errors"] = list_error [i]
        except:
            #to consider the same error for all the bases
            try : error = float (info ["default errors"])
            #if no error is inserted, it stays at 0
            except: error = 0
            for i in df_all_cs.index:
                if df_all_cs.loc [i,column] == 100.0 or df_all_cs.loc[i, column] == 0.0:
                    df_all_cs.loc [i,"negative errors"] = 0.0
                    df_all_cs.loc [i,"positive errors"] = 0.0
                else: 
                    if (df_all_cs.loc[i,column] + error) > 100.0:
                        df_all_cs.loc[i,"positive errors"] = 100.0 - df_all_cs.loc[i,column]
                    else: df_all_cs.loc[i, "positive errors"] = error

                    if (df_all_cs.loc[i,column]) - error < 0.0:
                        df_all_cs.loc[i,"negative errors"] = df_all_cs.loc[i,column]
                    else: df_all_cs.loc[i,"negative errors"] = error
        
        positive_errors = list(df_all_cs["positive errors"])
        negative_errors = list(df_all_cs["negative errors"])

        #takes only the index
        x = df_all_cs.index
        #takes only the first column
        y = df_all_cs.iloc [:, 0]
        str_x = []

        #transforms the index into a list of string to use it as X-axis tick values
        for i in x:
            str_x.append (str (i))

        #same thing for just the positions of CpGs
        str_cpg = []

        for i in list_cpg:
            str_cpg.append (str (i))

        #positions in which there are non-CpG
        str_non_cpg = [item for item in str_x if item not in str_cpg]

        #creates a column for CpG and where it is a CpG writes "CpG"
        for i in df_all_cs.index:
            if i in list_cpg:
                df_all_cs.loc [i, "CpG"] = "CpG"

        #takes only the rows of CpGs
        df_cpg = df_all_cs [df_all_cs.values == "CpG"]
        list_index_all_non_cpg = list (df_all_cs.index)
        list_for_loop = list_index_all_non_cpg.copy()
        for i in list_for_loop:
            #to see where is a CpG and remove
            if i in df_cpg.index:
                list_index_all_non_cpg.remove(i)

        for i in list_index_all_non_cpg:
            #creates the rest of the dataframe with zeros        
            df_cpg.loc [i] = [0,0,0,0]
        df_cpg = df_cpg.sort_index ()

        #takes the percentage of each base
        y_cpg = df_cpg.iloc [:, 0]
        all_cs_serie = df_all_cs ["CpG"]

        #From the dataframe takes only the CpG
        df_cpg_only = df_all_cs [df_all_cs.values == "CpG"]

        #takes where the Cs are not CpGs
        all_cs_serie [all_cs_serie != "CpG"].index

        #creates a dataframe of just non-CpGs
        df_non_cpg = pd.DataFrame ()
        for i in all_cs_serie [all_cs_serie != "CpG"].index:
            df_non_cpg = pd.concat ([df_non_cpg, df_all_cs.loc[[i]]])

        #chart for the global methylation
        #size of the figure x and y      
        ax = plt.subplots (figsize= (20, 4)) [1]

        #plots chart of all the Cs and then on top the chart of CpGs
        plt.bar (data = df_all_cs, x = str_x, height = y, yerr = (negative_errors, positive_errors), color = color_non_cpg, label = "Non-CpG Methylation", capsize = capsize)
        plt.bar (data = df_cpg, height = y_cpg, x = str_x, color = color_cpg, label = "CpG Methylation")

        if text_over_bar == 1:
            for i, val in enumerate (df_all_cs.iloc [:,0]):
                if val == 100.0:
                    plt.text(i - 0.4, val + positive_errors[i] + 0.4, str(100.0), fontsize = 400/len (df_all_cs))
                elif val != 0.0:
                    plt.text(i - 0.4, val + positive_errors[i] + 0.4, str(round(val, 1)), fontsize = 500/len (df_all_cs))
                else: plt.text(i - 0.4, val, str(0), fontsize = 0)
            
        #removes the outside box and names the labels
        sns.despine () 
        ax.set (xlabel = 'Base number', ylabel = 'Methylation %')

        #plot title
        plt.title ((f'Methylation of {gene_name} - {condition_name}'), fontsize = 12)

        #xlabel parameters
        plt.tick_params (axis = 'x', rotation = 90)
        plt.xticks (str_x, fontsize = 9)

        #ylabel parameters 
        plt.yticks (np.arange (0, 101, step = 10)) 
        vals = ax.get_yticks ()
        ax.set_yticklabels (['{:.0f}%'.format (x) for x in vals])

        #creates the legend
        ax.legend (bbox_to_anchor=(0.8, 0.98, 0.2, 0.2), loc="lower right", mode = "expand", ncol = 2)

        #changes the color of the xticks of the CpGs
        for i in list (df_all_cs [df_all_cs.values == "CpG"].index):
            to_color = str_x.index (str (i))
            plt.gca ().get_xticklabels () [to_color].set_color (color_cpg)

        #to remove the blank space at the side of the chart
        plt.margins (x=0)

        plt.tight_layout ()

        plt.savefig (os.path.join (os.getcwd (),"Charts",f'{gene_name}_{condition_name}_Methylation.{extension}'), dpi = float (resolution))
        plt.clf ()

        #chart for CpG methylation
        ax = plt.subplots (figsize= (20, 4)) [1]

        #plots the chart of CpGs
        plt.bar (data = df_cpg_only, x = str_cpg, height = df_cpg_only.iloc[:,0], color = color_cpg, yerr = (list(df_cpg_only["negative errors"].astype(float)), list(df_cpg_only["positive errors"].astype(float))), capsize = capsize)

        #removes the outside box and names the labels
        sns.despine () 
        ax.set (xlabel = 'Base number', ylabel = 'Methylation %')

        #plot title
        plt.title ((f'CpG Methylation of {gene_name} - {condition_name}'), fontsize = 12)

        #xlabel parameters
        plt.tick_params (axis = 'x', rotation = 90)
        plt.xticks (fontsize = 9)

        #ylabel parameters 
        plt.yticks (np.arange (0, 101, step = 10)) 
        vals = ax.get_yticks ()
        ax.set_yticklabels (['{:.0f}%'.format (x) for x in vals])

        #to remove the blank space at the side of the chart
        plt.margins (x = 0)
        
        if text_over_bar == 1:
            for i, val in enumerate (df_cpg_only.iloc [:,0]):
                if val == 100.0:
                    plt.text(i - 0.4, val + list(df_cpg_only["positive errors"])[i] + 0.4, str(100.0), fontsize = 400/len (df_cpg_only))
                elif val != 0.0:
                    plt.text(i - 0.4, val + list(df_cpg_only["positive errors"])[i] + 0.4, str(round(val, 1)), fontsize = 500/len (df_cpg_only))
                else: plt.text(i - 0.4, val, str(0), fontsize = 0)

        plt.tight_layout ()
        plt.savefig (os.path.join (os.getcwd (),"Charts",f'{gene_name}_{condition_name}_CpG_methylation.{extension}'), dpi = float (resolution))
        plt.clf ()

        #chart for non-CpG methylation
        ax = plt.subplots (figsize= (20, 4)) [1]

        #plots the chart of non-CpGs
        plt.bar (data = df_non_cpg, x = str_non_cpg, height = df_non_cpg.iloc [:,0], yerr = (list(df_non_cpg["negative errors"]), list(df_non_cpg["positive errors"])), color = color_non_cpg, capsize = capsize)
        
        #removes the outside box and names the labels
        sns.despine () 
        ax.set (xlabel = 'Base number', ylabel = 'Methylation %')

        #plot title
        plt.title ((f'Non-CpG Methylation of {gene_name} - {condition_name}'), fontsize = 12)

        #xlabel parameters
        plt.tick_params (axis = 'x', rotation = 90)
        plt.xticks (fontsize = 9)

        #ylabel parameters 
        plt.yticks (np.arange (0, 101, step = 10)) 
        vals = ax.get_yticks ()
        ax.set_yticklabels (['{:.0f}%'.format (x) for x in vals])

        #to remove the blank space at the side of the chart
        plt.margins (x = 0)

        if text_over_bar == 1:
            for i, val in enumerate (df_non_cpg.iloc [:,0]):
                if val == 100.0:
                    plt.text(i - 0.4, val + list(df_non_cpg["positive errors"]) [i] + 0.4, str(100.0), fontsize = 400/len (df_non_cpg))
                elif val != 0.0:
                    plt.text(i - 0.4, val + list(df_non_cpg["positive errors"]) [i] + 0.4, str(round(val, 1)), fontsize = 500/len (df_non_cpg))
                else: plt.text(i - 0.4, val, str(0), fontsize = 0)

        plt.tight_layout ()
        plt.savefig (os.path.join (os.getcwd (),"Charts",f'{gene_name}_{condition_name}_Non-CpG_methylation.{extension}'), dpi = float (resolution))
        plt.clf ()

        plt.close ("all")

        print ("Methylation plotted.")
    except: print ("Insert valid info.")

sys.modules[__name__] = plot