from js import document
import random
from collections import defaultdict
from pyodide.ffi import create_proxy

# --- Phase 1 Static Data ---

# Ground Truth for the Murder
GROUND_TRUTH = {
    "murderer": "Dakota Marino",
    "method": "Danshen extract poisoning (interaction with medication)",
    "motive": "Negligence/Prove Dr. Moretti wrong",
    "location": "Cristiano's Study",
    "time": "~3:00 AM"
}

# Game Introduction Text (from Script)
GAME_INTRODUCTION = """
Welcome to Murder Mystery on Lake Como

The summer air hangs heavy as the phone jars you awake in your Milan apartment. It's just past 5:00 AM on June 11th. You are one of Milan's most renowned detectives, known for untangling the most complex cases, and your skills are urgently needed.

An urgent call summons you through the early morning light to the shores of Lake Como, specifically to the opulent Villa Patrizi. The villa's owner, Cristiano Patrizi, a powerful and self-made industrialist, has been found dead in his private study. The discovery was made around 4:00 AM by the distraught butler, Antonello Pisani.

Just hours earlier, the villa was the scene of the final night of a lavish, weeks-long celebration for Cristiano's 50th birthday. What began as a grand affair with guests flying in from across the globe had simmered down over the last three days to an intimate gathering of close friends, family, and associates staying at the villa. Your investigation will need to reconstruct the events of June 10th, starting from 6:00 AM that morning, up until the body was discovered at 4:00 AM on June 11th.

Now, the laughter has died, replaced by suspicion and fear. The serene beauty of Lake Como hides a dark secret. Everyone who remained at the villa – both the esteemed guests and the dedicated staff – is now confined to the grounds. They are all suspects, and no one leaves until you uncover the truth.

Meet the Suspects:
*(Character introductions will be listed here based on the 'Script' document)*

Your Investigation:

As the Detective, the villa and its grounds are yours to investigate.
Explore Locations: Search every room, from the grand Library to the shadowy Boathouse, for physical clues – a dropped item, a revealing note, environmental details that seem out of place.
Converse with Suspects: Interview everyone present. Question their alibis, probe their motives, and uncover their secrets. Listen carefully – testimonies might conflict, revealing lies or hidden truths. Remember, these individuals have complex relationships and histories; what they know about each other can be as crucial as what they reveal about themselves.
Discover and Log Clues: Every piece of evidence, physical or testimonial, will be recorded in your detective's notebook. Analyze your findings, connect the dots, and separate the facts from the red herrings.

Your goal is to piece together the events of the last 24 hours, identify the murderer, determine their motive, and pinpoint the method of death. Only when you are certain you have solved the puzzle should you make your accusation.

The truth is hidden somewhere within the walls of Villa Patrizi. It's up to you to bring it into the light. Good luck, Detective.
"""

# Locations (Based on Script)
# We can enhance the existing `areas` and `room_templates` slightly
# Let's redefine them here for clarity based on the Script locations.
LOCATIONS = [
    # Villa Interior
    {"id": "library", "name": "Library", "area": "Villa Interior", "description": "Lined with floor-to-ceiling bookshelves, filled with old volumes. Smells faintly of leather and dust."},
    {"id": "dining_room", "name": "Dining Room", "area": "Villa Interior", "description": "A grand room with a long, polished table. Remnants of last night's lavish dinner have been cleared, but the formal setting remains."},
    {"id": "study", "name": "Cristiano's Study", "area": "Villa Interior", "description": "Cristiano's private sanctuary. Expensive furniture, a large desk, and personal belongings. The air feels heavy."},
    {"id": "kitchen", "name": "Kitchen", "area": "Villa Interior", "description": "A large, professional kitchen. Gleaming stainless steel surfaces, now quiet after the party preparations."},
    {"id": "guest_bedrooms", "name": "Guest Bedrooms Hallway", "area": "Villa Interior", "description": "A carpeted hallway leading to the various guest suites."}, # Simplified for now
    {"id": "staircase", "name": "Grand Staircase", "area": "Villa Interior", "description": "An imposing marble staircase connecting the main floors."},
    {"id": "living_room", "name": "Living Room", "area": "Villa Interior", "description": "A comfortable but formal room with sofas, armchairs, and a grand piano."},
    # Gardens
    {"id": "fountain_area", "name": "Fountain Area", "area": "Gardens", "description": "A central courtyard dominated by an ornate marble fountain."},
    {"id": "greenhouse", "name": "Greenhouse", "area": "Gardens", "description": "Filled with exotic plants and the earthy smell of damp soil. Feels humid."},
    {"id": "pool_bar", "name": "Swimming Pool & Bar", "area": "Gardens", "description": "An inviting pool area with lounge chairs and a well-stocked outdoor bar."},
    # Docks
    {"id": "yacht_deck", "name": "Patrizi's Yacht Deck", "area": "Docks", "description": "The deck of Cristiano's luxurious yacht, moored at the private pier."},
    {"id": "pier", "name": "Pier", "area": "Docks", "description": "A sturdy wooden pier extending into the lake."},
    {"id": "gazebo", "name": "Gazebo", "area": "Docks", "description": "A small, elegant gazebo near the water's edge, offering a view of the lake."},
    {"id": "boathouse", "name": "Boathouse", "area": "Docks", "description": "Contains smaller boats and equipment. Smells of lake water and oil."}
]

# Suspects (Based on Script Bios - simplified for now, will add more detail later)
SUSPECTS_DATA = [
    {"id": "raffaella", "name": "Raffaella Patrizi", "bio": "Cristiano's elegant, younger wife, active in high society."},
    {"id": "moretti", "name": "Dr. Elisa Moretti", "bio": "The sharp, young family physician."},
    {"id": "marco", "name": "Marco Santini", "bio": "The handsome young boatman, new to the staff."},
    {"id": "giovanna", "name": "Giovanna Russo", "bio": "The celebrated Tuscan chef, proud and fiery."},
    {"id": "antonello", "name": "Antonello Pisani", "bio": "The meticulous, long-serving butler."},
    {"id": "dakota", "name": "Dakota Marino", "bio": "The American wellness influencer."},
    {"id": "russell", "name": "Russell Williams", "bio": "The powerful British media mogul."},
    {"id": "rose", "name": "Rose Williams", "bio": "Russell's elegant wife, involved in charity."},
    {"id": "gabriel", "name": "Gabriel DuPont", "bio": "The charming French F1 pilot."},
    {"id": "sundeep", "name": "Sundeep Arora", "bio": "The ambitious Silicon Valley tech CEO."},
    {"id": "naomi", "name": "Naomi Lee", "bio": "Sundeep's model girlfriend."}
]

# Clues (Based on Script - using 'location_id' matching LOCATIONS above)
CLUES_DATA = [
    # Direct Clues
    {"id": "clue01", "location_id": "study", "description": "Residue of a potent, dark green herbal substance, identified as Danshen extract, found in Cristiano's nightcap glass.", "type": "Direct", "origin": "Physical Evidence", "discovered": False},
    {"id": "clue02", "location_id": "dakota_bedroom", "description": "An empty, small, dark glass vial with a minimalist silver leaf logo ('Dakota's Radiance' brand), containing Danshen extract residue, found in trash.", "type": "Direct", "origin": "Physical Evidence", "discovered": False}, # Note: Need a 'dakota_bedroom' location
    {"id": "clue03", "location_id": "greenhouse", "description": "Water-damaged notes discussing Danshen extract dosages and mentioning 'potential cardiac sensitivity'.", "type": "Direct", "origin": "Physical Evidence", "discovered": False},
    # Circumstantial Clues
    {"id": "clue04", "location_id": "dining_room", "description": "Testimony: Dakota argued heatedly with Dr. Moretti over Cristiano's health during dinner.", "type": "Circumstantial", "origin": "Testimony", "discovered": False},
    {"id": "clue05", "location_id": "living_room", "description": "Testimony: Cristiano argued sharply with Raffaella about Gabriel during Naomi's performance.", "type": "Circumstantial", "origin": "Testimony", "discovered": False},
    {"id": "clue06", "location_id": "kitchen", "description": "Testimony: Giovanna was heard shouting threats about Cristiano preferring Dakota's 'weeds'.", "type": "Circumstantial", "origin": "Testimony", "discovered": False},
    {"id": "clue07", "location_id": "pool_bar", "description": "Testimony: Antonello overheard Cristiano cutting off Russell financially during Aperitivo.", "type": "Circumstantial", "origin": "Testimony", "discovered": False},
    {"id": "clue08", "location_id": "gazebo", "description": "Testimony: Cristiano rudely dismissed Sundeep near the gazebo in the afternoon.", "type": "Circumstantial", "origin": "Testimony", "discovered": False}, # Adjusted location slightly
    {"id": "clue09", "location_id": "staircase", "description": "Testimony: Marco saw Gabriel looking flustered leaving Raffaella's room vicinity.", "type": "Circumstantial", "origin": "Testimony", "discovered": False},
    {"id": "clue10", "location_id": "study", "description": "A freshly poured, untouched glass of expensive French Cognac sits beside the overturned nightcap glass. The bottle is open but nearly full.", "type": "Circumstantial", "origin": "Physical Evidence", "discovered": False},
    {"id": "clue11", "location_id": "raffaella_bedroom", "description": "A hidden jeweler's box containing expensive F1-themed cufflinks (Gabriel's style).", "type": "Circumstantial", "origin": "Physical Evidence", "discovered": False}, # Note: Need a 'raffaella_bedroom' location
    {"id": "clue12", "location_id": "russell_bedroom", "description": "Crumpled bank statements under mattress show large overdrafts and defaulted payments to offshore entities.", "type": "Circumstantial", "origin": "Physical Evidence", "discovered": False}, # Note: Need a 'russell_bedroom' location
    {"id": "clue13", "location_id": "moretti_bedroom", "description": "Dr. Moretti's notebook details Cristiano's recent symptoms (arrythmia, dizziness) and questions unknown supplements.", "type": "Circumstantial", "origin": "Physical Evidence", "discovered": False}, # Note: Need a 'moretti_bedroom' location
    {"id": "clue14", "location_id": "study", "description": "Printed email on desk: Cristiano firmly rejecting Antonello's son's business proposal.", "type": "Circumstantial", "origin": "Physical Evidence", "discovered": False},
    {"id": "clue15", "location_id": "pool_bar", "description": "Testimony: Witness saw Marco and Gabriel argue heatedly near pool bar, then both head towards docks separately.", "type": "Circumstantial", "origin": "Testimony", "discovered": False},
    {"id": "clue16", "location_id": "yacht_deck", "description": "A slightly scratched 'Dupont Racing' engraved lighter found wedged in yacht deck seating.", "type": "Circumstantial", "origin": "Physical Evidence", "discovered": False},
    {"id": "clue17", "location_id": "living_room", "description": "Testimony: Raffaella made dismissive comments about Naomi's 'American' pop singing vs. opera.", "type": "Circumstantial", "origin": "Testimony", "discovered": False},
    # Red Herring Clues
    {"id": "clue18", "location_id": "study", "description": "A single strand of long, glossy dark hair (matching Naomi's) caught on the victim's chair armrest.", "type": "Red Herring", "origin": "Physical Evidence", "discovered": False},
    {"id": "clue19", "location_id": "library", "description": "Torn piece of stationery in trash: '...must end this dangerous liaison before he discovers everything...'", "type": "Red Herring", "origin": "Physical Evidence", "discovered": False},
    {"id": "clue20", "location_id": "kitchen", "description": "Container of potent Calabrian chili flakes left open near spice rack, away from main cooking area.", "type": "Red Herring", "origin": "Physical Evidence", "discovered": False},
    # Exonerating Clues (Represented as Testimony/Facts the player discovers)
    # Note: Exonerating clues often come from verifying alibis via testimony or logs,
    # so they might be revealed during dialogue rather than found physically.
    # We'll handle revealing these later, but list them here for reference.
    {"id": "clue21", "location_id": "security_office", "description": "Fact: Security logs & testimony confirm Russell/Rose were in their suite 11 PM - 4 AM.", "type": "Exonerating", "origin": "Testimony/Log", "discovered": False},
    {"id": "clue22", "location_id": "sundeep_bedroom", "description": "Fact: Testimony (Naomi, Dr. Moretti hearing shouts) confirms Sundeep argued then passed out drunk 11:30 PM - 1 AM+.", "type": "Exonerating", "origin": "Testimony", "discovered": False},
    {"id": "clue23", "location_id": "gabriel_bedroom", "description": "Fact: Phone logs/testimony confirm Gabriel was on a video call to California 1:05 AM - 3:38 AM.", "type": "Exonerating", "origin": "Testimony/Log", "discovered": False},
    {"id": "clue24", "location_id": "staff_quarters", "description": "Fact: Testimony/Receipt confirms Giovanna left the villa grounds ~10:30 PM, returned next morning.", "type": "Exonerating", "origin": "Testimony/Receipt", "discovered": False},
    # Environmental Clues
    {"id": "clue25", "location_id": "study", "description": "The heavy crystal nightcap tumbler lies overturned on the Persian rug near the chair.", "type": "Environmental", "origin": "Physical Evidence", "discovered": False},
    {"id": "clue26", "location_id": "study", "description": "The room feels uncomfortably warm; the A/C thermostat is switched off.", "type": "Environmental", "origin": "Physical Evidence", "discovered": False},
    {"id": "clue27", "location_id": "study", "description": "A French window is slightly ajar, letting in the scent of night-blooming jasmine.", "type": "Environmental", "origin": "Physical Evidence", "discovered": False},
    {"id": "clue28", "location_id": "gardens_path", "description": "The flagstone path towards the Greenhouse is damp from a recent night shower.", "type": "Environmental", "origin": "Physical Evidence", "discovered": False}, # Needs location 'gardens_path'
    {"id": "clue29", "location_id": "dining_room", "description": "Faint aroma of cigars/perfume lingers. Table formally set under cleanup cloths.", "type": "Environmental", "origin": "Physical Evidence", "discovered": False},
    {"id": "clue30", "location_id": "living_room", "description": "Sheet music for pop/jazz standards scattered on piano; empty cocktail glass nearby.", "type": "Environmental", "origin": "Physical Evidence", "discovered": False}
]

# --- End of Phase 1 Static Data ---

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


# --- Game Initialization ---
# --- Game Initialization ---
def init_game():
    # Load static data into game_state
    # Create deep copies to avoid modifying the original data during gameplay
    game_state["ground_truth"] = dict(GROUND_TRUTH)
    game_state["rooms"] = [dict(loc) for loc in LOCATIONS] # Using new LOCATIONS list
    game_state["suspects"] = [dict(sus) for sus in SUSPECTS_DATA] # Using new SUSPECTS_DATA
    game_state["clues"] = [dict(clue) for clue in CLUES_DATA] # Using new CLUES_DATA

    # Initialize player state
    game_state["player_notes"] = [] # Changed from "notes" for clarity
    game_state["visited_rooms"] = [] # Changed from "visited"
    game_state["accused"] = False
    game_state["current_location_id"] = None # Player starts nowhere initially
    game_state["menu_state"] = "main" # Or maybe "intro" first?
    game_state["initialized"] = True

    # Show the intro text
    show_intro()
    # Show the main menu to start
    show_main_menu()

# --- Menu Displays ---
def show_intro():
    print_output(GAME_INTRODUCTION) # Display the intro text we defined
    # Optional: Add a small prompt like "Press Enter to continue..." if needed.

def show_main_menu():
    print_output("\nMain Menu:")
    print_output("1. Visit a room")
    print_output("2. View your notes")
    print_output("3. Make an accusation")
    print_output("4. Talk to a suspect")
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

# --- Talk to Suspects ---
def show_suspect_menu():
    print_output("\nWho would you like to talk to?")
    for idx, s in enumerate(game_state["suspects"], 1):
        print_output(f"{idx}. {s['name']}")
    print_output("Enter the number of the suspect:")

def talk_to_suspect(suspect):
    print_output(f"You approach {suspect['name']}.")
    print_output(f"{suspect['name']}: \"{suspect['dialogue_intro']}\"")
    game_state["notes"].append(f"Talked to {suspect['name']}: {suspect['dialogue_intro']}")
    game_state["menu_state"] = "main"
    show_main_menu()

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
        elif cmd == "4":
            game_state["menu_state"] = "talk"
            show_suspect_menu()
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

    elif game_state["menu_state"] == "talk":
        if cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < len(game_state["suspects"]):
                talk_to_suspect(game_state["suspects"][idx])
            else:
                print_output("Invalid suspect.")
                show_suspect_menu()
        else:
            print_output("Please enter the number of the suspect.")
            show_suspect_menu()

# --- Input Bindings ---
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

# --- Start Game ---
def start_game():
    try:
        document.getElementById('submit').addEventListener('click', create_proxy(on_submit))
        document.getElementById('command').addEventListener('keypress', create_proxy(on_enter))
        init_game()
    except Exception as e:
        print_output(f"❌ Startup error: {e}")

start_game()