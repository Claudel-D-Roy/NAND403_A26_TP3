import random
from maya import cmds

class RandomAnimationAnim():
    #Le frame au début de l'animation, pourrait être modifier
    START_FRAME = 0

#---------------constructeur----------------------
    def __init__(self):
        self.frames = []
#-------------------------------------------------


#---------------Generate--------------------------
    def generate(self, duration, step, values):   
        objects = cmds.ls(selection= True, type='transform') #Recupère object sélectionner

        if not objects: #S'assure que quelque chose est séléctionner, fait un warning en bas de l'écran de maya 
            cmds.warning('Sélectionne au moins un objet.')
            return
        
        self.frames = self.compute_frames(duration, step) #Appel compute_frames, donne les places ou on doit mettre les clé
        ranges = self.group_ranges(values) #appel groupe_ranges donne les valeurs min max

        cmds.undoInfo(openChunk=True, chunkName="RandomAnimation") #Ctrl + Z
        try:
            for obj in objects:  # pour chaque object séléctionner, on va voir les 9 attributs (translate min x, translate max x, etc.. )
                for attribute, bound in ranges.items(): 
                    self.animate_attribute(obj, attribute, bound['min'], bound['max']) # on appel animate_attribute avec les attributs avec les min max
            cmds.playbackOptions(minTime=self.START_FRAME, maxTime = self.frames[-1]) #Ajuste du frame 1 au dernier pour que l'anime puisse avoir la bonne durée

        finally: 
            cmds.undoInfo(closeChunk=True)#Ctrl + Z
#-------------------------------------------------

#---------------Compute-Frames--------------------
    def compute_frames(self, duration, step):
        end_frame = self.START_FRAME + duration   #ex duration = 100 et step = 20, end_frame ici donne 100 vu que start_frame = 0
        frames = list(range(self.START_FRAME, end_frame, step)) # donne la liste de frame avec le step, donc [0, 20, 40, 60.. etc.. ] vu que step est de 20
        frames.append(end_frame) #ajoute 100 car la dernière clé tombe toujours a la fin 
        return frames
#-------------------------------------------------

#----------------Group-Ranges---------------------
    def group_ranges(self, values):
        ranges = {}
        for key, value in values.items():
            attribute, bound, axis = key.split('_') # a cause de translate_min_x, le nom de mon spinbox, découpe le string
            maya_attribute = f'{attribute}{axis.upper()}' # reconstruit 'translate' + 'X'  donne 'translateX' pour Maya
            ranges.setdefault(maya_attribute, {})[bound] = value #Crée un dictionnaire vide si il existe pas déjà, range le min max dans bound
        return ranges #Donne quelque chose dans le genre {'translateX': {'min': -5, 'max': 5}, ....etc..}
#-------------------------------------------------

#----------------Animate-Attribute----------------
    def animate_attribute(self, obj, attribute, min_value, max_value):
        cmds.cutKey(obj, attribute = attribute, clear = True) #Efface les anciennes clés

        random_values = []
        for _ in self.frames[:-1]: # pour chaque frame sauf le dernier, tire un chiffre aléatoire en tre le min et max et ajoute a la liste. 
            #_ veux dire qu'on utlise pas la valeur de la boucle, juste le nombre de répétitions
            value = random.uniform(min_value, max_value)
            random_values.append(value)

        random_values.append(random_values[0]) #ajoute une en dernier une copie de la premiere valeur pour que sa boucle

        for frame, value in zip(self.frames, random_values): # zip = associe chaque fram a sa valeur, ex frame 0 avec valeur 1, frame 20 avec valeur 2, etc.. 
            cmds.setKeyframe(obj, attribute=attribute, time=frame, value=value)   # Crée la clé
#-------------------------------------------------
                