import sys
import difflib
import random
import sqlite3
from collections import deque
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

campus_map = {
    "main entrance": ["admin block", "food court", "mini mart", "temple"],
    "admin block": ["main entrance", "faculty block", "engineering block", "basketball court", "canteen"],
    "food court": ["main entrance", "hostel", "mini mart"],
    "hostel": ["food court", "river", "football court"],
    "guest house": ["main entrance", "temple"],
    "faculty block": ["admin block", "engineering block", "basketball court"],
    "basketball court": ["faculty block", "admin block", "football court"],
    "football court": ["basketball court", "hostel", "engineering block"],
    "engineering block": ["faculty block", "admin block", "football court"],
    "mini mart": ["main entrance", "food court"],
    "temple": ["main entrance", "guest house"],
    "river": ["hostel", "football court"],
    "exit": ["main entrance"],
    "canteen": ["admin block"]
}

departments = {
    "admin block": "Admin Block is near the Main Entrance.",
    "food court": "Food Court is located behind the Engineering Block.",
    "hostel": "Student Hostels, Blocks H & H2 for girls.",
    "guest house": "Guest House near the Temple.",
    "faculty block": "Faculty Offices, Block F.",
    "basketball court": "Basketball Court behind the Food Court.",
    "football court": "Football Ground near Hostels.",
    "engineering block": "Engineering Block, Block E.",
    "main entrance": "Main Entrance of Chanakya University.",
    "mini mart": "Mini Mart near the Hostel.",
    "temple": "Campus Temple near Guest House.",
    "river": "Campus River bordering the Hostels.",
    "exit": "Exit from Main Entrance.",
    "canteen": "Canteen is in the Admin Block."
}

faqs = {
    "admissions": "You can apply online via the official website: www.chanakyauniv.edu/admissions.",
    "fees": "Fee details are available online: https://www.chanakyauniv.edu/fees-portal",
    "btech fees": "BTech fees are available online here: https://www.chanakyauniv.edu/fees-portal#btech",
    "mtech fees": "MTech fees are available online here: https://www.chanakyauniv.edu/fees-portal#mtech",
    "mba fees": "MBA fees are available online here: https://www.chanakyauniv.edu/fees-portal#mba",
    "hostels": "Hostels are located near the main gate. Boys Hostel - Block H, Girls Hostel - Block H2.",
    "placement": "Placement cell is in Block A, 1st floor. Contact: placement@chanakyauniv.edu.",
    "food court": "Food Court is located near the Main Entrance, serving breakfast, lunch, and snacks.",
    "sports": "Basketball and Football courts are located behind the Food Court."
}

class ChatBotBackend:
    def __init__(self):
        self.conn, self.cursor = self.init_db()
        self.greetings = ["hi", "hello", "hey", "hola", "namaste", "konichiwa"]
        self.greeting_responses = [
            "Hello! Welcome to Chanakya University!",
            "Hi there! How can I help you today?",
            "Hey! Need any campus info?",
            "Greetings! How can I assist you?",
            "Namaste! Welcome!"
        ]
        self.farewells = ["bye", "goodbye", "see you"]
        self.farewell_responses = [
            "Goodbye! Have a great day at Chanakya University.",
            "See you soon!",
            "Bye! Take care!"
        ]
        self.thanks = ["thankyou", "thanks", "thx"]
        self.thanks_responses = ["You're welcome!", "No problem!", "Glad to help!"]
        self.okay_responses = ["Ok!", "Got it!", "Sure!"]
        self.all_keywords = list(departments.keys()) + list(faqs.keys())

    def init_db(self):
        conn = sqlite3.connect("campus.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS departments (name TEXT PRIMARY KEY, info TEXT)''')
        for dept, info in departments.items():
            c.execute("INSERT OR REPLACE INTO departments (name, info) VALUES (?, ?)", (dept, info))
        conn.commit()
        return conn, c

    def autocorrect(self, word):
        matches = difflib.get_close_matches(word.lower(), self.all_keywords, n=1, cutoff=0.6)
        return matches[0] if matches else None

    def get_department_info(self, dept):
        dept = dept.lower()
        self.cursor.execute("SELECT info FROM departments WHERE name=?", (dept,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def find_path(self, start, end):
        start = start.lower()
        end = end.lower()
        if start not in campus_map or end not in campus_map:
            return None
        queue = deque([[start]])
        visited = set()
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == end:
                return path
            if node not in visited:
                visited.add(node)
                for neighbor in campus_map[node]:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return None

    def get_response(self, user_input):
        user_input = user_input.lower().strip()

        if user_input in self.greetings:
            return random.choice(self.greeting_responses)
        elif user_input in self.farewells:
            return random.choice(self.farewell_responses)
        elif user_input in self.thanks:
            return random.choice(self.thanks_responses)
        elif user_input in ["okay", "ok"]:
            return random.choice(self.okay_responses)
        elif "where is" in user_input:
            place = user_input.replace("where is", "").strip()
            corrected_place = self.autocorrect(place)
            info = self.get_department_info(corrected_place) if corrected_place else None
            return info if info else "Sorry, I don't have details about that place."
        elif "what locations" in user_input or "list locations" in user_input:
            locs = ", ".join([loc.title() for loc in departments.keys()])
            return "Chanakya University has the following locations: " + locs
        elif "fees" in user_input:
            if "btech" in user_input:
                return faqs.get("btech fees", "Fee information not available.")
            elif "mtech" in user_input:
                return faqs.get("mtech fees", "Fee information not available.")
            elif "mba" in user_input:
                return faqs.get("mba fees", "Fee information not available.")
            else:
                return faqs.get("fees", "Fee information not available.")
        else:
            corrected_input = self.autocorrect(user_input)
            if corrected_input in departments:
                info = self.get_department_info(corrected_input)
                return info if info else "Sorry, info not found."
            elif corrected_input in faqs:
                return faqs[corrected_input]
            else:
                return "Sorry, I can help with 'where is <place>', FAQs, course fees, paths, or 'what locations'."

class MapWindow(QWidget):
    def __init__(self, start, end, api_key):
        super().__init__()
        self.setWindowTitle(f"Map: {start} → {end}")
        self.setGeometry(300, 200, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.webview = QWebEngineView()
        layout.addWidget(self.webview)

        html = f"""
        <!DOCTYPE html>
        <html>
          <head>
            <title>Directions</title>
            <script src="https://maps.googleapis.com/maps/api/js?key={api_key}"></script>
            <script>
              function initMap() {{
                var directionsService = new google.maps.DirectionsService();
                var directionsRenderer = new google.maps.DirectionsRenderer();
                var map = new google.maps.Map(document.getElementById('map'), {{
                  zoom: 15,
                  center: {{lat: 25.5941, lng: 85.1376}}
                }});
                directionsRenderer.setMap(map);
                directionsService.route({{
                  origin: '{start}',
                  destination: '{end}',
                  travelMode: 'WALKING'
                }}, function(response, status) {{
                  if (status === 'OK') {{
                    directionsRenderer.setDirections(response);
                  }} else {{
                    alert('Directions request failed due to ' + status);
                  }}
                }});
              }}
            </script>
          </head>
          <body onload="initMap()">
            <div id="map" style="height:100%; width:100%;"></div>
          </body>
        </html>
        """
        self.webview.setHtml(html)

class ChatBotUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chanakya University Chatbot")
        self.setGeometry(200, 200, 600, 500)
        self.bg_image_path = r"C:\Users\LUCKY\OneDrive\Desktop\Y31\Documents\Desktop\New folder (17)\Screenshot 2025-09-10 131732.png"
        self.set_background(self.bg_image_path)
        self.backend = ChatBotBackend()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("background: rgba(255,255,255,180); font-size:14px; border-radius:10px; padding:10px;")
        layout.addWidget(self.chat_area)
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setStyleSheet("background: rgba(255,255,255,200); font-size:14px; padding:8px; border-radius:10px;")
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("background: rgba(0,120,215,180); color:white; font-size:14px; border-radius:10px; padding:8px;")
        self.send_button.clicked.connect(self.handle_user_input)
        self.input_box.returnPressed.connect(self.handle_user_input)
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        self.append_message("Bot", "Hi! Ask me about campus locations, fees, directions, or anything about Chanakya University.")

    def set_background(self, image_path):
        palette = self.palette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.set_background(self.bg_image_path)
        super().resizeEvent(event)

    def append_message(self, sender, message):
        self.chat_area.append(f"<b>{sender}:</b> {message}")

    def handle_user_input(self):
        user_text = self.input_box.text().strip()
        if not user_text:
            return
        self.append_message("You", user_text)
        self.input_box.clear()

        if "path from" in user_text or "directions from" in user_text:
            words = user_text.split()
            if "from" in words and "to" in words:
                start_idx = words.index("from") + 1
                end_idx = words.index("to") + 1
                start = words[start_idx].title()
                end = words[end_idx].title()
                api_key = "YOUR_GOOGLE_MAPS_API_KEY"  # <-- replace with your key
                self.map_window = MapWindow(start, end, api_key)
                self.map_window.show()
                return

        response = self.backend.get_response(user_text)
        self.append_message("Bot", response)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatBotUI()
    window.show()
    sys.exit(app.exec_())
