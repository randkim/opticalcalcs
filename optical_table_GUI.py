import numpy as np
import PySimpleGUI as sg

sg.ChangeLookAndFeel('Dark') 

# =============================================================================
# windows_rows = [[sg.Text("Insert laser wavelength and beamwaist")],
#                  [sg.Text("")],
#                  [sg.Text("Wavelength:", pad=((20,0),0)), sg.In(size=(15,1)), sg.Text("Beamwaist:", pad=((20,0),0)), sg.In(size=(15,1))],
#                  [sg.Text("")],
#                  [sg.Submit(), sg.Cancel()]
#                  ]
# 
# window = sg.Window('Basic Data Input', windows_rows)
# 
# event, values = window.Read()
# window.Close()
# values = values
# =============================================================================

     

optical_table_layout = [      
           [sg.Graph(canvas_size=(800, 800), graph_bottom_left=(0,0), graph_top_right=(400, 400), background_color='white', key='graph')],   
           [sg.T("")],
           [sg.T('Device Input'), sg.Button('Laser'), sg.Button('Lens'), sg.Button('AOM'), sg.Button('Exit')],
           [sg.Button('List of available optical elements')]      
           ]      

optical_table_window = sg.Window('Optical Table Layout', optical_table_layout)      
optical_table_window.Finalize()   

graph = optical_table_window.Element('graph')   


available_optics_layout = [
        [sg.Button('Laser', size=(5,5)), sg.Image('laser.png')],
        [sg.Button('Lens', size=(5,5))]
        ]



while True:
    event, values = optical_table_window.Read()
    
    if event is 'Laser':
        laser = graph.DrawRectangle((90,70),(50,20), line_color='black')
        lasert_text = graph.DrawText('Laser', (75,75), color = 'black', font=None, angle=0)
        
    if event is 'List of available optical elements':
        available_optics_window = sg.Window('Available Optics', available_optics_layout)
        available_optics_window.Finalize()
        event2, values2 = available_optics_window.Read()
        
        while True:
            if event2 is 'Laser':
                laser = graph.DrawRectangle((90,70),(50,20), line_color='black')
                lasert_text = graph.DrawText('Laser', (75,75), color = 'black', font=None, angle=0)
                
                available_optics_window.Close()
        
        
    if event is 'Exit':
        optical_table_window.Close()


