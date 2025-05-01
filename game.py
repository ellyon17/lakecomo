# -*- coding: utf-8 -*-
from js import document, console
import random
from collections import defaultdict
from pyodide.ffi import create_proxy
import json # Added for potential future use with loading/saving complex data

# --- Configuration ---
DEBUG = True  # Set to False to disable debug print statements

# --- Phase 1 Static Data ---

# Ground Truth for the Murder (Example - can be randomized or loaded)
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

The morning air is crisp as your car pulls up to the gates of the stunning Villa Patrizi on the shores of Lake Como. It's 6:00 AM on April 15th. You are Detective [Player Name], one of Milan's most renowned investigators, known for untangling the most complex cases.

An urgent call summoned you here. The villa's owner, Cristiano Patrizi, a powerful and self-made industrialist, was found dead in his private study just hours ago, around 4:00 AM, by the distraught butler, Antonello Pisani.

Yesterday, April 14th, was Cristiano's 50th birthday, and the villa hosted a lavish celebration. What began as a grand affair simmered down to an intimate gathering of close friends, family, and associates staying at the villa.

Now, the laughter has died, replaced by suspicion and fear. The serene beauty of Lake Como hides a dark secret. Everyone who remained at the villa is now confined to the grounds. They are all suspects, and no one leaves until you uncover the truth.
"""

# --- Suspects (Phase 1 - Basic Info) ---
# Detailed bios, motives, alibis, and dialogue trees would expand this.
SUSPECTS = {
    "Antonello Pisani": {"role": "Butler", "description": "Loyal, anxious, discovered the body."},
    "Bianca Rossi": {"role": "Business Rival", "description": "Sharp, competitive, had recent disputes with Cristiano."},
    "Dr. Elara Moretti": {"role": "Personal Physician", "description": "Calm, professional, concerned about Cristiano's health."},
    "Leo Gallo": {"role": "Estranged Nephew", "description": "Artistic, resentful, recently cut off financially."},
    "Sofia Bianchi": {"role": "Younger Fiancée", "description": "Charming, possibly hiding secrets, stands to inherit."},
    "Dakota Marino": {"role": "Personal Chef", "description": "Passionate, knowledgeable about herbs and remedies, recently argued with Cristiano."},
}

# --- Locations (Phase 1 - Basic Descriptions) ---
LOCATIONS = {
    "Foyer": "The grand entrance hall of the villa. Doors lead to the Living Room, Dining Room, and stairs go up.",
    "Living Room": "Luxurious, with plush seating, a grand piano, and large windows overlooking the lake.",
    "Dining Room": "Elegant, with a long table still showing remnants of last night's dinner.",
    "Kitchen": "Modern and spacious, the domain of the chef.",
    "Study": "Cristiano's private office, the scene of the crime. Currently sealed.",
    "Library": "A quiet room filled with books, comfortable chairs.",
    "Guest Wing Hallway": "Leads to the guest bedrooms.",
    "Bianca's Room": "Guest room.",
    "Leo's Room": "Guest room.",
    "Sofia's Room": "Guest room (connected to Master Suite).",
    "Master Suite": "Cristiano and Sofia's bedroom.",
    "Staff Quarters Hallway": "Leads to staff rooms.",
    "Antonello's Room": "Staff room.",
    "Dakota's Room": "Staff room.",
    "Dr. Moretti's Room": "Guest room (in main wing).",
    "Terrace": "Overlooks the lake, access from Living Room and Dining Room.",
    "Greenhouse": "Accessed via the Terrace, contains various plants.",
    "Gardens": "Extensive grounds surrounding the villa."
}

# --- Clues (Phase 1 - Example Set) ---
# Format: {location: {clue_id: {"description": "...", "found": False, "details": "...", "type": "Object/Observation/Document"}}}
CLUES = {
    "Study": {
        "clue_body": {"description": "Cristiano Patrizi's body.", "found": False, "details": "Lying near his desk. Initial observation suggests no obvious signs of struggle.", "type": "Observation"},
        "clue_glass": {"description": "An overturned glass near the desk.", "found": False, "details": "Seems to have held a dark liquid, possibly whiskey. Smells faintly bitter.", "type": "Object"},
        "clue_letter": {"description": "A crumpled letter on the desk.", "found": False, "details": "It's a threatening business letter from Bianca Rossi's company.", "type": "Document"}
    },
    "Living Room": {
        "clue_music": {"description": "Sheet music on the piano.", "found": False, "details": "Jazz standards and some modern pop songs.", "type": "Object"},
         "clue_lipstick_glass": {"description": "An empty cocktail glass with lipstick traces.", "found": False, "details": "Left on the piano. The lipstick is a vibrant red shade.", "type": "Object"}
    },
     "Greenhouse": {
        "clue_herbs": {"description": "Various herbs, some medicinal.", "found": False, "details": "Includes a prominent section of Danshen (Salvia miltiorrhiza), known for cardiovascular effects.", "type": "Observation"}
    },
    "Dakota's Room": {
        "clue_herb_book": {"description": "A book on medicinal herbs.", "found": False, "details": "Open to a page detailing interactions between Danshen and heart medications.", "type": "Document"}
    },
     "Dr. Moretti's Room": {
        "clue_medical_bag": {"description": "Dr. Moretti's medical bag.", "found": False, "details": "Contains standard medical supplies, including syringes and vials. Also contains prescription notes for Cristiano's heart condition.", "type": "Object"}
    }
    # Add more clues for other locations
}

# --- Dialogue Trees (Simplified Example - requires dialogue_data.py) ---
# Moved to dialogue_data.py for better organization
try:
    from dialogue_data import DIALOGUE_TREES
    if DEBUG: print("Successfully imported DIALOGUE_TREES")
except ImportError:
    if DEBUG: print("Warning: dialogue_data.py not found. Using placeholder dialogue.")
    DIALOGUE_TREES = { # Placeholder if file missing
        "Antonello Pisani": {
            "start": {"text": "Detective? Oh, thank goodness you're here. It's terrible, just terrible.", "options": {"ask_discovery": "Tell me about finding Mr. Patrizi.", "ask_evening": "What happened last night?"}, "leads_to": {"ask_discovery": "discovery_details", "ask_evening": "evening_overview"}},
            "discovery_details": {"text": "I came in around 4 AM to prepare his morning coffee... the study door was ajar... I saw him...", "options": {}, "ends_dialogue": True},
            "evening_overview": {"text": "The party ended late. A few guests remained. Mr. Patrizi seemed... tense.", "options": {}, "ends_dialogue": True}
        },
         # Add basic trees for other suspects
         "Bianca Rossi": {
            "start": {"text": "Detective. A tragic event. Cristiano and I had our differences, but this...", "options": {"ask_business": "What were your business dealings?"}, "leads_to": {"ask_business": "business_talk"}},
            "business_talk": {"text": "We were rivals, yes, but competitive, not criminal.", "options": {}, "ends_dialogue": True}
         }
    }


# --- Game State ---
game_state = {
    "current_location": "Foyer",
    "player_name": "Investigator", # Can be set by player later
    "inventory": set(), # Stores clue_ids found by the player
    "suspect_states": {suspect: {"met": False, "dialogue_node": "start"} for suspect in SUSPECTS},
    "current_time": "April 15th, 6:00 AM", # Simple time progression
    "crime_details_known": defaultdict(lambda: None), # Stores player deductions
    "menu_state": "main", # Controls current interaction mode: main, move, look, talk, inventory, accuse, dialogue
    "talking_to": None # Which suspect is currently being interviewed
}

# --- Helper Functions ---

def print_output(message):
    """Appends message to the game's output area in the HTML."""
    output_area = document.getElementById('output')
    # Sanitize message slightly to prevent accidental HTML injection
    # In a real game, use a proper sanitization library
    sanitized_message = message.replace('<', '&lt;').replace('>', '&gt;')
    output_area.innerHTML += f"<p>{sanitized_message}</p>"
    output_area.scrollTop = output_area.scrollHeight # Auto-scroll

def clean_input(text):
    """Basic cleaning for user input."""
    return text.lower().strip()

def get_available_actions():
    """Returns a list of actions available in the current state."""
    state = game_state["menu_state"]
    actions = ["help"] # Help is always available

    if state == "main":
        actions.extend(["move", "look", "talk", "inventory", "accuse", "time"])
    elif state == "move":
        actions.append("back") # Go back to main menu
        # Could also list available directions/locations here
    elif state == "look":
        actions.append("around") # Look around the current location
        actions.append("clue <clue_id>") # Examine a found clue
        actions.append("back")
    elif state == "talk":
        actions.extend(list(SUSPECTS.keys())) # List suspects to talk to
        actions.append("back")
    elif state == "inventory":
         actions.append("list") # List found clues
         actions.append("back")
    elif state == "accuse":
        actions.append("back")
        # Accusation requires specifying details, handled in handle_input
    elif state == "dialogue":
        # Actions are dialogue choices, handled dynamically
         actions.append("goodbye") # Option to end conversation

    return actions

def display_help():
    """Shows available commands based on the current state."""
    actions = get_available_actions()
    state_desc = game_state["menu_state"]
    if game_state["menu_state"] == "dialogue":
        state_desc = f"talking to {game_state['talking_to']}"

    help_text = f"--- Help (Current mode: {state_desc}) ---\n"
    help_text += "Available commands:\n"
    if game_state["menu_state"] == "main":
         help_text += "  move        - Change your location\n"
         help_text += "  look        - Examine your surroundings or clues\n"
         help_text += "  talk        - Speak with a suspect\n"
         help_text += "  inventory   - Check the clues you have found\n"
         help_text += "  accuse      - Make an accusation (when ready)\n"
         help_text += "  time        - Check the current game time\n"
         help_text += "  help        - Show this help message"
    elif game_state["menu_state"] == "move":
         help_text += "  <location_name> - Go to a specific connected location\n"
         help_text += "  list            - List accessible locations from here\n"
         help_text += "  back            - Return to the main menu"
    elif game_state["menu_state"] == "look":
         help_text += "  around          - Describe the current location and any obvious clues\n"
         help_text += "  <clue_id>       - Examine a specific clue you see (e.g., 'look clue_glass')\n"
         help_text += "  back            - Return to the main menu"
    elif game_state["menu_state"] == "talk":
         help_text += "  <suspect_name>  - Start a conversation (e.g., 'talk Antonello Pisani')\n"
         help_text += "  list            - List suspects present or available\n"
         help_text += "  back            - Return to the main menu"
    elif game_state["menu_state"] == "inventory":
        help_text += "  list            - List all clues you have collected\n"
        help_text += "  examine <clue_id> - Look at details of a collected clue\n"
        help_text += "  back            - Return to the main menu"
    elif game_state["menu_state"] == "accuse":
        help_text += "  Usage: accuse <suspect_name> with <method> for <motive>\n"
        help_text += "  Example: accuse Leo Gallo with Poison for Inheritance\n"
        help_text += "  back            - Return to the main menu"
    elif game_state["menu_state"] == "dialogue":
        help_text += "  <number>        - Choose a dialogue option by its number\n"
        help_text += "  goodbye         - End the conversation\n"
        help_text += "  help            - Show this help message (during dialogue)"
        # Dialogue options are displayed separately

    print_output(help_text)


def show_main_menu():
    """Displays the main menu options."""
    print_output("\n--- Main Menu ---")
    print_output(f"Location: {game_state['current_location']}")
    print_output(f"Time: {game_state['current_time']}")
    print_output("What would you like to do? (move, look, talk, inventory, accuse, time, help)")

def update_time(minutes=10):
     """Advances game time (very basic)."""
     # This needs a proper time system later
     current_time_str = game_state["current_time"]
     # Rudimentary time advance - replace with datetime objects for real calculation
     parts = current_time_str.split(", ")
     time_parts = parts[1].split(":")
     hour = int(time_parts[0])
     minute = int(time_parts[1].split(" ")[0])
     am_pm = time_parts[1].split(" ")[1]

     minute += minutes
     hour += minute // 60
     minute %= 60

     if hour >= 12:
         if am_pm == "AM":
             am_pm = "PM"
         elif hour > 12: # Handle 12 PM case
            hour -= 12
     if hour >= 12 and am_pm == "PM": # Rollover past midnight (shouldn't happen much in phase 1)
         hour -=12
         am_pm = "AM"
         # Advance day? Need date tracking for that.

     game_state["current_time"] = f"{parts[0]}, {hour:02d}:{minute:02d} {am_pm}"
     if DEBUG: print(f"DEBUG: Time advanced to {game_state['current_time']}")


# --- Action Handlers ---

def handle_move(command_parts):
    """Handles the 'move' command."""
    if len(command_parts) < 2 or command_parts[1] == 'list':
        # Basic connectivity - needs proper map/graph later
        # Example: List locations accessible from Foyer
        accessible = []
        if game_state["current_location"] == "Foyer":
            accessible = ["Living Room", "Dining Room", "Stairs (not implemented)"] # Stairs lead conceptually
        elif game_state["current_location"] == "Living Room":
             accessible = ["Foyer", "Terrace", "Dining Room"]
        elif game_state["current_location"] == "Dining Room":
             accessible = ["Foyer", "Terrace", "Kitchen"]
        # Add more connections for other locations
        else:
            accessible.append("Foyer (example back connection)") # Default fallback

        print_output(f"From {game_state['current_location']}, you can access:")
        for loc in accessible:
            print_output(f"- {loc}")
        print_output("Enter 'move <location_name>' to go there, or 'back'.")
        return

    destination = " ".join(command_parts[1:]).title() # Allow multi-word locations

    # Add validation: Is destination a valid location AND accessible from here?
    # For now, just check if it's a known location. Accessibility needs map data.
    if destination in LOCATIONS:
        game_state["current_location"] = destination
        game_state["menu_state"] = "main"
        update_time(5) # Moving takes time
        print_output(f"You move to the {destination}.")
        print_output(LOCATIONS[destination])
        show_main_menu()
    elif destination == "Back":
         game_state["menu_state"] = "main"
         show_main_menu()
    else:
        print_output(f"'{destination}' is not a place you recognize or can access from here.")
        # Re-show move help/options
        handle_move(["move", "list"])


def handle_look(command_parts):
    """Handles the 'look' command."""
    location = game_state["current_location"]

    if len(command_parts) < 2 or command_parts[1] == 'around':
        print_output(f"--- Looking around the {location} ---")
        print_output(LOCATIONS[location])
        # Check for visible clues in the current location
        found_any = False
        if location in CLUES:
            print_output("\nYou notice:")
            for clue_id, clue_data in CLUES[location].items():
                 # Only show clues not yet 'found' (added to inventory)
                 # Or maybe always show description, but only allow 'examine' if found? Let's show if not found.
                if clue_id not in game_state["inventory"]:
                    print_output(f"- ({clue_id}): {clue_data['description']}")
                    found_any = True
        if not found_any:
            print_output("\nNothing immediately catches your eye as a clue.")
        print_output("\nUse 'look <clue_id>' to examine something specific, or 'back'.")

    elif command_parts[1] == 'clue' and len(command_parts) > 2:
        clue_id_to_find = command_parts[2]
        if location in CLUES and clue_id_to_find in CLUES[location]:
            clue_data = CLUES[location][clue_id_to_find]
            if clue_id_to_find not in game_state["inventory"]:
                print_output(f"--- Examining {clue_id_to_find} ---")
                print_output(clue_data["details"])
                game_state["inventory"].add(clue_id_to_find)
                update_time(2) # Examining takes a moment
                print_output(f"(Added '{clue_id_to_find}' to your inventory)")
                if DEBUG: print(f"DEBUG: Inventory: {game_state['inventory']}")
            else:
                print_output(f"You have already examined {clue_id_to_find}. Check your inventory.")
        else:
             print_output(f"You don't see '{clue_id_to_find}' here to examine.")
        # Stay in 'look' mode
        print_output("Look around again, examine another clue, or type 'back'.")

    elif command_parts[1] == 'back':
        game_state["menu_state"] = "main"
        show_main_menu()
    else:
        print_output("Use 'look around' to survey the area, 'look clue <clue_id>' to examine, or 'back'.")


def handle_talk(command_parts):
    """Handles the 'talk' command."""
    if len(command_parts) < 2 or command_parts[1] == 'list':
         # Simple: list all suspects. Future: list only those present in the location.
         print_output("--- Suspects ---")
         for name, data in SUSPECTS.items():
             status = "(Met)" if game_state["suspect_states"][name]["met"] else ""
             print_output(f"- {name} ({data['role']}) {status}")
         print_output("\nEnter 'talk <suspect_name>' to start a conversation, or 'back'.")
         return

    target_suspect = " ".join(command_parts[1:]).title()

    if target_suspect == "Back":
        game_state["menu_state"] = "main"
        show_main_menu()
        return

    if target_suspect in SUSPECTS:
        # Check if suspect is 'available' (e.g., in the same location - Phase 2/3 feature)
        # For Phase 1, assume they are reachable.
        start_dialogue(target_suspect)

    else:
        print_output(f"You can't talk to '{target_suspect}'. Are they here? Did you spell the name correctly?")
        # Re-show talk list
        handle_talk(["talk", "list"])

def handle_inventory(command_parts):
    """Handles the 'inventory' command."""
    action = command_parts[1] if len(command_parts) > 1 else "list" # Default to list

    if action == "list":
        print_output("--- Inventory (Clues Found) ---")
        if not game_state["inventory"]:
            print_output("You haven't collected any specific clues yet.")
        else:
            for clue_id in sorted(list(game_state["inventory"])):
                # Find which location this clue belongs to for context (inefficient, better data structure later)
                origin_location = "Unknown Location"
                clue_desc = "Unknown Clue"
                for loc, clues_in_loc in CLUES.items():
                    if clue_id in clues_in_loc:
                        origin_location = loc
                        clue_desc = clues_in_loc[clue_id].get("description", "No description")
                        break
                print_output(f"- {clue_id}: {clue_desc} (Found in {origin_location})")
        print_output("\nUse 'inventory examine <clue_id>' for details, or 'back'.")

    elif action == "examine" and len(command_parts) > 2:
        clue_id_to_examine = command_parts[2]
        if clue_id_to_examine in game_state["inventory"]:
             # Find the clue details again
             clue_details = "Details not found (error)."
             for loc, clues_in_loc in CLUES.items():
                 if clue_id_to_examine in clues_in_loc:
                     clue_details = clues_in_loc[clue_id_to_examine].get("details", "No details available.")
                     break
             print_output(f"--- Examining {clue_id_to_examine} (from Inventory) ---")
             print_output(clue_details)
        else:
             print_output(f"You don't have the clue '{clue_id_to_examine}' in your inventory.")
        # Stay in inventory mode
        print_output("List inventory again, examine another clue, or type 'back'.")

    elif action == "back":
        game_state["menu_state"] = "main"
        show_main_menu()

    else:
         print_output("Use 'inventory list', 'inventory examine <clue_id>', or 'back'.")


def handle_accuse(command_parts):
    """Handles the 'accuse' command."""
    # Example format: accuse Leo Gallo with Poison for Inheritance
    if len(command_parts) < 6 or 'with' not in command_parts or 'for' not in command_parts:
        print_output("Invalid accusation format.")
        print_output("Use: accuse <Suspect Name> with <Method/Weapon> for <Motive>")
        print_output("Example: accuse Leo Gallo with Poison for Inheritance")
        print_output("Type 'back' to cancel accusation.")
        return

    try:
        suspect_name_parts = []
        method_parts = []
        motive_parts = []

        mode = "suspect" # Modes: suspect, method, motive
        for i, part in enumerate(command_parts[1:]):
             if part == 'with' and mode == 'suspect':
                 mode = "method"
                 continue
             elif part == 'for' and mode == 'method':
                 mode = "motive"
                 continue

             if mode == "suspect":
                 suspect_name_parts.append(part)
             elif mode == "method":
                 method_parts.append(part)
             elif mode == "motive":
                 motive_parts.append(part)

        accused_suspect = " ".join(suspect_name_parts).title()
        accused_method = " ".join(method_parts)
        accused_motive = " ".join(motive_parts)

        if not accused_suspect or not accused_method or not accused_motive:
             raise ValueError("Missing parts of accusation") # Trigger format error below

        if accused_suspect not in SUSPECTS:
            print_output(f"'{accused_suspect}' is not recognized as a suspect.")
            return

        print_output(f"\n--- Final Accusation ---")
        print_output(f"You accuse: {accused_suspect}")
        print_output(f"Method: {accused_method}")
        print_output(f"Motive: {accused_motive}")
        print_output("-" * 26)

        # --- Check against Ground Truth ---
        # Basic check for Phase 1 - needs more nuance (partial matches?) later
        correct_murderer = GROUND_TRUTH["murderer"]
        # Method/Motive matching needs to be flexible (keywords?)
        # Simple check for now:
        murderer_match = (accused_suspect == correct_murderer)
        # This is too strict, needs keyword/semantic matching later
        method_match = (accused_method.lower() in GROUND_TRUTH["method"].lower())
        motive_match = (accused_motive.lower() in GROUND_TRUTH["motive"].lower())

        if murderer_match and method_match and motive_match:
            print_output("\n*** CORRECT! ***")
            print_output("You have pieced together the truth and exposed the killer.")
            print_output(f"It was indeed {correct_murderer}, who used {GROUND_TRUTH['method']} because of {GROUND_TRUTH['motive']}.")
            # End game state or transition to epilogue
            game_state["menu_state"] = "ended"
            print_output("\n--- GAME OVER ---")
        else:
            print_output("\n*** INCORRECT ***")
            print_output("Your accusation doesn't match the facts.")
            if not murderer_match:
                print_output(f"- The murderer was not {accused_suspect}.")
            if not method_match:
                 print_output(f"- The method used was not '{accused_method}'.")
            if not motive_match:
                 print_output(f"- The motive was not '{accused_motive}'.")

            print_output("\nThe true killer remains elusive. Keep investigating.")
            # Return to main menu to allow player to continue
            game_state["menu_state"] = "main"
            show_main_menu()

    except Exception as e:
        print_output("Error processing accusation format.")
        print_output("Use: accuse <Suspect Name> with <Method/Weapon> for <Motive>")
        if DEBUG: print(f"DEBUG: Accusation parsing error: {e}")
        # Stay in accuse mode


# --- Dialogue System ---

def start_dialogue(suspect_id):
    """Initiates dialogue with a suspect."""
    if suspect_id not in DIALOGUE_TREES:
        print_output(f"You approach {suspect_id}, but they don't seem to have anything to say right now.")
        if DEBUG: print(f"DEBUG: No dialogue tree found for {suspect_id}")
        return

    game_state["menu_state"] = "dialogue"
    game_state["talking_to"] = suspect_id
    # Mark suspect as met if not already
    if not game_state["suspect_states"][suspect_id]["met"]:
        game_state["suspect_states"][suspect_id]["met"] = True
        if DEBUG: print(f"DEBUG: Marked {suspect_id} as met.")
    # Reset to start node or get current node (for resuming later)
    current_node_id = game_state["suspect_states"][suspect_id].get("dialogue_node", "start")
    if DEBUG: print(f"DEBUG: Starting dialogue with {suspect_id} at node '{current_node_id}'")

    display_dialogue_node(current_node_id)


def display_dialogue_node(node_id=None):
    """Displays the text and options for the current dialogue node."""
    suspect_id = game_state["talking_to"]
    if not suspect_id:
        if DEBUG: print("DEBUG: Error - Tried to display dialogue node with no suspect selected.")
        end_dialogue()
        return

    tree = DIALOGUE_TREES.get(suspect_id, {})
    if node_id is None:
        node_id = game_state["suspect_states"][suspect_id].get("dialogue_node", "start")

    node_data = tree.get(node_id)

    if not node_data:
        print_output(f"[Error: Dialogue node '{node_id}' not found for {suspect_id}. Ending conversation.]")
        if DEBUG: print(f"DEBUG: Missing node '{node_id}' in tree for {suspect_id}")
        end_dialogue()
        return

    # Store current node for state
    game_state["suspect_states"][suspect_id]["dialogue_node"] = node_id

    # Display node text
    print_output(f"\n--- {suspect_id} ---")
    print_output(node_data.get("text", "[Silent response...]"))

    # Display options
    options = node_data.get("options", {})
    if options:
        print_output("\nYour options:")
        i = 1
        for key, text in options.items():
            print_output(f"{i}. {text}")
            i += 1
        print_output("\nEnter the number of your choice, or 'goodbye'.")
    else:
        # If no options and not explicitly ending, assume it ends
        if not node_data.get("ends_dialogue", False):
             print_output("(The conversation seems to be at an end.)")
             # Automatically end if no options are presented
             end_dialogue(implicit=True)


def end_dialogue(implicit=False):
    """Ends the current dialogue session."""
    if not implicit: # Don't print message if implicitly ended by lack of options
        print_output(f"You end the conversation with {game_state['talking_to']}.")
    if DEBUG: print(f"DEBUG: Ending dialogue with {game_state['talking_to']}.")
    game_state["talking_to"] = None
    game_state["menu_state"] = "main"
    update_time(5) # Talking takes time
    show_main_menu()


# --- Main Input Handler ---

def handle_input(command):
    """Processes the player's command."""
    command = clean_input(command)
    command_parts = command.split()
    verb = command_parts[0] if command_parts else ""

    current_state = game_state["menu_state"]
    if DEBUG: print(f"DEBUG: Handling input '{command}' in state '{current_state}'")

    # Universal commands
    if verb == "help":
        display_help()
        return
    if verb == "time" and current_state == "main":
         print_output(f"Current game time: {game_state['current_time']}")
         return
    if verb == "quit" or verb == "exit": # Allow quitting
        print_output("Exiting game. Goodbye.")
        # In a web context, this doesn't close the tab, just stops interaction.
        # We might disable the input field or show a final message.
        document.getElementById('command').disabled = True
        document.getElementById('submit').disabled = True
        return

    # State-specific commands
    if current_state == "main":
        if verb == "move":
            game_state["menu_state"] = "move"
            handle_move(["move", "list"]) # Show available locations initially
        elif verb == "look":
            game_state["menu_state"] = "look"
            handle_look(["look", "around"]) # Look around initially
        elif verb == "talk":
            game_state["menu_state"] = "talk"
            handle_talk(["talk", "list"]) # Show suspects initially
        elif verb == "inventory":
            game_state["menu_state"] = "inventory"
            handle_inventory(["inventory", "list"]) # List inventory initially
        elif verb == "accuse":
            game_state["menu_state"] = "accuse"
            handle_accuse([]) # Show accusation help/format
        else:
            print_output("Unknown command in main menu. Type 'help' for options.")
            show_main_menu()

    elif current_state == "move":
        if verb == "back":
            game_state["menu_state"] = "main"
            show_main_menu()
        elif verb == "list":
             handle_move(["move", "list"])
        elif len(command_parts) > 0: # Assume the command IS the location
             handle_move(["move"] + command_parts) # Prepend "move" for the handler
        else:
             print_output("Enter a location name to move to, 'list' available locations, or 'back'.")


    elif current_state == "look":
        if verb == "back":
            game_state["menu_state"] = "main"
            show_main_menu()
        elif verb == "around":
            handle_look(["look", "around"])
        elif verb == "look" and len(command_parts) > 1: # Allow "look clue_id" directly
            handle_look(command_parts)
        elif len(command_parts) == 1 : # Allow just "clue_id" as shorthand for "look clue_id"
             handle_look(["look", "clue", command_parts[0]])
        else:
            print_output("Use 'look around', 'look <clue_id>', or 'back'.")


    elif current_state == "talk":
        if verb == "back":
            game_state["menu_state"] = "main"
            show_main_menu()
        elif verb == "list":
             handle_talk(["talk", "list"])
        elif len(command_parts) > 0: # Assume the command IS the suspect name
             handle_talk(["talk"] + command_parts) # Prepend "talk" for the handler
        else:
             print_output("Enter a suspect's name to talk to, 'list' suspects, or 'back'.")

    elif current_state == "inventory":
         if verb == "back":
             game_state["menu_state"] = "main"
             show_main_menu()
         elif verb == "list":
             handle_inventory(["inventory", "list"])
         elif verb == "examine" and len(command_parts) > 1:
              handle_inventory(command_parts)
         elif len(command_parts) == 1: # Allow shorthand "clue_id" for examine
              handle_inventory(["inventory", "examine", command_parts[0]])
         else:
             print_output("Use 'inventory list', 'inventory examine <clue_id>', or 'back'.")


    elif current_state == "accuse":
        if verb == "back":
            game_state["menu_state"] = "main"
            show_main_menu()
        elif verb == "accuse":
            handle_accuse(command_parts)
        else:
            print_output("Invalid command during accusation. Use 'accuse ...' or 'back'.")

    # --- New Dialogue Block ---
    elif current_state == "dialogue":
        suspect_id = game_state["talking_to"]
        current_node_id = game_state["suspect_states"][suspect_id]["dialogue_node"]
        tree = DIALOGUE_TREES.get(suspect_id, {})
        node_data = tree.get(current_node_id, {})
        options = node_data.get("options", {})
        leads_to = node_data.get("leads_to", {})

        if verb == "goodbye":
            end_dialogue()
            return

        try:
            # Try to parse the command as a choice number
            choice_num = int(command)
            if 1 <= choice_num <= len(options):
                # Valid choice number
                option_key = list(options.keys())[choice_num - 1] # Get the internal key for the choice
                next_node_id = leads_to.get(option_key)

                if next_node_id:
                    if DEBUG: print(f"DEBUG: Dialogue transition: {current_node_id} -> {next_node_id} via choice {choice_num} ('{option_key}')")
                    display_dialogue_node(next_node_id)
                else:
                    # If the chosen option key doesn't lead anywhere defined
                    print_output("[This line of questioning seems to end here.]")
                    if DEBUG: print(f"DEBUG: Dialogue option '{option_key}' has no 'leads_to' target from node '{current_node_id}'.")
                    # Decide if this implicitly ends the dialogue or just returns to the node options
                    # Let's end it for simplicity now.
                    end_dialogue(implicit=True) # End implicitly as there's nowhere to go

            else:
                print_output(f"Invalid choice number. Please enter a number between 1 and {len(options)}, or 'goodbye'.")
                # Re-display the current node's options without re-printing the text
                # (We need a slight refactor to separate text printing from option printing if we want this perfect)
                display_dialogue_node() # Re-displaying whole node is okay for now

        except ValueError:
            # Input was not a number
            print_output("Please enter the number corresponding to your choice, or 'goodbye'.")
            # Re-display the current node's options
            display_dialogue_node() # Re-display whole node

        except KeyError:
            print_output(f"[Error: Dialogue node '{node_id}' configuration issue for {suspect_id}. Ending conversation.]")
            if DEBUG: print(f"DEBUG: KeyError during dialogue processing for node '{current_node_id}', suspect '{suspect_id}'. Check DIALOGUE_TREES.")
            end_dialogue()
    # --- End of new dialogue block ---

    else:
        print_output(f"Error: Unknown menu state '{current_state}'")
        if DEBUG: print(f"DEBUG: Reached unknown menu state: {current_state}")
        # Reset to main menu as a fallback
        game_state["menu_state"] = "main"
        show_main_menu()

# --- Input Bindings (for HTML/Pyodide) ---
def on_submit(e):
    """Callback for when the submit button is clicked."""
    try:
        cmd = document.getElementById('command').value.strip()
        document.getElementById('command').value = '' # Clear input field
        if not cmd:
            return # Ignore empty commands
        print_output(f"\n> {cmd}") # Echo command to output
        handle_input(cmd)
    except Exception as err:
        print_output(f"An error occurred processing your command: {err}")
        if DEBUG: console.error(f"Python Error: {err}") # Log detailed error to browser console

def on_enter(e):
    """Callback for when Enter key is pressed in the input field."""
    if e.key == "Enter":
        on_submit(e) # Trigger the same action as clicking submit

# --- Start Game ---
def start_game():
    """Initializes and starts the game."""
    try:
        # Setup input listeners
        submit_button = document.getElementById('submit')
        command_input = document.getElementById('command')

        # Use create_proxy to wrap Python functions for JS event listeners
        submit_proxy = create_proxy(on_submit)
        enter_proxy = create_proxy(on_enter)

        submit_button.addEventListener('click', submit_proxy)
        command_input.addEventListener('keypress', enter_proxy)

        # Print introduction and initial state
        print_output(GAME_INTRODUCTION)
        # Potentially ask for player name here
        show_main_menu()

        # Initial focus on command input
        command_input.focus()
        if DEBUG: print("DEBUG: Game started, input listeners attached.")

    except Exception as e:
        print_output(f"Fatal Error during game initialization: {e}")
        if DEBUG: console.error(f"Initialization Error: {e}")


# --- Main execution block (when script is loaded in Pyodide) ---
# We don't call start_game() directly here.
# It should be called from the HTML file after Pyodide is ready.
# Example: In HTML, after pyodide loads: pyodide.runPython(game_code); pyodide.globals.get('start_game')()
if DEBUG: print("DEBUG: game.py loaded.")