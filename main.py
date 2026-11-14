import os
import sys

#aller chercher le chemin pour le file et le folder en absolute
absolute_file_path = os.path.abspath(__file__) #__file__ is an Alias pour python 
absolute_folder_path = os.path.dirname(absolute_file_path)

#absolute_path = os.path.realpath(os.path.curdir), permet d'aller chercher le current directiory

#Ajoute le path du fichier au path de python
sys.path.append(absolute_folder_path)

#Après on import
import ui 
import animator 
import importlib
importlib.reload(ui)
importlib.reload(animator)

      
def main():
    global tool_window
    try:
        tool_window.close()
    except Exception:
        pass
    #passe l'animator au ui, comme ca juste le main s'occupe des imports 
    random_animator = animator.RandomAnimationAnim()
    tool_window = ui.RandomAnimationUI(random_animator)
    tool_window.show()

main()