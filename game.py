from js import document
import random
from collections import defaultdict
from pyodide.ffi import create_proxy

from dialogue_data import DIALOGUE_TREES

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
* Cristiano Patrizi (Victim): Self‑made industrialist celebrating his 50th birthday at the villa.
* Raffaella Patrizi (Cristiano's wife): Cristiano's elegant, younger wife, active in high society, passionate of the arts but perhaps feeling trapped.
* Dr. Elisa Moretti (Personal Physician): Young and prominent Doctor from Milan, Dr. Moretti is also Patrizi's family doctor, and Cristiano’s longtime doctor, entrusted with his health. 
* Marco Santini (Boater): Young and handsome, Marco is a new addition to the staff and is in charge of the boating needs of the Patrizi's family. Takes care of their yacht and always hangs around the docks.
* Giovanna Russo (Chef): A celebrated Tuscan cook, famous for her extravagant way of presenting her food in the national food network. Was hired by Cristiano Patrizi to craft a lavish menu for tonight’s party.
* Antonello Pisani (Butler): Has been taking care of the Villa for decades, is very precise and knows the villa and the family like the palm of his hand
* Dakota Marino (American Wellness Influencer): A rich and famous wellness influencer that prescribes very out of the ordinary methods, is against traditional medicine and has an extreme diet and very specific early morning habits.
* Russell Williams (British media mogul and Cristian's friend): Famous businessman from London, controls one of the biggest media empires in the world, although rumors are that traditional media is not as profitable as it once was.
* Rose Williams (Russell's wife): Wife of Russell, manages the Williams foundation and is very active in charity work. She is classically posh and clearly comes from a British noble family. 
* Gabriel DuPont (French F1 pilot): Close friends with Cristiano, they spend a long weekend every year in Montecarlo, partying together after the F1 race.
* Sundeep Arora (CEO and tech bro): Rich engineer from Silicon Valley, with a humble background but reached success after launching a social media app to make short disappearing videos, very popular with the young audience.
* Naomi Lee (model, Sundeep's girlfriend): American model, she’s Sundeep +1 and seems to have met everyone else here for the first time. It’s her first time in Italy and is very excited about the scenery. 


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
# Example for Raffaella (add similarly to all others):
# {"id": "raffaella", "name": "Raffaella Patrizi", "bio": "...", 'dialogue_start_node': 'START'},
# ... do this for all suspects in the SUSPECTS_DATA list ...

# --- Updated SUSPECTS_DATA Example (showing first few with the new key) ---
SUSPECTS_DATA = [
    {"id": "raffaella", "name": "Raffaella Patrizi", "bio": "Cristiano's elegant, younger wife, active in high society.", 'dialogue_start_node': 'START'},
    {"id": "moretti", "name": "Dr. Elisa Moretti", "bio": "The sharp, young family physician.", 'dialogue_start_node': 'START'},
    {"id": "marco", "name": "Marco Santini", "bio": "The handsome young boatman, new to the staff.", 'dialogue_start_node': 'START'},
    {"id": "giovanna", "name": "Giovanna Russo", "bio": "The celebrated Tuscan chef, proud and fiery.", 'dialogue_start_node': 'START'},
    {"id": "antonello", "name": "Antonello Pisani", "bio": "The meticulous, long-serving butler.", 'dialogue_start_node': 'START'},
    {"id": "dakota", "name": "Dakota Marino", "bio": "The American wellness influencer.", 'dialogue_start_node': 'START'},
    {"id": "russell", "name": "Russell Williams", "bio": "The powerful British media mogul.", 'dialogue_start_node': 'START'},
    {"id": "rose", "name": "Rose Williams", "bio": "Russell's elegant wife, involved in charity.", 'dialogue_start_node': 'START'},
    {"id": "gabriel", "name": "Gabriel DuPont", "bio": "The charming French F1 pilot.", 'dialogue_start_node': 'START'},
    {"id": "sundeep", "name": "Sundeep Arora", "bio": "The ambitious Silicon Valley tech CEO.", 'dialogue_start_node': 'START'},
    {"id": "naomi", "name": "Naomi Lee", "bio": "Sundeep's model girlfriend.", 'dialogue_start_node': 'START'}
]
# --- End of Updated SUSPECTS_DATA ---

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
    # Core game data holders (populated by init_game)
    "ground_truth": {},
    "rooms": [],
    "suspects": [],
    "clues": [], # Holds ALL clues (static data), discovered status changes here

    # --- Notebook Data ---
    "notebook_discovered_clue_ids": [], # List of IDs of clues player has found
    "notebook_suspect_info": {}, # Dict: {suspect_id: {"bio": "...", "alibi_statement": None, "notes": []}, ...}
    "notebook_timeline_entries": [], # List of strings representing timeline events discovered
    # --- End of Notebook Data ---

    # Player state / Location tracking
    "current_location_id": None,
    "visited_rooms": [], # Tracks first visits for clue discovery

    # State management
    "initialized": False,
    "menu_state": "main", # Current game menu/mode
    "in_dialogue_with": None, # ID of suspect in dialogue
    "current_dialogue_node_id": None, # Current node in dialogue tree

    # Accusation state
    "accused": False,
    "in_accusation": False, # (This key was in the original, kept for potential use)

    # Basic Time Tracking (Placeholder)
    "current_game_time": None,
}
# --- End Game State Definition ---

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
    print_output("\n--- Your Detective Notes ---")
    if not game_state["player_notes"]:
        print_output("You haven't recorded any notes yet.")
    else:
        # Just print each note string as recorded
        for idx, note in enumerate(game_state["player_notes"]):
            print_output(f"{idx + 1}. {note}")
    print_output("--------------------------")

    # Stay in 'main' menu state after viewing notes
    game_state["menu_state"] = "main"
    show_main_menu()

def visit_room(room):
    # room is a dictionary like {"id": "study", "name": "Cristiano's Study", ...}
    room_id = room['id']
    room_name = room['name']
    game_state["current_location_id"] = room_id # Track current location

    print_output(f"\n--- Entering {room_name} ---")
    print_output(room.get('description', 'It looks like a room.')) # Show room description

    # Check if room has been visited before for clue discovery
    first_visit = room_id not in game_state["visited_rooms"]
    if first_visit:
        game_state["visited_rooms"].append(room_id)
        print_output("You look around carefully...")

        clues_found_in_room = []
        # Iterate through the *copy* of the list to avoid issues while modifying
        for clue in game_state["clues"]:
            # Find undiscovered clues matching this room's ID
            # Also ensure the clue is meant to be found physically (not Testimony/Fact)
            is_physical_clue = clue['origin'] in ["Physical Evidence", "Physical", "Environmental"] # Check origin type
            if clue['location_id'] == room_id and not clue['discovered'] and is_physical_clue:
                print_output(f"\n🔎 Clue Found!")
                print_output(f"   {clue['description']}")
                clue['discovered'] = True # Mark clue as discovered IN THE GAME STATE
                clues_found_in_room.append(clue)

                # Add formatted clue to player notes
                note_text = f"Clue ({clue['origin']}) in {room_name}: {clue['description']}"
                game_state["player_notes"].append(note_text)

        if not clues_found_in_room:
            print_output("You don't find any obvious clues right now.")

    else: # Room already visited
        print_output(f"You return to the {room_name}. You've already searched here thoroughly.")

    # Always show the main menu after visiting a room
    game_state["menu_state"] = "main"
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

def display_dialogue_node():
    suspect_id = game_state["in_dialogue_with"]
    node_id = game_state["current_dialogue_node_id"]
    suspect_name = ""

    # Find the suspect's name (optional but good for display)
    for s in game_state["suspects"]:
        if s['id'] == suspect_id:
            suspect_name = s['name']
            break

    # Try to get the dialogue node data
    try:
        node_data = DIALOGUE_TREES[suspect_id][node_id]

        # --- Add this block to process actions ---
        action_to_process = node_data.get('action') # Get action string if it exists
        if action_to_process:
            process_dialogue_action(action_to_process, game_state)
        # --- End of action processing block ---

        npc_text = node_data['text']
        options = node_data.get('options', [])

        # Display NPC text
        print_output(f"\n{suspect_name}: \"{npc_text}\"")

        # Display Player Options
        if options:
            print_output("\nYour response:")
            for idx, option in enumerate(options):
                print_output(f"{idx + 1}. {option['text']}")
            print_output("Enter the number of your choice:")
        else:
            # If no options, maybe automatically end? Or needs an explicit END node.
            # For now, assume an END node should always have options leading out.
            print_output("The conversation seems to be over.")
            # End dialogue automatically if no options? Risky, let's rely on END node.
            # end_dialogue() # We might need an end_dialogue helper function later

    except KeyError:
        print_output(f"\n[Error: Dialogue node '{node_id}' not found for {suspect_name}. Ending conversation.]")
        end_dialogue() # End dialogue if node is broken

def end_dialogue():
    """Resets dialogue state and returns to main menu."""
    print_output("--- Leaving Conversation ---")
    game_state["in_dialogue_with"] = None
    game_state["current_dialogue_node_id"] = None
    game_state["menu_state"] = "main"
    show_main_menu()

# --- Action Processing ---

# --- Action Processing ---

def process_dialogue_action(action_string, current_game_state): # Added current_game_state argument
    """Parses and executes actions defined in dialogue nodes."""
    # Removed 'global game_state' line
    if not action_string:
        return # No action defined

    print(f"[DEBUG] Processing action: {action_string}") # Optional debug print

    if action_string.startswith("discover_clue"):
        try:
            clue_id_to_discover = action_string.split("discover_")[1] # Get the part after "discover_"

            # Check if clue exists in master list (optional safety check)
            # NOTE: Assumes CLUES_DATA is accessible globally or passed if needed
            clue_exists = any(clue['id'] == clue_id_to_discover for clue in CLUES_DATA)
            if not clue_exists:
                print(f"[DEBUG] Action Error: Clue ID '{clue_id_to_discover}' not found in CLUES_DATA.")
                return

            # Check if clue is already discovered using the passed dictionary
            if clue_id_to_discover not in current_game_state["notebook_discovered_clue_ids"]:
                current_game_state["notebook_discovered_clue_ids"].append(clue_id_to_discover)
                print_output("   [Notebook Updated]")
            # else:
                # print(f"[DEBUG] Clue '{clue_id_to_discover}' was already discovered.")

        except IndexError:
            print(f"[DEBUG] Action Error: Invalid format for discover_clue action: {action_string}")
        except Exception as e:
             # Use current_game_state here too if needed for more complex error handling
             print(f"[DEBUG] Error processing action '{action_string}': {e}")

    # --- Add more action types later? ---
    # Example using current_game_state:
    # elif action_string == "update_alibi":
    #     suspect_id = current_game_state["in_dialogue_with"]
    #     node_id = current_game_state["current_dialogue_node_id"]
    #     npc_text = DIALOGUE_TREES[suspect_id][node_id]['text']
    #     current_game_state['notebook_suspect_info'][suspect_id]['alibi_statement'] = npc_text
    #     print_output("   [Notebook Updated - Alibi Noted]")

def talk_to_suspect(suspect):
    # suspect is a dictionary like {"id": "raffaella", "name": "Raffaella Patrizi", ...}
    suspect_id = suspect['id']
    suspect_name = suspect['name']

    print_output(f"\n--- Approaching {suspect_name} ---")

    # Set dialogue state
    game_state["in_dialogue_with"] = suspect_id
    game_state["current_dialogue_node_id"] = suspect.get('dialogue_start_node', 'START') # Get start node from suspect data
    game_state["menu_state"] = "dialogue" # Change game state to dialogue mode

    # Display the first node
    display_dialogue_node()

# --- Input Handling ---
def handle_input(cmd):
    if not game_state["initialized"]:
        # init_game() # Should already be initialized by start_game()
        print_output("Error: Game not initialized.")
        return

    current_state = game_state["menu_state"]

    if current_state == "main":
        # ... (keep existing logic for main menu: 1, 2, 3, 4)
        if cmd == "1":
            game_state["menu_state"] = "room"
            show_room_menu()
        elif cmd == "2":
            # No state change needed for view_notes, it returns to main menu itself
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

    elif current_state == "room":
        # ... (keep existing logic for room selection)
        if cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < len(game_state["rooms"]):
                visit_room(game_state["rooms"][idx]) # visit_room now handles returning to main menu
            else:
                print_output("Invalid room selection.")
                show_room_menu() # Show menu again
        else:
            print_output("Invalid room input. Please enter a number.")
            show_room_menu() # Show menu again


    elif current_state == "accuse":
        # ... (keep existing logic for accusation)
        process_accusation(cmd) # process_accusation handles game end or returning to menu

    elif current_state == "talk":
        # ... (keep existing logic for suspect selection)
         if cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < len(game_state["suspects"]):
                talk_to_suspect(game_state["suspects"][idx]) # talk_to_suspect now changes state to 'dialogue'
            else:
                print_output("Invalid suspect.")
                show_suspect_menu() # Show menu again
         else:
            print_output("Please enter the number of the suspect.")
            show_suspect_menu() # Show menu again

    # --- Add this new block to handle dialogue input ---
    elif current_state == "dialogue":
        suspect_id = game_state["in_dialogue_with"]
        node_id = game_state["current_dialogue_node_id"]

        if suspect_id is None or node_id is None:
            print_output("[Error: Unexpectedly not in dialogue. Returning to main menu.]")
            end_dialogue()
            return

        try:
            node_data = DIALOGUE_TREES[suspect_id][node_id]
            options = node_data.get('options', [])

            if cmd.isdigit():
                choice_idx = int(cmd) - 1
                if 0 <= choice_idx < len(options):
                    chosen_option = options[choice_idx]
                    next_node_id = chosen_option['next_node']

                    if next_node_id == 'END':
                        end_dialogue()
                    else:
                        # Move to the next node
                        game_state["current_dialogue_node_id"] = next_node_id
                        # Optional: Execute action if defined for the new node
                        # new_node_data = DIALOGUE_TREES[suspect_id].get(next_node_id, {})
                        # action = new_node_data.get('action')
                        # if action:
                        #     action() # Call the action function
                        display_dialogue_node() # Display the new node
                else:
                    print_output("Invalid option number. Please try again.")
                    # Re-display the current node's options
                    display_dialogue_node()
            else:
                print_output("Please enter the number corresponding to your choice.")
                # Re-display the current node's options
                display_dialogue_node()

        except KeyError:
            print_output(f"[Error: Dialogue node '{node_id}' configuration issue for {suspect_id}. Ending conversation.]")
            end_dialogue()
    # --- End of new dialogue block ---

    else:
        print_output(f"Error: Unknown menu state '{current_state}'")
        # Reset to main menu as a fallback
        game_state["menu_state"] = "main"
        show_main_menu()

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