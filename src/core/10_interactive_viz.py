"""
AI33-MPOPT: Interactive Visualization Module
Created by Rolando Rivero (2024)
https://github.com/Rivero-ai/AI33-MPOPT

Implements interactive visualization for 33-multiverse system:

Interactive Features:
- Real-time 3D rotation
- Universe selection and focus
- Energy flow animation
- Force field toggling
- Zone highlighting
- Information display
- Dynamic camera control

Interface Controls:
- Mouse rotation/zoom
- Universe selection
- Force visibility toggles
- Energy flow controls
- Information panels
- Camera presets

Book: "The Platonic Solid Big Bang"
Registration: TXu 2-426-457
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, CheckButtons
from mpl_toolkits.mplot3d import Axes3D

class InteractiveVisualization:
    def __init__(self):
        """Initialize interactive visualization"""
        self.setup_interface()
        self.initialize_controls()
        self.configure_interaction()
        
    def setup_interface(self):
        """Configure visualization interface"""
        self.interface = {
            'main_view': {
                'size': (1200, 800),
                'position': (0, 0),
                'background': 'black',
                'grid': False
            },
            'controls': {
                'position': (1000, 0),
                'size': (200, 800),
                'background': 'darkgray'
            },
            'info_panel': {
                'position': (0, 600),
                'size': (1000, 200),
                'background': 'black',
                'text_color': 'white'
            }
        }
        
    def initialize_controls(self):
        """Set up interactive controls"""
        self.controls = {
            'universe_select': {
                'type': 'dropdown',
                'options': range(1, 34),
                'position': (1020, 750),
                'callback': self.select_universe
            },
            'force_toggles': {
                'type': 'checkbuttons',
                'options': ['Strong', 'Weak', 'EM', 'Gravity'],
                'position': (1020, 650),
                'callback': self.toggle_force
            },
            'energy_flow': {
                'type': 'slider',
                'range': (0, 1),
                'position': (1020, 550),
                'callback': self.adjust_energy
            },
            'camera_presets': {
                'type': 'buttons',
                'options': ['Top', 'Side', 'Iso'],
                'position': (1020, 450),
                'callback': self.set_camera
            }
        }
        
    def configure_interaction(self):
        """Set up interaction handlers"""
        self.interactions = {
            'mouse_rotation': {
                'enabled': True,
                'sensitivity': 0.5,
                'callback': self.rotate_view
            },
            'mouse_zoom': {
                'enabled': True,
                'sensitivity': 0.1,
                'callback': self.zoom_view
            },
            'mouse_select': {
                'enabled': True,
                'callback': self.handle_selection
            }
        }

    def create_interface(self):
        """Create main visualization interface"""
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(16, 9))
        self.setup_main_view()
        self.setup_control_panel()
        self.setup_info_panel()
        
    def setup_main_view(self):
        """Set up main 3D visualization area"""
        self.main_ax = self.fig.add_subplot(111, projection='3d')
        self.main_ax.set_facecolor('black')
        self.setup_lighting()
        self.setup_camera()
        
    def setup_control_panel(self):
        """Create control panel with widgets"""
        # Universe Selection
        self.universe_selector = CheckButtons(
            plt.axes([0.85, 0.8, 0.1, 0.1]),
            ['Green', 'Yellow', 'Blue', 'Orange']
        )
        self.universe_selector.on_clicked(self.toggle_zone)
        
        # Force Field Controls
        self.force_controls = CheckButtons(
            plt.axes([0.85, 0.6, 0.1, 0.1]),
            ['Strong', 'Weak', 'EM', 'Gravity']
        )
        self.force_controls.on_clicked(self.toggle_force)
        
        # Energy Flow Slider
        self.energy_slider = Slider(
            plt.axes([0.85, 0.5, 0.1, 0.03]),
            'Energy', 0, 1, valinit=0.5
        )
        self.energy_slider.on_changed(self.update_energy)
        
    def setup_info_panel(self):
        """Create information display panel"""
        self.info_ax = plt.axes([0.1, 0.1, 0.7, 0.2])
        self.info_ax.axis('off')
        
    def toggle_zone(self, label):
        """Toggle visibility of selected zone"""
        if label == 'Green':
            self.toggle_green_zone()
        elif label == 'Yellow':
            self.toggle_yellow_zone()
        elif label == 'Blue':
            self.toggle_blue_zone()
        elif label == 'Orange':
            self.toggle_orange_zone()
        self.update_display()
        
    def toggle_force(self, label):
        """Toggle force field visibility"""
        if label in ['Strong', 'Weak', 'EM', 'Gravity']:
            self.toggle_force_field(label)
            self.update_force_display()
            
    def update_energy(self, val):
        """Update energy flow visualization"""
        self.energy_level = val
        self.update_energy_flow()
        self.update_display()
        
    def handle_selection(self, event):
        """Handle mouse selection of universe"""
        if event.inaxes == self.main_ax:
            self.select_nearest_universe(event)
            self.update_info_panel()
            
    def select_nearest_universe(self, event):
        """Find and select nearest universe to click"""
        # Implementation for universe selection
        pass
        
    def update_info_panel(self):
        """Update information panel with selected universe details"""
        if hasattr(self, 'selected_universe'):
            info = self.get_universe_info(self.selected_universe)
            self.display_universe_info(info)
            
    def animate_rotation(self):
        """Create smooth rotation animation"""
        self.rotation_angle = 0
        self.rotation = animation.FuncAnimation(
            self.fig, self.update_rotation,
            frames=360, interval=50
        )
        
    def update_rotation(self, frame):
        """Update view rotation"""
        self.main_ax.view_init(elev=30, azim=frame)
        self.update_display()
        
    def show(self):
        """Display interactive visualization"""
        plt.show()
