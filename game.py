from js import document
import random
from collections import defaultdict
from pyodide.ffi import create_proxy


# --- Data Definitions ---
areas = {
    "Villa Interior": ["Library", "Dining Room", "Study"],
    "Gardens": ["Fountain", "Greenhouse", "Pathway"],
    "Docks": ["Boathouse", "Pier", "Lighthouse"]
}

room_templates = []
for area, subrooms in areas.items():
    for room in subrooms:
        room_templates.append({
            "name": room,
            "area": area,
            "clue": None,
            "discovered": False,
            "occupants": [],
            "item_found": None
        })

suspect_templates = [
    {"name": "Doctor", "goal": None, "alibi": None, "secrets": [], "is_murderer": False, "knows_about": [], "schedule": [], "dialogue_intro": "I'm just here to help. I had nothing to do with the murder.", "dialogue_defensive": "How dare you! I'm a respected professional!"},
    {"name": "Butler", "goal": None, "alibi": None, "secrets": [], "is_murderer": False, "knows_about": [], "schedule": [], "dialogue_intro": "It’s my job to keep things in order. Even in death.", "dialogue_defensive": "Surely you don’t think *I* would harm my employer?"},
    {"name": "Chef", "goal": None, "alibi": None, "secrets": [], "is_murderer": False, "knows_about": [], "schedule": [], "dialogue_intro": "A good dish can bring peace. I only served food.", "dialogue_defensive": "My hands smell like garlic, not blood!"},
    {"name": "Artist", "goal": None, "alibi": None, "secrets": [], "is_murderer": False, "knows_about": [], "schedule": [], "dialogue_intro": "Beauty is truth. I only paint what I see.", "dialogue_defensive": "Are you accusing me because I'm different?"}
]

causes_of_death = ["Poisoning", "Stabbing", "Blunt Force"]
motives = ["Inheritance", "Revenge", "Love Triangle", "Cover-up"]

# --- Game State ---
game_state = {
    "murderer": None,
    "cause": None,
    "motive": None,
    "suspects": [],
    "rooms": [],
    "clues": {},
    "notes": [],
    "visited": [],
    "accused": False,
    "in_accusation": False,
    "interactions": defaultdict(list),
    "initialized": False,
    "menu_state": "main"
}

# --- Utility Functions ---
def print_output(text):
    try:
        out = document.getElementById('output')
        out.innerHTML += text + "<br/>"
        out.scrollTop = out.scrollHeight
    except Exception as e:
        print("Error in print_output:", e)

# --- Game Logic ---
def generate_mystery():
    murderer = random.choice(game_state["suspects"])
    murderer["is_murderer"] = True
    game_state["murderer"] = murderer
    game_state["cause"] = random.choice(causes_of_death)
    game_state["motive"] = random.choice(motives)

    time_slots = ["6AM", "9AM", "12PM", "3PM", "6PM", "9PM", "12AM", "3AM", "5AM"]

    for s in game_state["suspects"]:
        available_rooms = game_state["rooms"][:]
        random.shuffle(available_rooms)
        s["schedule"] = []
        for i, t in enumerate(time_slots):
            room = available_rooms[i % len(available_rooms)]
            s["schedule"].append({"room": room["name"], "time": t})
            room["occupants"].append({"suspect": s["name"], "time": t})

        s["goal"] = random.choice(motives)
        s["secrets"].append(random.choice([
            "Had a feud with the victim",
            "Was hiding evidence",
            "In debt",
            "Secret affair"
        ]))
        s["alibi"] = random.choice([
            "Claims to have been in the kitchen",
            "Says they were outside",
            "No one saw them",
            "Alibi checked out"
        ])

def place_clues():
    for room in game_state["rooms"]:
        hint = f"You find a clue hinting the motive may be: {random.choice(motives)}."
        game_state["clues"][room["name"]] = hint

def find_overlaps():
    interaction_map = defaultdict(list)
    for s in game_state["suspects"]:
        for entry in s["schedule"]:
            key = (entry["room"], entry["time"])
            interaction_map[key].append(s["name"])

    for key, participants in interaction_map.items():
        if len(participants) > 1:
            game_state["interactions"][key] = participants

# --- Game Setup ---
def init_game():
    game_state["rooms"] = [dict(room) for room in room_templates]
    game_state["suspects"] = [dict(s) for s in suspect_templates]
    generate_mystery()
    place_clues()
    find_overlaps()
    show_intro()
    show_main_menu()
    game_state["initialized"] = True

# --- Display Functions ---
def show_intro():
    print_output("\u2705 Game initialized")
    print_output("Welcome to the Lake Como Murder Mystery!")
    print_output("A murder occurred last night. Investigate the villa to uncover the truth.")
    print_output("The investigation begins at 7AM on June 11th, 2025.")

def show_main_menu():
    print_output("\nMain Menu:")
    print_output("1. Visit a room")
    print_output("2. View your notes")
    print_output("3. Make an accusation")
    print_output("Enter the number of your choice:")

def show_room_menu():
    print_output("\nWhere would you like to go?")
    for idx, room in enumerate(game_state["rooms"], 1):
        print_output(f"{idx}. {room['name']} ({room['area']})")
    print_output("Enter the number of the room to visit:")

def view_notes():
    print_output("\nYour Notes:")
    if not game_state["notes"]:
        print_output("You have no notes yet.")
    else:
        for note in game_state["notes"]:
            print_output(f"- {note}")
    show_main_menu()

def visit_room(room):
    if room["name"] in game_state["visited"]:
        print_output(f"You return to the {room['name']}.")
    else:
        print_output(f"You enter the {room['name']} for the first time.")
        game_state["visited"].append(room["name"])
        clue = game_state["clues"][room["name"]]
        print_output(clue)
        game_state["notes"].append(f"Clue from {room['name']}: {clue}")
    show_main_menu()

def make_accusation():
    print_output("\nWho do you accuse as the murderer?")
    for idx, s in enumerate(game_state["suspects"], 1):
        print_output(f"{idx}. {s['name']}")
    print_output("Enter the number of the suspect:")

def process_accusation(cmd):
    try:
        choice = int(cmd)
    except:
        print_output("Please enter a number.")
        return
    if 1 <= choice <= len(game_state["suspects"]):
        accused = game_state["suspects"][choice - 1]
        if accused["is_murderer"]:
            print_output(f"Correct! The {accused['name']} committed the murder by {game_state['cause']} due to {game_state['motive']}.")
        else:
            print_output(f"Wrong! The murderer was the {game_state['murderer']['name']}.")
        print_output("Game over. Refresh to play again.")
        disable_input()
    else:
        print_output("Invalid suspect.")
        make_accusation()

def disable_input():
    btn = document.getElementById('submit')
    btn.removeEventListener('click', on_submit)
    btn.disabled = True
    document.getElementById('command').disabled = True

# --- Input Handling ---
def handle_input(cmd):
    if not game_state["initialized"]:
        init_game()
        return

    if game_state["menu_state"] == "main":
        if cmd == "1":
            game_state["menu_state"] = "room"
            show_room_menu()
        elif cmd == "2":
            view_notes()
        elif cmd == "3":
            game_state["menu_state"] = "accuse"
            make_accusation()
        else:
            print_output("Invalid input. Please enter a valid number.")
            show_main_menu()

    elif game_state["menu_state"] == "room":
        if cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < len(game_state["rooms"]):
                game_state["menu_state"] = "main"
                visit_room(game_state["rooms"][idx])
            else:
                print_output("Invalid room selection.")
                show_room_menu()
        else:
            print_output("Invalid room input. Please enter a number.")
            show_room_menu()

    elif game_state["menu_state"] == "accuse":
        process_accusation(cmd)


def on_submit(e):
    try:
        cmd = document.getElementById('command').value.strip()
        document.getElementById('command').value = ''
        if not cmd:
            return
        print_output(f"> {cmd}")
        handle_input(cmd)
    except Exception as e:
        print_output(f"Submission error: {e}")

def on_enter(e):
    if e.key == "Enter":
        on_submit(e)

# --- Run ---
def start_game():
    try:
        print_output("🟢 start_game called")
        submit_proxy = create_proxy(on_submit)
        enter_proxy = create_proxy(on_enter)
        document.getElementById('submit').addEventListener('click', submit_proxy)
        document.getElementById('command').addEventListener('keypress', enter_proxy)
        init_game()
    except Exception as e:
        print_output(f"❌ Startup error: {e}")


start_game()