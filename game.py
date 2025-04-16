        from js import document
        import random

        # ===== Game State & Data (Phase 1 mechanics) =====
        rooms = ["Villa Interior", "Gardens", "Docks"]
        suspects = ["Doctor", "Butler", "Chef", "Artist"]
        causes_of_death = ["Poisoning", "Stabbing", "Blunt Force"]
        motives = ["Inheritance", "Revenge", "Love Triangle", "Cover-up"]

        game_state = {
            "murderer": None,
            "cause": None,
            "motive": None,
            "clues_placed": {},
            "visited_rooms": [],
            "in_accusation": False
        }

        def print_output(text):
            out = document.getElementById('output')
            out.innerHTML += text + "<br/>"
            out.scrollTop = out.scrollHeight

        def init_game():
            # Randomize scenario
            game_state["murderer"] = random.choice(suspects)
            game_state["cause"] = random.choice(causes_of_death)
            game_state["motive"] = random.choice(motives)
            # Place clues
            for room in rooms:
                clue_text = f"Clue in {room}: motive hints at '{random.choice(motives)}'."
                game_state["clues_placed"][room] = clue_text
            print_output("Welcome to the Lake Como Murder Mystery!")
            print_output("A murder occurred last night. Investigate to uncover the culprit.")
            show_menu()

        def show_menu():
            print_output("\nWhere would you like to go?")
            for idx, room in enumerate(rooms, 1):
                print_output(f"{idx}. {room}")
            print_output(f"{len(rooms)+1}. Make an accusation")

        def process_input(cmd):
            try:
                choice = int(cmd)
            except:
                print_output("Please enter a number.")
                return
            if 1 <= choice <= len(rooms):
                visit_room(rooms[choice-1])
            elif choice == len(rooms) + 1:
                game_state["in_accusation"] = True
                make_accusation()
            else:
                print_output("Invalid choice, try again.")

        def visit_room(room):
            if room in game_state["visited_rooms"]:
                print_output(f"You return to the {room}.")
            else:
                print_output(f"You enter the {room}.")
                game_state["visited_rooms"].append(room)
                print_output(game_state["clues_placed"][room])
            show_menu()

        def make_accusation():
            print_output("\nWho is the murderer?")
            for idx, suspect in enumerate(suspects, 1):
                print_output(f"{idx}. {suspect}")

        def process_accusation(cmd):
            try:
                choice = int(cmd)
            except:
                print_output("Please enter a number.")
                return
            if 1 <= choice <= len(suspects):
                accused = suspects[choice-1]
                if accused == game_state["murderer"]:
                    print_output(f"Correct! The murderer was the {accused}, via {game_state['cause']}.")
                else:
                    print_output(f"Wrong. The murderer was the {game_state['murderer']}.")
                print_output("Game over. Refresh to play again.")
                disable_input()
            else:
                print_output("Invalid choice.")

        def disable_input():
            btn = document.getElementById('submit')
            btn.removeEventListener('click', on_submit)
            btn.disabled = True
            document.getElementById('command').disabled = True

        def on_submit(e):
            cmd = document.getElementById('command').value.strip()
            document.getElementById('command').value = ''
            if not cmd:
                return
            print_output(f"> {cmd}")
            if game_state['in_accusation']:
                process_accusation(cmd)
            else:
                process_input(cmd)

        # Attach event and start
        document.getElementById('submit').addEventListener('click', on_submit)
        init_game()