#import statements
import sys
import folium
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer, QUrl
import requests
import os

#url where data is stored in json format
url = "https://eonet.gsfc.nasa.gov/api/v3/events"
#output type
output = 'json'

map_center = [40.7128, -74.006]

#current wokring directory for storage of html file
cwd = os.getcwd()

html_path = cwd+'/folium_map.html'

#defining the main window of the app
class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #setting up main window
        self.setWindowTitle("Natural Disaster Treacking App")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        #adding QWebEngineView widget so that html file where map is stored can be seen
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        #timer to update the map every two minutes
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_map)
        self.timer.start(120000)
        self.update_map()


    #function to update the map
    def update_map(self):

        #function to generate the new map
        def generate_folium_map():
            folium_map = folium.Map(location=map_center, zoom_start=2)

            #getting the data from the url defined before
            response = requests.get(f'{url}?format={output}', verify=False).json()

            #variables to store all the data got from the webpage
            coords = []
            descriptions = []
            description_index = 0

            #getting the data, formatting it and storing it
            for event in response['events'][0:10]:
                coords.append([event['geometry'][0]['coordinates'][1],event['geometry'][0]['coordinates'][0]])
                name = event['title']
                kind = event['categories'][0]['title']
                date = event['geometry'][0]['date']
                description = name+'\n'+'\n'+kind+'\n'+date
                descriptions.append(description)

            #creating markers for incidents
            for coord in coords:
                folium.Marker(location=coord, popup=descriptions[description_index]).add_to(folium_map)
                description_index += 1

            #saving the map
            folium_map.save(html_path)
        
        generate_folium_map()

        #displaying the html map on the main window
        map_url = QUrl.fromLocalFile(html_path)
        self.web_view.load(map_url)


if __name__ == "__main__":
    #running the whole code
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())
