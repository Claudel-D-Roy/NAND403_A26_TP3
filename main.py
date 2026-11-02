import os
import sys

#aller chercher le chemin pour le file et le folder en absolute
absolute_file_path = os.path.abspath(__file__) #__file__ is an Alias pour python 
absolute_folder_path = os.path.dirname(absolute_file_path)

#absolute_path = os.path.realpath(os.path.curdir), permet d'aller chercher le current directiory
#print les resultats 
print(f" le chemin :  {absolute_file_path}")
print(f" le dossier :  {absolute_folder_path}")
#print(sys.path)

#Ajoute le path du fichier au path de python
sys.path.append(absolute_folder_path)
#Après on import
from folder.ui import MyClass


my_class = MyClass()
my_class.print_variable()

