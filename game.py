from js import document
import random
from collections import defaultdict

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
    "initialized": False
}

# --- Utility Functions ---
def print_output(text):
    try:
        out = document.getElementById('output')
        out.innerHTML += text + "<br/>"
        out.scrollTop = out.scrollHeight
    except Exception as e:
        print("Error in print_output:", e)

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

def start_game():
    try:
        document.getElementById('submit').addEventListener('click', on_submit)
        document.getElementById('command').addEventListener('keypress', on_enter)
        init_game()
    except Exception as e:
        print("Startup error:", e)

# --- Input Handling ---
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
start_game()
