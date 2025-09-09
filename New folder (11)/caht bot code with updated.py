import difflib
import random
import sqlite3
from collections import deque

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

def autocorrect(word, word_list):
    matches = difflib.get_close_matches(word.lower(), word_list, n=1, cutoff=0.6)
    return matches[0] if matches else None

def find_path(start, end):
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

def init_db():
    conn = sqlite3.connect("campus.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS departments (name TEXT PRIMARY KEY, info TEXT)''')
    for dept, info in departments.items():
        c.execute("INSERT OR REPLACE INTO departments (name, info) VALUES (?, ?)", (dept, info))
    conn.commit()
    return conn, c

def get_department_info(c, dept):
    dept = dept.lower()
    c.execute("SELECT info FROM departments WHERE name=?", (dept,))
    result = c.fetchone()
    return result[0] if result else None

def chatbot():
    conn, c = init_db()
    print("Hello! I am your Chanakya University chatbot :). How can I help you?")
    print("Type 'exit' to leave the chat.")
    print("You can ask about locations ('where is <place>'), FAQs like fees/hostel/food/sports/admissions, or 'what locations' to see all campus places.")

    greetings = ["hi", "hello", "hey", "hola", "namaste", "konichiwa"]
    greeting_responses = [
        "Hello! Welcome to Chanakya University!",
        "Hi there! How can I help you today?",
        "Hey! Need any campus info?",
        "Greetings! How can I assist you?",
        "Namaste! Welcome!"
    ]
    farewells = ["bye", "goodbye", "see you"]
    farewell_responses = [
        "Goodbye! Have a great day at Chanakya University.",
        "See you soon!",
        "Bye! Take care!"
    ]
    thanks = ["thankyou", "thanks", "thx"]
    thanks_responses = ["You're welcome!", "No problem!", "Glad to help!"]
    okay_responses = ["Ok!", "Got it!", "Sure!"]

    all_keywords = list(departments.keys()) + list(faqs.keys())

    while True:
        user_input = input("\nYou: ").lower().strip()
        if user_input == "exit":
            print("Bot: Goodbye! Have a great day at Chanakya University.")
            break
        elif user_input in greetings:
            print("Bot:", random.choice(greeting_responses))
        elif user_input in farewells:
            print("Bot:", random.choice(farewell_responses))
        elif user_input in thanks:
            print("Bot:", random.choice(thanks_responses))
        elif user_input in ["okay", "ok"]:
            print("Bot:", random.choice(okay_responses))
        elif "where is" in user_input:
            place = user_input.replace("where is", "").strip()
            corrected_place = autocorrect(place, list(departments.keys()))
            info = get_department_info(c, corrected_place) if corrected_place else None
            print(f"Bot: {info}" if info else "Bot: Sorry, I don't have details about that place.")
        elif "path from" in user_input or "directions from" in user_input:
            words = user_input.split()
            if "from" in words and "to" in words:
                start_idx = words.index("from") + 1
                end_idx = words.index("to") + 1
                start = words[start_idx]
                end = words[end_idx]
                path = find_path(start, end)
                if path:
                    print("Bot: Path:", " -> ".join(path))
                else:
                    print("Bot: No path found between these locations.")
            else:
                print("Bot: Please use format 'path from <start> to <end>'.")
        elif "what locations" in user_input or "list locations" in user_input:
            print("Bot: Chanakya University has the following locations:")
            for loc in departments.keys():
                print(f"- {loc.title()}")
        elif "fees" in user_input:
            if "btech" in user_input:
                print("Bot:", faqs["btech fees"])
            elif "mtech" in user_input:
                print("Bot:", faqs["mtech fees"])
            elif "mba" in user_input:
                print("Bot:", faqs["mba fees"])
            else:
                print("Bot:", faqs["fees"])
        else:
            corrected_input = autocorrect(user_input, all_keywords)
            if corrected_input in departments:
                info = get_department_info(c, corrected_input)
                print(f"Bot: {info}" if info else "Bot: Sorry, info not found.")
            elif corrected_input in faqs:
                print(f"Bot: {faqs[corrected_input]}")
            else:
                print("Bot: Sorry, I can help with 'where is <place>', FAQs, course fees, paths, or 'what locations'.")

if __name__ == "__main__":
    chatbot()
