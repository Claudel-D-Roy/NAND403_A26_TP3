import os
from PySide6.QtWidgets import (
  QWidget, 
  QVBoxLayout, 
  QGroupBox,
  QLabel,
  QSpinBox,
  QGridLayout,
  QPushButton)

class RandomAnimationUI(QWidget):

#-----------------Constructeur------------------------
    def __init__(self, animator):
        super().__init__()
        self.animator = animator
        self.setWindowTitle("Random Animation Generator")
        self.setMinimumWidth(400)
        self.build_ui()
#-----------------------------------------------------

#------------------Build UI---------------------------
    def build_ui(self): 

      #--------------------------------------------
      layout = QVBoxLayout(self)
      self.spins = {} 

      #--------------------------------------------
      group_timing = QGroupBox('Animation Timing')
      grid_timing = QGridLayout()

      self.spin_duration = QSpinBox()
      self.spin_duration.setRange(1, 9999)
      self.spin_duration.setValue(100)

      self.spin_step = QSpinBox()
      self.spin_step.setRange(1, 9999)
      self.spin_step.setValue(20)

      grid_timing.addWidget(QLabel('Durations (Frames):'), 0, 0)
      grid_timing.addWidget(self.spin_duration, 0, 1)
      grid_timing.addWidget(QLabel('Step (Frames):'), 0, 2)
      grid_timing.addWidget(self.spin_step, 0, 3)

      group_timing.setLayout(grid_timing)
      layout.addWidget(group_timing)
      #-------------------------------------------

      parameters = [('Translate Parameters', 'translate', 1),
                     ('Rotate Parameters', 'rotate', 1), 
                     ('Scale Parameters', 'scale', 1)]

      axes = ['x', 'y', 'z']
      bounds = ['min', 'max']

      #---------------------------------------------------
      for group_title, prefix, default_val in parameters: #groupe_title = translate parameters, prefixe = translate, default_val = 1, etc...
        group = QGroupBox(group_title)
        grid = QGridLayout()

        for row, bound in enumerate(bounds):
          for col, axis in enumerate(axes):

            label_text = f'{bound.capitalize()} {axis.upper()}:' #Met le nom du label avec les parameters
            spin_name = f'{prefix}_{bound}_{axis}' #Meme chose ici 

            spin = QSpinBox()
            spin.setRange(-1000, 1000) #Min et max du spin
            spin.setValue(default_val) #valeur par défault

            self.spins[spin_name] = spin # ajoute les valeurs 

            grid.addWidget(QLabel(label_text), row, col * 2)
            grid.addWidget(spin, row, (col * 2) + 1)

          group.setLayout(grid)
          layout.addWidget(group)

      button = QPushButton('Generate')
      button.clicked.connect(self.on_generate)
      layout.addWidget(button)
      #-------------------------------------------------
    

    #-------------------On-Generate---------------------
    def on_generate(self):
      values = {} 
      #aller chercher juste les valeur dans spins
      for name, spin in self.spins.items():
        values[name] = spin.value()

      #Appel l'animator
      self.animator.generate(self.spin_duration.value(), 
                             self.spin_step.value(), 
                             values)
    #-------------------------------------------------