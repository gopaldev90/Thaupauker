import os
import copy
import json
from datetime import datetime

class PVZ2Modifier:
    '''
    This class is used to change or modify plant levels in PVZ2.
    Created by Gopal Krishna Pandey, first released on 20 November 2023.
    More updates will come in the future.
    '''
    
    def __init__(self):
        self.logs=""
        self.__eligipau = [
            7, 15, 27, 30, 35, 37, 39, 42, 45, 47, 49, 50, 52, 56
        ]

    def getcurtime(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")[:-3]

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
        status_text = "Sampurn" if pratishat >= 100 else "{:.2f}%".format(pratishat)
        label.config(text=status_text)
        root.update_idletasks()

    def savejson(self, saveto, paun_folder, data):
        '''
        Save JSON data to a specified folder.

        Parameters:
        saveto (str): Directory where JSON file is to be saved.
        paun_folder (str): Folder where JSON file is to be saved.
        data (dict): Data to be saved as JSON file.
        '''
        fo = os.path.join(saveto, paun_folder)
        filep = os.path.join(fo, "PlantLevels.json")
        if not os.path.exists(fo):
            os.makedirs(fo)
        with open(filep, 'w') as f:
            json.dump(data, f, indent=2)
        lop = os.path.join(fo, "log.txt")
        with open(lop, 'w') as f:
            f.write(self.logs)
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

    def sabalaga(self, data, saveto, label=False, root=False):
        '''
        Modify all plants and save the JSON files separately.

        Parameters:
        data (dict): JSON data.
        saveto (str): Directory where JSON files are to be saved.
        label (tk.Label): Label to be updated.
        root (tk.Tk): Tkinter root for GUI updates.
        '''
        paunlist = []
        Seema = self.getSeema(data)
        shudhdata = copy.deepcopy(data)
        
        for k in range(Seema + 1):
            nam = self.naamde(data, k)
            paunlist.append(nam)
        for taton in range(Seema + 1):
            paun_folder = paunlist[taton]
            data = copy.deepcopy(shudhdata)
            cpf = taton in self.__eligipau
            data = self.update_json(taton, data, cpf, paun_folder)
            vyakhya = f"{paun_folder} Hacked by Pvz2pagalpan Id: {taton}"
            data["#vyakhya"] = vyakhya
            data["#Kab"] = self.getcurtime()
            self.savejson(saveto, (str(taton) + "." + paun_folder), data)
            if label and root:
                self.__updatestatus(label, root, taton, Seema)

    def ekamsab(self, data, saveto, label=False, root=False):
        '''
        Modify all plants and save them in a single JSON file.

        Parameters:
        data (dict): JSON data.
        saveto (str): Directory where JSON file is to be saved.
        label (tk.Label): Label to be updated.
        root (tk.Tk): Tkinter root for GUI updates.
        '''
        Seema = self.getSeema(data)
        for taton in range(Seema + 1):
            cpf = taton in self.__eligipau
            paunaam = self.naamde(data, taton)
            data = self.update_json(taton, data, cpf, paunaam)
            if label and root:
                self.__updatestatus(label, root, taton, Seema)
        
        paun_folder = 'Sabheepaudhe'
        vyakhya = "All plants hacked by Pvz2pagalpan"
        data["#vyakhya"] = vyakhya
        data["#Kab"] = self.getcurtime()
        self.savejson(saveto, paun_folder, data)

    def update_json(self, taton, data, cpf, paunam):
        '''
        Update the plant levels.

        Parameters:
        taton (int): Index of the plant.
        data (dict): JSON data.
        paunam (str): Name of the plant.
        cpf (bool): Indicates PlantFood play count is to be updated.

        Returns:
        dict: Updated JSON data.
        '''
        nodename = 'PlantFoodPlayCount'
        skiplist = [nodename.lower(), 'planttier', 'plantfoodduration', "knockback"]

        def checkodr(stat, name, gap):
            for ele in skiplist:
                if not ele in name:
                    asce = True
                    desce = True
                    originallist = statval[0:gap+1]
                    for k in range(1, len(originallist)):
                        if originallist[k] > originallist[k-1]:
                            desce = False
                        elif originallist[k] < originallist[k-1]:
                            asce = False
                        if not asce and not desce:
                            break
                    if asce or desce:
                        if asce:
                            statval[-1] = 90745545
                        else:
                            statval[-1] = 0
                        stat["Values"] = statval
                    break
            return stat

        maxlvl = 1000
        levelcoins_values = [0] * maxlvl
        self.logs += f"{paunam} changes:\n"
        float_stats = data['objects'][taton]['objdata']['FloatStats']
        conditionvalues = {
            "damage": 22339,
            "dps": 22339,
            "cost": -2048,
            "hitpoints": 99999999,
            "packetcooldown": 0,
            "startingcooldown": 0,
            "expirationduration": 12999990,
            "velocity": 1124
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
                self.logs+= 'used checkodr for '
            self.logs += f'{name} last value\n{statval[-1]}\n'
            print(self.logs)
            if 'nut' in paunam and name == 'hitpoints':
                stat["Values"][-1] = 21474836479999999

        self.logs+= f"cpf was\n{cpf}\n"
        if cpf:
            iseligible = not any(skiplist[2] in stat.get('Name', '').lower() for stat in float_stats)
            self.logs+= f'Eligible\n{iseligible}\n'
            if iseligible:
                
                pfvalues = [1] * maxlvl
                pfvalues[-1] = 8707051
                pfst = False
                for stat in float_stats:
                    if stat.get('Name', '') == nodename:
                        pfst = stat
                        break
                if pfst:
                    self.logs+=f'{nodename} was already in float_stats\n'
                    pfst["Values"] = pfvalues
                else:
                    pfpc_dict = {
                        'Name': nodename,
                        'Values': pfvalues
                    }
                    float_stats.append(pfpc_dict)
                    self.logs+=f'{nodename} added in float_stats\n'
            else:
                pass

        data['objects'][taton]['objdata']['LevelCoins'] = levelcoins_values
        self.logs+="LevelCoins changed\n"
        data['objects'][taton]['objdata']['LevelXP'] = levelcoins_values
        self.logs+="LevelXP changed\n"
        data['objects'][taton]['objdata']['LevelCap'] = maxlvl
        self.logs += 'LevelCap changed\n'
        
        return data


if __name__ == "__main__":
    pass