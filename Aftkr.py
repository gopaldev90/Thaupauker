import os
import copy
import json
import platform
from datetime import datetime
import sys
def get_data_path(filename):
    if getattr(sys, 'frozen', False):  # Check if the app is frozen (i.e., bundled)
        return os.path.join(sys._MEIPASS, filename)
        # _MEIPASS is where PyInstaller stores the bundled files
    else:
        return filename  # Otherwise, use the normal filename


class PVZ2Modifier:
    '''
    This class is used to change or modify plant levels in PVZ2.
    Created by Gopal Krishna Pandey, first released on 20 November 2023.
    More updates will come in the future.
    '''
    
    def __init__(self):
        if platform.system()=='Linux':
        	import sys
        	sys.path.append('/storage/emulated/0/pvz2/plant_1000_bnao/Tool/')
        	
        	self.__alreadypath='/storage/emulated/0/pvz2/plant_1000_bnao/Tool/alrdy.json'
        else:
        	self.__alreadypath=get_data_path('alrdy.json')
        self.logs=""
        # yaad rhe ye sorted rhe(ascending)
        
        self.sphlist = [
            4,
            25,
            41,
            51,
            59,
            77,
            102,
            143,
            147,
            153
        ]
        self.__alrdymod= self.loadjson(self.__alreadypath) 
    def loadjson(self, path):
        if not os.path.exists(path):
        	alson={
        	'already': []
        	}
        else:
        	with open(path, 'r') as f:
        		alson= json.load(f)
        return alson
    def getcurtime(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")[:-3]

    def __geteligi(self,taton, list):
        n = len(list)
        step= int(n**0.5)
        prev=curr = 0
        while curr < n and list[curr] <= taton:
            prev = curr
            curr+=step
            if curr>=n:
                curr=n
        
        left, right =prev, curr-1
        r = False
        while (left<=right):
            mid = (left + right) // 2
            if(list[mid]==taton):
                r=True
                break
            elif(list[mid]<taton):
                left = mid+1
            else:
                right = mid-1
        return r
    def __updatestatus(self, label, root, taton, Seema):
        '''
        Update the status label in the GUI.

        Parameters:
        label (tk.Label): Label to be updated.
        root (tk.Tk): Tkinter root for GUI updates.
        taton (int): Current index.
        Seema (int): Total number of plants.
        '''
        pratishat = ((taton + 1) / (Seema + 1)) * 100
        if pratishat<100:
        	status_text= "{:.2f}%".format(pratishat)	
        	label.config(text=status_text)
        	root.update_idletasks()

    def savejson(self, saveto, paun_folder, data, ston=False):
        '''
        Save JSON data to a specified folder.

        Parameters:
        saveto (str): Directory where JSON file is to be saved.
        paun_folder (str): Folder where JSON file is to be saved.
        data (dict): Data to be saved as JSON file.
        '''
        import jsortokhi
        fo = os.path.join(saveto, paun_folder)
        filep = os.path.join(fo, "PlantLevels.json")
        if not os.path.exists(fo):
            os.makedirs(fo)
        jsortokhi.save_data(data,filep)
        if ston:
        	rton = jsortokhi.torton(filep)
        	savep=(os.path.join(fo,'PlantLevels.rton'))
        	jsortokhi.save_data(rton,savep)
        	self.logs+='Rton converted'
        lop = os.path.join(fo, "log.txt")
        jsortokhi.save_data(self.logs,lop)
        print(self.logs)
        self.logs=""
    def naamde(self, data, taton):
        '''
        Return the name of the plant.

        Parameters:
        data (dict): JSON data.
        taton (int): Index of the plant.

        Returns:
        str: Name of the plant.
        '''
        aliases = data['objects'][taton].get('aliases', [])
        cleaned_aliases = ', '.join(alias.capitalize() for alias in aliases)
        cleaned_aliases = cleaned_aliases.translate(str.maketrans('', '', "/\\:*?\"<>|"))
        return cleaned_aliases

    def getSeema(self, data):
        '''
        Return the number of the last plant.

        Parameters:
        data (dict): JSON data.

        Returns:
        int: Index of the last plant.
        '''
        return len(data["objects"]) - 1

    def gettaton(self, data, name):
        '''
        Return the index of the plant if found, else -1.

        Parameters:
        data (dict): JSON data.
        name (str): Name of the plant.

        Returns:
        int: Index of the plant or -1 if not found.
        '''
        cleaned_names = set()  
        for k, obj in enumerate(data['objects']):
            aliases = obj.get('aliases', [])
            for alias in aliases:
                cleaned_alias = alias.capitalize().translate(str.maketrans('', '', "/\\:*?\"<>|"))
                cleaned_names.add(cleaned_alias)
                if cleaned_alias == name.capitalize().translate(str.maketrans('', '', "/\\:*?\"<>|")):
                    return k  
        return -1
    def groupupdate(self, data, cpf, tatonlist):
        vyakhya= []
        for taton in tatonlist:
            paunaam= self.naamde(data, taton)
            data=self.update_json(taton, data, cpf, paunaam)
            
            vyakhya.append(f"{paunaam} id: {taton}")
        data["#vyakhya"]=vyakhya
        data["#credit"]="Hacked by Pvz2pagalpan"
        return data
    
    def getkshetr(self,bound,data):
        if(not (bound and ',' in bound)):
        	shuru=0
        	Seema = self.getSeema(data)
        else:
        	shuru,Seema=bound.split(',')
        	shuru=int(shuru)
        	Seema=int(Seema)
       
        return (shuru,Seema)
    
    def zeromana(self, data, label=False, root=False, bound=None):
        '''
        changes every plant's recharge to 0.
        Parameters:
        data (dict): JSON data
        label: tk.Label to update (optional)
        root: tk.Tk root (optional)
        return: (dict) Json data 
        
        '''
        shuru,seema=self.getkshetr(bound, data)
        for taton in range(shuru, seema + 1):
            ch=0
            paunaam= self.naamde(data, taton)
            float_stats =data['objects'][taton]['objdata']['FloatStats']
            for stat in float_stats:
                name = stat.get('Name', '').lower()
                if(any(substring in name for substring in ["cooldown","cost"])):
                    if(name=="cost"):
                    	stat["Values"] = [-2048] * len(stat["Values"])
                    else:
                    	stat["Values"] = [0] * len(stat["Values"])
                    ch+=1
                    if(ch>2):
                    	break
                    self.logs+=f"Zeroed {paunaam}'s {name}\n"
            print(f'{taton}. {paunaam}')
            if label and root:
                self.__updatestatus(label, root, taton, seema) 
        return data
    
    def sabalaga(self, data, saveto, label=False, root=False, bound=None):
        '''
        Modify all plants and save the JSON files separately.

        Parameters:
        data (dict): JSON data.
        saveto (str): Directory where JSON files are to be saved.
        label (tk.Label): Label to be updated.
        root (tk.Tk): Tkinter root for GUI updates.
        bound (Str): Start and end bound seperated by , 
        '''
        
        shudhdata = copy.deepcopy(data)
        shuru,Seema=self.getkshetr(bound, data)
        for taton in range(shuru, Seema + 1):
            paun_folder = self.naamde(data, taton)
            data = copy.deepcopy(shudhdata)
            print(f'{taton}. {paun_folder}')
            data = self.update_json(taton, data, False, paun_folder)
            vyakhya = f"{paun_folder} Hacked by Pvz2pagalpan Id: {taton}"
            data["#vyakhya"] = vyakhya
            data["#Kab"] = self.getcurtime()
            self.savejson(saveto, (str(taton) + "." + paun_folder), data, True)
            if label and root:
                self.__updatestatus(label, root, taton, Seema)

    def ekamsab(self, data, saveto, label=False, root=False, bound=None):
        '''
        Modify all plants and save them in a single JSON file.

        Parameters:
        data (dict): JSON data.
        saveto (str): Directory where JSON file is to be saved.
        label (tk.Label): Label to be updated.
        root (tk.Tk): Tkinter root for GUI updates.
        bound (Str): Start and end bound seperated by , 
        '''
        shuru,Seema=self.getkshetr(bound, data)
        
        for taton in range(shuru,Seema + 1):
            
            paunaam = self.naamde(data, taton)
            print(f'{taton}. {paunaam}')
            data = self.update_json(taton, data, False, paunaam)
            if label and root:
                self.__updatestatus(label, root, taton, Seema)
        
        paun_folder = 'Sabheepaudhe'
        vyakhya = "All plants hacked by Pvz2pagalpan"
        data["#vyakhya"] = vyakhya
        data["#Kab"] = self.getcurtime()
        self.savejson(saveto, paun_folder, data, True)

    def update_json(self, taton, data, cpf, paunam, ignoreallr= False):
        '''
        Update the plant levels.

        Parameters:
        taton (int): Index of the plant.
        data (dict): JSON data.
        paunam (str): Name of the plant.
        cpf (bool): Indicates PlantFood play count is to be updated.
        ignoreallr (bool): ignore allready hacked stats if True it will hack again
        Returns:
        dict: Updated JSON data.
        '''
        locallogs=""
        if(not ignoreallr):
        	alreadylist = self.__alrdymod['already']
        	if(self.__geteligi(taton, alreadylist)):
        		data['objects'][taton]= self.__alrdymod['plants'][str(taton)]['value']
        		self.logs+=f'\n{paunam} already hacked\n'
        		return data
        nodename = 'PlantFoodPlayCount'
        skiplist = [nodename.lower(), 'planttier', 'plantfoodduration', "knockback"]

        def checkodr(stat, name, gap):
            for ele in skiplist:
                if not ele in name:
                    asce = desce = True
                    originallist = statval[0:gap+1]
                    for k in range(1, len(originallist)):
                        if originallist[k] > originallist[k-1]:
                            desce = False
                        elif originallist[k] < originallist[k-1]:
                            asce = False
                        if(not(asce or desce)):
                            break
                    if asce or desce:
                        if asce:
                            statval[-1] = 90745545
                        else:
                            statval[-1] = 0.1
                        stat["Values"] = statval
                    break
            return stat

        maxlvl = 1000
        levelcoins_values = [0] * maxlvl
        locallogs += f"\n{taton}. {paunam} changes:\n"
        float_stats = data['objects'][taton]['objdata']['FloatStats']
        conditionvalues = {
            "damage": 22339,
            "dps": 22339,
            "cost": -2048,
            "hitpoints": 99999999,
            "packetcooldown": 0,
            "startingcooldown": 0,
            "expirationduration": 12999990,
            "velocity": 1124,
            "sunproduce": 907
        }

        for stat in float_stats:
            ntco = True
            name = stat.get('Name', '').lower()
            statval = stat["Values"]
            gap = (maxlvl - len(statval))
            if gap > 0:
                statval.extend(([statval[-1]] * (gap)))
            if any(skip_name in name for skip_name in skiplist):
                continue  # Skip modification for this stat
            for key in conditionvalues:
                if key in name:
                    statval[-1] = conditionvalues[key]
                    stat["Values"] = statval
                    ntco = False
                    break
            if ntco:
                stat = checkodr(stat, name, gap)
                locallogs+= 'used checkodr for '
            locallogs += f'{name} last value\n{statval[-1]}\n'
        # new nut logic here
        if(self.__geteligi(taton, self.sphlist)):
            name = 'hitpoints'
            sh = 21474836479999999
            index = next((i for i, stat in enumerate(float_stats) if stat["Name"].lower()== name), None)
            if index is not None:
                float_stats[index]["Values"][-1] = sh
                locallogs = locallogs.replace(f"{name} last value\n99999999", f"{name} last value\n{sh}")
                index=None
            
        locallogs+= f"cpf was\n{cpf}\n"
        if cpf:
            index=-1
            for i,v in enumerate(float_stats):
            	if (skiplist[2] in v.get("Name","").lower()):
            		index=i
            		break
            
            iseligible =(index==-1)
            locallogs+= f'Eligible\n{iseligible}\n'
            if iseligible:
                
                pfvalues = [1] * maxlvl
                pfvalues[-1] = 8707051
                pfst = False
                for stat in float_stats:
                    if stat.get('Name', '') == nodename:
                        pfst = stat
                        break
                if pfst:
                    locallogs+=f'{nodename} was already in float_stats\n'
                    pfst["Values"] = pfvalues
                else:
                    pfpc_dict = {
                        'Name': nodename,
                        'Values': pfvalues
                    }
                    float_stats.append(pfpc_dict)
                    locallogs+=f'{nodename} added in float_stats\n'
            elif False:
                # yahan pe abhi kaam baaki hai
                float_stats[index]["Values"][-1] = 123456789
                locallogs+= "Plant food duration changed\n"
                

        data['objects'][taton]['objdata']['LevelCoins'] = levelcoins_values
        locallogs+="LevelCoins changed\n"
        data['objects'][taton]['objdata']['LevelXP'] = levelcoins_values
        locallogs+="LevelXP changed\n"
        data['objects'][taton]['objdata']['LevelCap'] = maxlvl
        locallogs += 'LevelCap changed\n'
        
        
        self.logs+=locallogs
        return data


if __name__ == "__main__":
    md = PVZ2Modifier()
    data = md.loadjson("Plantlevels.json")
    print('ek: se ek plant ko 1000 bnao')
    print('sa: se sabhee plant alag alag')
    print('se: se sabhee plant ek main')
    print('z: se zeeromana suncost')
    agya = input('aagyaa ').lower()
    
    sahej = "Edited"
    if agya == 'ek':
        tatton = int(input('plant index is: '))
        cpf=(input('cpf:0=False: ')!='0')
        pf = md.naamde(data, tatton)
        data = md.update_json(tatton, data, cpf, pf, False)
        md.savejson(sahej, f'{str(tatton)}.{pf}', data, True)
    else:
        kshetr = input('Shuru,Seema: ')
        if agya == 'sa':
            md.sabalaga(data, sahej, False, False, kshetr)
        elif agya == 'se':
            md.ekamsab(data, sahej, False, False, kshetr)
        elif agya == 'z':
            data = md.zeromana(data, False, False, kshetr)
            md.savejson(os.getcwd(), os.path.join(sahej, "Zeromana"), data, True)
            