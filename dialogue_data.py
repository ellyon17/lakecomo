# --- Dialogue Trees (Revised May 1, 2025) ---

# Structure: DIALOGUE_TREES[suspect_id][node_id] = {
#     'text': "NPC line",
#     'options': [ ... ],
#     'action': None or "action_string" or ["action_string_1", "action_string_2"]
# }

DIALOGUE_TREES = {
    # --- Raffaella Patrizi ---
    "raffaella": {
        "START": {
            "text": "Detective. This is all just terrible... poor Cristiano.",
            "options": [
                {"text": "Can you tell me about last night?", 'next_node': 'ASK_LAST_NIGHT'},
                {"text": "Where were you around 3 AM?", 'next_node': 'ASK_ALIBI'},
                {"text": "Did you notice any arguments yesterday?", 'next_node': 'ASK_ARGUMENTS'},
                {"text": "How was your relationship with Cristiano?", 'next_node': 'ASK_RELATIONSHIP'},
                {"text": "Leave conversation.", 'next_node': 'END'}
            ],
            "action": None
        },
        "ASK_LAST_NIGHT": {
            "text": "The party ended late. Naomi sang... quite loudly. Afterwards, people drifted off. I went to my room around 11:30 PM, I think. Alone.",
            "options": [
                {"text": "Did you see Cristiano after the singing?", 'next_node': 'SEE_CRISTIANO_LATE'},
                {"text": "Did you notice any arguments yesterday?", 'next_node': 'ASK_ARGUMENTS'},
                {"text": "Where were you around 3 AM?", 'next_node': 'ASK_ALIBI'},
                {"text": "How was your relationship with Cristiano?", 'next_node': 'ASK_RELATIONSHIP'},
                {"text": "Leave conversation.", 'next_node': 'END'}
            ],
            "action": "record_testimony_went_to_room_alone" # Record general timeline info
        },
        "ASK_ALIBI": {
            "text": "At 3 AM? Asleep in my own suite, of course! Where else would I be? This is insulting.",
            "options": [
                {"text": "Did anyone see you?", 'next_node': 'ALIBI_WITNESS'},
                {"text": "Tell me about last night.", 'next_node': 'ASK_LAST_NIGHT'},
                {"text": "Leave conversation.", 'next_node': 'END'}
            ],
            "action": "record_alibi" # Record her stated alibi
        },
         "ALIBI_WITNESS": {
            "text": "See me? No! I was alone in my room after 11:30 PM. Ask Antonello, maybe he saw me go upstairs.",
            "options": [
                {"text": "Tell me about arguments yesterday.", 'next_node': 'ASK_ARGUMENTS'},
                {"text": "Leave conversation.", 'next_node': 'END'}
            ],
            "action": "record_testimony_alibi_no_witness"
        },
        "ASK_ARGUMENTS": {
            "text": "Arguments? Cristiano argued with everyone eventually. I saw him talking heatedly with Russell during dinner... something about money, I suppose. And he wasn't pleased with Gabriel and I chatting during the aperitivo.",
            "options": [
                {"text": "He argued with you too?", 'next_node': 'ARGUE_WITH_CRISTIANO'},
                 {"text": "Where were you around 3 AM?", 'next_node': 'ASK_ALIBI'},
                {"text": "Leave conversation.", 'next_node': 'END'}
            ],
             # This testimony covers Russell/Cristiano (Clue07 related) and C/G tension (Clue05 related)
            "action": ["record_testimony_raffaella_saw_arguments", "discover_clue07"] # Discover Clue07 (Russell/C argument)
        },
         "ARGUE_WITH_CRISTIANO": {
            "text": "We had a brief... disagreement after Naomi's performance. Just married couple things. Nothing serious.",
            "options": [
                 {"text": "Tell me about your relationship.", 'next_node': 'ASK_RELATIONSHIP'},
                 {"text": "Leave conversation.", 'next_node': 'END'}
            ],
            # This confirms the argument mentioned in Clue05
            "action": ["record_testimony_argued_with_cristiano", "discover_clue05"]
        },
        "ASK_RELATIONSHIP": {
            "text": "Cristiano gave me everything. Security. A certain lifestyle. But he was... demanding. And older. We had our difficulties.",
             "options": [
                 {"text": "Were you close with Gabriel DuPont?", 'next_node': 'ASK_GABRIEL'},
                 {"text": "Leave conversation.", 'next_node': 'END'}
            ],
            "action": "record_testimony_relationship_difficulties" # Background info
        },
        "ASK_GABRIEL": {
             # Avoids admitting affair directly, but records the statement
            "text": "Gabriel? He's a charming boy, a friend of Cristiano's. We talked, yes. He's amusing.",
             "options": [
                 {"text": "Did you see him late last night?", 'next_node': 'SEE_GABRIEL_LATE'},
                 {"text": "Leave conversation.", 'next_node': 'END'}
            ],
            "action": "record_testimony_opinion_of_gabriel"
        },
         "SEE_CRISTIANO_LATE": {
            "text": "I saw him briefly after Naomi sang, when we argued. Then he went towards the study, I believe. That was the last time.",
             "options": [
                 {"text": "Leave conversation.", 'next_node': 'END'}
            ],
            "action": "record_testimony_last_saw_cristiano"
        },
        "SEE_GABRIEL_LATE": {
            "text": "He went to his room shortly after I went to mine, I think. Around 11:30 PM or midnight.",
             "options": [
                 {"text": "Leave conversation.", 'next_node': 'END'}
            ],
             "action": "record_testimony_saw_gabriel_go_to_room"
        }
        # END node is implicit via the "Leave conversation" option
    },

    # --- Dr. Elisa Moretti ---
    "moretti": {
        "START": {
            "text": "Detective. I examined the body, but the exact cause requires an autopsy. However, I have my suspicions... about Ms. Marino.",
            "options": [
                 {"text": "What suspicions about Dakota Marino?", 'next_node': 'SUSPICION_DAKOTA'},
                 {"text": "What was Cristiano's health like?", 'next_node': 'ASK_HEALTH'},
                 {"text": "Where were you around 3 AM?", 'next_node': 'ASK_ALIBI'},
                 {"text": "Leave conversation.", 'next_node': 'END'}
            ],
            "action": None
        },
        "SUSPICION_DAKOTA": {
             # This directly relates to her notebook (Clue13) and context for Clue01/Clue02/Clue03
             "text": "Cristiano was under my care, taking medication for blood pressure. But he was also secretly taking supplements from Ms. Marino. I warned him about potential interactions. She dismissed my concerns.",
             "options": [
                 {"text": "What kind of supplements?", 'next_node': 'ASK_SUPPLEMENTS'},
                 {"text": "What was his health like otherwise?", 'next_node': 'ASK_HEALTH'},
                 {"text": "Leave conversation.", 'next_node': 'END'}
             ],
             "action": ["record_testimony_moretti_warning_supplements", "discover_clue13"] # Discover clue about her concerns/notebook
         },
         "ASK_HEALTH": {
              # This also relates to Clue13
             "text": "He had high blood pressure, managed with medication. Recently, he'd shown worrying signs - dizziness, arrhythmia. I suspected external factors... like those 'supplements'.",
             "options": [
                  {"text": "Did you argue with Dakota about this?", 'next_node': 'ARGUE_DAKOTA'},
                  {"text": "Where were you around 3 AM?", 'next_node': 'ASK_ALIBI'},
                  {"text": "Leave conversation.", 'next_node': 'END'}
             ],
             "action": ["record_testimony_cristiano_symptoms", "discover_clue13"] # Also discovers clue about symptoms/notebook
         },
         "ASK_ALIBI": {
             "text": "I retired to my room around 9:30 PM after Naomi started singing. I read for a while. Around 1:30 AM, I briefly went to the hallway - thought I heard something - but saw nothing and returned to my room and slept.", # Mentions being near Study hallway late
             "options": [
                  {"text": "Did you hear anything specific?", 'next_node': 'HEARD_SOMETHING'},
                  {"text": "Did you see anyone?", 'next_node': 'SEE_ANYONE_LATE'},
                  {"text": "Leave conversation.", 'next_node': 'END'}
             ],
             "action": "record_alibi" # Records her alibi
         },
         "ARGUE_DAKOTA": {
             # This confirms Clue04 testimony
             "text": "At dinner, yes! I told her she was being reckless, peddling untested nonsense. She called my medicine poison! Cristiano just laughed...",
             "options": [
                 {"text": "What supplements was she giving him?", 'next_node': 'ASK_SUPPLEMENTS'},
                 {"text": "Leave conversation.", 'next_node': 'END'}
             ],
             "action": ["record_testimony_moretti_dinner_argument", "discover_clue04"]
         },
          "ASK_SUPPLEMENTS": {
             # This hints towards Clue02 / Clue03 (physical clues) but doesn't discover them
             "text": "I don't know exactly. Something herbal, potent... she was very secretive. Check her room or the greenhouse maybe.",
             "options": [
                 {"text": "Tell me about your alibi.", 'next_node': 'ASK_ALIBI'},
                 {"text": "Leave conversation.", 'next_node': 'END'}
             ],
             "action": "record_testimony_moretti_supplement_details"
         },
         "HEARD_SOMETHING": {
             "text": "Just... movement? A door closing softly down the hall perhaps. Nothing distinct. I went back to bed.",
             "options": [
                 {"text": "Did you see anyone?", 'next_node': 'SEE_ANYONE_LATE'},
                 {"text": "Leave conversation.", 'next_node': 'END'}
             ],
             "action": "record_testimony_heard_movement"
         },
          "SEE_ANYONE_LATE": {
             "text": "No, the hallway was empty when I looked out around 1:30 AM.",
             "options": [
                 {"text": "Leave conversation.", 'next_node': 'END'}
             ],
             "action": "record_testimony_saw_noone_late"
         },
    },

    # --- Marco Santini ---
     "marco": {
        "START": {
            "text": "Detective... I just take care of the boats. I saw things, sure, but I stayed out of the way.",
            "options": [
                {"text": "What did you see last night?", "next_node": "ASK_SAW_LAST_NIGHT"},
                {"text": "Where were you around 3 AM?", "next_node": "ASK_ALIBI"},
                # Add specific question for Clue09
                {"text": "Did you see Gabriel near Raffaella's room?", "next_node": "ASK_SAW_GABRIEL_LEAVE_RAFFAELLA"},
                {"text": "Did you have any conflicts with Gabriel DuPont?", "next_node": "ASK_GABRIEL_CONFLICT"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": None
        },
        "ASK_SAW_LAST_NIGHT": {
             # Describes scene relevant to Clue05 context
            "text": "During the day, I saw Signora Patrizi and Signor DuPont chatting very close by the pool. Later, near sunset, I saw them again... too close, laughing. Cristiano noticed too. The air was tense.",
            "options": [
                {"text": "Did Cristiano react?", "next_node": "CRISTIANO_REACTION"},
                {"text": "Did you see Gabriel near Raffaella's room?", "next_node": "ASK_SAW_GABRIEL_LEAVE_RAFFAELLA"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_marco_saw_RG_pool" # Record this observation
        },
        # New node specifically for Clue09
        "ASK_SAW_GABRIEL_LEAVE_RAFFAELLA": {
            "text": "Mid-afternoon, yes... I saw Signor DuPont coming from the direction of her rooms. He looked... flustered. Avoided my eyes.",
            "options": [
                {"text": "What else did you see last night?", "next_node": "ASK_SAW_LAST_NIGHT"},
                {"text": "Tell me about your conflict with Gabriel.", "next_node": "ASK_GABRIEL_CONFLICT"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": ["record_testimony_marco_saw_G_leave_R", "discover_clue09"] # Discover Clue09
        },
        "CRISTIANO_REACTION": {
            # Confirms argument context for Clue05
            "text": "He was furious. Later during Naomi's singing, Cristiano grabbed Raffaella aside. I heard whispers. Accusations about Gabriel. It wasn’t a happy birthday night, Detective.",
            "options": [
                {"text": "Tell me about your own situation with Gabriel.", "next_node": "ASK_GABRIEL_CONFLICT"},
                {"text": "Did you see Gabriel near Raffaella's room?", "next_node": "ASK_SAW_GABRIEL_LEAVE_RAFFAELLA"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": ["record_testimony_marco_saw_CR_argue", "discover_clue05"] # Links to C/R argument Clue05
        },
        "ASK_ALIBI": {
            "text": "After everything... I went down to the docks. I needed air. I stayed there till late, maybe midnight, then went to my quarters.",
            "options": [
                {"text": "Can anyone confirm that?", "next_node": "ALIBI_CONFIRM"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_alibi" # Record his alibi
        },
        "ALIBI_CONFIRM": {
            "text": "Antonello might've seen me coming back up from the docks. I wasn't thinking about being seen... just needed to clear my head.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_alibi_confirm_antonello"
        },
        "ASK_GABRIEL_CONFLICT": {
            # Background info / motive context
            "text": "Gabriel... he was different. Open. Free. Things I can't be, not here, not with this world watching.",
            "options": [
                {"text": "Did you argue with him?", "next_node": "ARGUE_WITH_GABRIEL"},
                {"text": "Were you jealous of Raffaella?", "next_node": "JEALOUS_OF_RAFFAELLA"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_marco_feelings_about_gabriel"
        },
        "ARGUE_WITH_GABRIEL": {
            # Confirms argument from Clue15
            "text": "We had words by the pool. I accused him of playing games—with everyone. With me. I said too much. Others might have heard.",
            "options": [
                {"text": "What happened after that?", "next_node": "AFTER_ARGUMENT"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": ["record_testimony_marco_argued_gabriel_pool", "discover_clue15"]
        },
        "AFTER_ARGUMENT": {
             # Context for Clue16 location
            "text": "I ran off towards the docks. Gabriel followed later. We argued again on the yacht. Quietly. No one else saw.",
            "options": [
                {"text": "What did you argue about?", "next_node": "YACHT_ARGUMENT"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_marco_yacht_argument_location" # Doesn't discover physical Clue16
        },
        "YACHT_ARGUMENT": {
            "text": "I... I wanted him to be honest. To not hide behind flirting with Raffaella. To admit there was something real between us. He said it was just fun. No promises. That crushed me.",
            "options": [
                {"text": "Did you threaten him?", "next_node": "THREATEN_GABRIEL"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_marco_yacht_argument_content"
        },
        "THREATEN_GABRIEL": {
            "text": "No. I begged him not to say anything. If Cristiano knew... if anyone knew... I'd lose everything. So I left. Alone.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_marco_did_not_threaten"
        },
        "JEALOUS_OF_RAFFAELLA": {
            "text": "Maybe. She could be open about her feelings. I can't. I have to hide everything. It eats at you, you know?",
            "options": [
                {"text": "Did Cristiano know about you?", "next_node": "CRISTIANO_KNOW"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_marco_jealousy_raffaella"
        },
        "CRISTIANO_KNOW": {
            "text": "I don't think so. Maybe he suspected something. But if he knew for sure... he would have destroyed me.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_marco_cristiano_didnt_know"
        }
    },

    # --- Antonello Pisani ---
    "antonello": {
            "START": {
            "text": "Good morning, Detective. A terrible shock. I found him, you know. In the study, around 4 AM. Door was unlocked, which was unusual.",
            "options": [
                {"text": "Tell me about finding the body.", "next_node": "FINDING_BODY"},
                {"text": "What did you observe last night?", "next_node": "ASK_OBSERVATIONS"},
                {"text": "Where were you between midnight and 4 AM?", "next_node": "ASK_ALIBI"},
                {"text": "Did Cristiano seem concerned about anything?", "next_node": "ASK_CRISTIANO_STATE"}, # Add question for Clue14 context
                {"text": "Did you see Raffaella go to her room?", "next_node": "SAW_RAFFAELLA"},
                {"text": "Did you see Dakota visiting Cristiano?", "next_node": "SAW_DAKOTA"},
                {"text": "Did you see Marco return from the docks?", "next_node": "SAW_MARCO"},
                {"text": "Did you see Giovanna leave last night?", "next_node": "SAW_GIOVANNA_LEAVE"}, # Add question for Clue24
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_antonello_found_body_time"
        },
        "FINDING_BODY": {
             # Mentions overturned glass (Clue25)
            "text": "I do my rounds starting at 4 AM. The study light was on, door unlocked. Signor Patrizi was... slumped in his chair. The glass was overturned.",
            "options": [
                {"text": "Did you touch anything?", "next_node": "TOUCH_SCENE"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": ["record_testimony_finding_body_details", "discover_clue25"]
        },
        "TOUCH_SCENE": {
            "text": "No, Detective. I checked for breathing, then immediately called Signora Patrizi and Dr. Moretti.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_did_not_touch_scene"
        },
        "ASK_OBSERVATIONS": {
             # Confirms Russell cut off (Clue07), saw Dakota visit (Clue01 context), saw Marco
            "text": "The evening was tense. I overheard Signor Patrizi refusing Mr. Williams money near the pool bar. Later, I saw Ms. Marino carrying a drink towards the study around 1 AM. Marco looked upset when returning from the docks.",
            "options": [
                {"text": "Did you see Dr. Moretti near the study?", "next_node": "SEE_MORETTI_LATE"},
                {"text": "Did Cristiano seem concerned about anything?", "next_node": "ASK_CRISTIANO_STATE"},
                {"text": "Did you see Giovanna leave?", "next_node": "SAW_GIOVANNA_LEAVE"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": ["record_testimony_antonello_observations_evening", "discover_clue07"] # Discover Clue07
        },
        "ASK_ALIBI": {
            "text": "Between midnight and 4 AM, I was clearing the dining room, checking the locks, and ensuring the house was secure. I retired around 2:30 AM, then started rounds again at 4 AM.",
            "options": [
                {"text": "Did you see anyone else during that time?", "next_node": "SEE_ANYONE_MIDNIGHT_4AM"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_alibi"
        },
        # New node for Clue14 context
        "ASK_CRISTIANO_STATE": {
            "text": "Signor Patrizi seemed... preoccupied. He finalized some decisions yesterday. He asked me to ensure an email to his lawyer was sent regarding my son's business idea... the answer was no. A disappointment, certainly.",
            "options": [
                {"text": "Tell me about finding the body.", "next_node": "FINDING_BODY"},
                {"text": "What else did you observe?", "next_node": "ASK_OBSERVATIONS"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": ["record_testimony_antonello_son_rejected", "discover_clue14"] # Provides context and discovers Clue14 fact
        },
        "SEE_ANYONE_MIDNIGHT_4AM": {
            "text": "Only Ms. Marino heading toward the study around 1 AM, and Dr. Moretti peeking into the hallway near 1:30 AM. No one else.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_antonello_saw_dakota_moretti_late"
        },
        "SEE_MORETTI_LATE": {
            "text": "Yes, around 1:30 AM. She looked into the hallway near the study, hesitated, then returned to her room.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_antonello_saw_moretti_hesitate"
        },
        "SAW_RAFFAELLA": {
            "text": "Yes, I saw Signora Patrizi heading upstairs after Naomi's singing, around 11:30 PM. She did not come down again, as far as I observed.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_antonello_saw_raffaella_upstairs"
        },
        "SAW_DAKOTA": {
            # Confirms time Dakota went to study (Clue01 context)
            "text": "Indeed. Around 1 AM, Ms. Marino carried a drink—her so-called 'tonic'—toward the study. She seemed confident, not sneaky.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             # This testimony is crucial context for Clue01 (found in Study)
             # Let's also discover Clue01 here if the player hasn't found the residue yet.
             "action": ["record_testimony_antonello_saw_dakota_tonic", "discover_clue01"]
        },
        "SAW_MARCO": {
            "text": "Young Marco returned from the docks looking upset, around midnight. His clothes were a little disheveled, but he said nothing to me.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_antonello_saw_marco_return"
        },
        # New node for Clue24
        "SAW_GIOVANNA_LEAVE": {
            "text": "Ah yes, the chef. Signora Russo left the villa around 10:30 PM after her duties were finished. I saw her drive away myself.",
            "options": [
                 {"text": "What did you observe inside the villa later?", "next_node": "ASK_OBSERVATIONS"},
                 {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": ["record_testimony_antonello_saw_giovanna_leave", "discover_clue24"] # Confirms Giovanna's alibi clue
        }
    },

# --- Dakota Marini ---
    "dakota": {
        "START": {
            "text": "Detective, Cristiano's health was compromised by traditional medicine. My wellness path could've healed him.",
            "options": [
                {"text": "What exactly did you give Cristiano?", "next_node": "ASK_SUPPLEMENTS"},
                {"text": "Did you visit Cristiano late last night?", "next_node": "VISIT_STUDY"},
                {"text": "Did you argue with Dr. Moretti about your treatments?", "next_node": "ARGUE_MORETTI"},
                {"text": "Where were you around 3 AM?", "next_node": "ASK_ALIBI"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": None
        },
        "ASK_SUPPLEMENTS": {
             # Admits giving Danshen extract (Clue01/Clue02/Clue03 context)
            "text": "I provided Cristiano with a vitality tonic made from pure Danshen extract. It's a traditional herb for circulation and heart health.",
            "options": [
                {"text": "Was this tonic safe to mix with his medication?", "next_node": "SUPPLEMENT_SAFETY"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             # This confirms the substance from Clue01/Clue02/Clue03
            "action": ["record_testimony_dakota_gave_danshen", "discover_clue01", "discover_clue02", "discover_clue03"] # Discover related clues
        },
        "SUPPLEMENT_SAFETY": {
            # Shows awareness/dismissal of risk (Clue03 context)
            "text": "There are always risks with pharmaceuticals. Natural remedies support the body holistically. Cristiano trusted me.",
            "options": [
                {"text": "Did Cristiano show any adverse reactions?", "next_node": "ADVERSE_REACTIONS"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_dakota_dismissed_risks"
        },
        "ADVERSE_REACTIONS": {
             # Admits symptoms but dismisses them (links to Moretti Clue13)
            "text": "He mentioned some dizziness, but I attributed that to detox symptoms. A sign his body was healing.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_dakota_observed_symptoms"
        },
        "VISIT_STUDY": {
             # Confirms visit time (matches Antonello's testimony)
            "text": "Yes, I brought Cristiano his nightly tonic around 2:30 AM. We spoke briefly. He seemed tired but calm.",
            "options": [
                {"text": "Did anyone else see you?", "next_node": "SEEN_BY_ANYONE"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_dakota_visited_study"
        },
        "SEEN_BY_ANYONE": {
            "text": "I believe Antonello saw me walking that way. But he didn't question me. Everyone knew I cared for Cristiano's health.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_dakota_thinks_antonello_saw"
        },
        "ARGUE_MORETTI": {
             # Confirms dinner argument (Clue04)
            "text": "Yes, during dinner. Dr. Moretti clings to outdated, chemical-based medicine. I offer natural healing. Cristiano needed a real path to vitality.",
            "options": [
                {"text": "Did Cristiano agree with you?", "next_node": "CRISTIANO_AGREEMENT"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": ["record_testimony_dakota_dinner_argument", "discover_clue04"]
        },
        "CRISTIANO_AGREEMENT": {
            "text": "He was open-minded. He laughed off Dr. Moretti's warnings. He knew true healing doesn't come in pills.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_dakota_cristiano_agreed"
        },
        "ASK_ALIBI": {
            "text": "After delivering the tonic, I returned to my room to meditate. I stayed there until the commotion started.",
            "options": [
                {"text": "Can anyone confirm that?", "next_node": "ALIBI_CONFIRM"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_alibi" # Records her alibi
        },
        "ALIBI_CONFIRM": {
            "text": "I'm not sure. I value solitude after my rituals. But I have nothing to hide.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_dakota_alibi_no_witness"
        }
    },

# --- Russell Williams ---
    "russell": {
        "START": {
            "text": "Devastating. Cristiano was complex, but he was a valued friend.",
            "options": [
                {"text": "Did you argue with Cristiano about money?", "next_node": "ASK_FINANCES"},
                {"text": "Where were you around 3 AM?", "next_node": "ASK_ALIBI"},
                {"text": "What was your financial situation recently?", "next_node": "ASK_FINANCIAL_TROUBLES"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": None
        },
        "ASK_FINANCES": {
             # Admits asking for money, confirms Clue07
            "text": "It was a misunderstanding. I merely asked Cristiano for a small liquidity bridge. He overreacted.",
            "options": [
                {"text": "Did the disagreement get heated?", "next_node": "DISAGREEMENT_HEATED"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": ["record_testimony_russell_asked_money", "discover_clue07"]
        },
        "DISAGREEMENT_HEATED": {
            "text": "I suppose. Voices were raised. I regret it now, obviously. But that doesn't make me a killer.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_russell_argument_heated"
        },
        "ASK_ALIBI": {
             # Provides alibi, which is Clue21
            "text": "I was in my suite with Rose from around 11 PM. Antonello brought us tea around midnight. We didn't leave afterward.",
            "options": [
                {"text": "Can anyone confirm this?", "next_node": "CONFIRM_ALIBI"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": ["record_alibi", "discover_clue21"]
        },
        "CONFIRM_ALIBI": {
            "text": "Antonello can confirm bringing the tea. Check the villa's security logs if you must.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_russell_alibi_confirm"
        },
        "ASK_FINANCIAL_TROUBLES": {
             # Refers to financial state (Clue12 context)
            "text": "Business has been... challenging. Traditional media faces headwinds. I was exploring partnerships to pivot into tech.",
            "options": [
                {"text": "Was Cristiano blocking that pivot?", "next_node": "CRISTIANO_BLOCKING"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": ["record_testimony_russell_financial_troubles", "discover_clue12"] # Discover Clue12 fact
        },
        "CRISTIANO_BLOCKING": {
            "text": "Cristiano had influence over certain investors. If he spoke against me, it could've been disastrous. But murder? That's absurd.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_russell_cristiano_blocking"
        }
    },

# --- Rose Williams ---
     "rose": {
        "START": {
            "text": "It's dreadful. Russell is devastated. Cristiano could be difficult, but... this is too much.",
            "options": [
                {"text": "Where were you around 3 AM?", "next_node": "ASK_ALIBI"},
                {"text": "Were you aware of Russell's financial troubles?", "next_node": "ASK_RUSSELL_TROUBLES"},
                {"text": "How did you personally feel about Cristiano?", "next_node": "OPINION_CRISTIANO"},
                 # Add question for Clue17
                {"text": "What did you think of Naomi's performance?", "next_node": "ASK_NAOMI_PERFORMANCE"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": None
        },
        "ASK_ALIBI": {
             # Provides alibi, confirms Clue21
            "text": "Russell and I were in our suite all night. Antonello brought us tea around midnight. We never left until the alarm.",
            "options": [
                {"text": "Can Antonello confirm that?", "next_node": "CONFIRM_ALIBI"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": ["record_alibi", "discover_clue21"]
        },
        "CONFIRM_ALIBI": {
            "text": "Yes, he can. He brought the tea personally. And I'm sure the villa's security logs will support it too.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_rose_alibi_confirm"
        },
        "ASK_RUSSELL_TROUBLES": {
             # Confirms financial troubles (Clue12 context)
            "text": "I knew Russell was under pressure. The media business isn't what it used to be. Cristiano withdrawing support would've been catastrophic.",
            "options": [
                {"text": "Did you blame Cristiano for this?", "next_node": "BLAME_CRISTIANO"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": ["record_testimony_rose_aware_troubles", "discover_clue12"] # Discover Clue12 fact
        },
        "BLAME_CRISTIANO": {
            # Provides motive context
            "text": "I resented how he toyed with our future, yes. But that doesn't mean I wished him harm. I just wanted him to reconsider.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_rose_resented_cristiano"
        },
        "OPINION_CRISTIANO": {
            "text": "Cristiano was a force of nature. Charismatic, commanding. But he also loved control—over people, over outcomes. It made him enemies.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_rose_opinion_cristiano"
        },
         # New node for Clue17
        "ASK_NAOMI_PERFORMANCE": {
             # This is the dismissive comment from Clue17
            "text": "Oh, the young lady? Enthusiastic, I suppose. A bit... modern for my tastes. Not exactly La Scala, was it?",
            "options": [
                 {"text": "Were you aware of Russell's financial troubles?", "next_node": "ASK_RUSSELL_TROUBLES"},
                 {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": ["record_testimony_rose_naomi_performance", "discover_clue17"]
        }
    },

 # --- Gabriel DuPont ---
     "gabriel": {
        "START": {
            "text": "Merde. Cristiano... he lived fast. But like this? No. I was on a call most of the night.",
            "options": [
                {"text": "Where were you around 3 AM?", "next_node": "ASK_ALIBI"},
                {"text": "Tell me about your relationship with Raffaella.", "next_node": "RELATIONSHIP_RAFFAELLA"},
                {"text": "What happened between you and Marco?", "next_node": "CONFLICT_MARCO"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": None
        },
        "ASK_ALIBI": {
             # Provides alibi, which is Clue23
            "text": "I was on a video call with my racing team in California from about 1:05 AM to past 3:30 AM. Check the logs if you want.",
            "options": [
                {"text": "Can you show me the call log?", "next_node": "SHOW_CALL_LOG"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": ["record_alibi", "discover_clue23"]
        },
        "SHOW_CALL_LOG": {
             # Confirms details of Clue23
            "text": "Of course. Here. You can see the timestamps. Practice strategies for Laguna Seca. Long call, too boring for murder.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_gabriel_showed_log" # No need to re-discover Clue23
        },
        "RELATIONSHIP_RAFFAELLA": {
             # Context for Clue05/Clue11
            "text": "She was charming. Flirtatious, even. But it was harmless fun. She needed escape. Cristiano... was controlling.",
            "options": [
                {"text": "Did Cristiano confront you about Raffaella?", "next_node": "CONFRONTED_BY_CRISTIANO"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_gabriel_relationship_raffaella"
        },
        "CONFRONTED_BY_CRISTIANO": {
            # Confirms argument from Clue05
            "text": "After Naomi sang, Cristiano pulled Raffaella aside. I caught a glimpse. He was furious. He accused her of making a fool of him—with me.",
            "options": [
                {"text": "Did you and Raffaella have an affair?", "next_node": "DENY_AFFAIR"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": ["record_testimony_gabriel_saw_confrontation", "discover_clue05"]
        },
        "DENY_AFFAIR": {
            "text": "It was just flirtation. Maybe it went too far in words... but no. Nothing physical. Not with her.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_gabriel_denies_affair"
        },
        "CONFLICT_MARCO": {
             # Confirms argument @ pool (Clue15)
            "text": "Marco is... sensitive. He got upset when he saw me with Raffaella. We argued by the pool. Later, he followed me to the docks.",
            "options": [
                {"text": "What happened at the docks?", "next_node": "DOCKS_ENCOUNTER"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": ["record_testimony_gabriel_conflict_marco_pool", "discover_clue15"]
        },
        "DOCKS_ENCOUNTER": {
             # Context for Clue16 location
            "text": "We talked aboard the yacht. Heated words, emotions... Look, Marco wanted more than I could give. I tried to let him down gently.",
            "options": [
                {"text": "Did Marco threaten you?", "next_node": "MARCO_THREAT"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_gabriel_conflict_marco_yacht" # Doesn't discover physical Clue16
        },
        "MARCO_THREAT": {
            "text": "No, no threats. Just... pain. I didn't want to hurt him. But secrets... in a place like this? Dangerous.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_gabriel_marco_no_threat"
        }
    },

 # --- Sundeep Arora ---
     "sundeep": {
        "START": {
            "text": "Tragic. Really tragic. Bad for business, bad for everyone. I barely knew him, really.",
            "options": [
                {"text": "Where were you around 3 AM?", "next_node": "ASK_ALIBI"},
                {"text": "Did you have any interactions with Cristiano yesterday?", "next_node": "ASK_CRISTIANO_INTERACTION"},
                {"text": "How did you feel about being dismissed by Cristiano?", "next_node": "HUMILIATION_REACTION"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": None
        },
        "ASK_ALIBI": {
             # Provides alibi, which is Clue22
            "text": "After dinner I argued with Naomi. We were in our room from around 11:30 PM. I drank a lot. Naomi says I passed out before 1 AM.",
            "options": [
                {"text": "Can Naomi confirm that?", "next_node": "CONFIRM_NAOMI"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": ["record_alibi", "discover_clue22"]
        },
        "CONFIRM_NAOMI": {
            "text": "Yeah. She told me I snored loud enough to wake the dead. She would have said if I'd left.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_sundeep_alibi_confirm"
        },
        "ASK_CRISTIANO_INTERACTION": {
             # Confirms dismissal (Clue08)
            "text": "Tried to talk business. Pitched some ideas. He laughed. Said I was just another app boy. Told me to run along and let the adults talk.",
            "options": [
                {"text": "How did that make you feel?", "next_node": "HUMILIATION_REACTION"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": ["record_testimony_sundeep_dismissal_details", "discover_clue08"]
        },
        "HUMILIATION_REACTION": {
             # Motive context
            "text": "It stung. More than I want to admit. I built something real. And he dismissed me like garbage because I wasn't born rich.",
            "options": [
                {"text": "Did you ever threaten him?", "next_node": "THREATEN_CRISTIANO"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_sundeep_humiliation"
        },
        "THREATEN_CRISTIANO": {
            "text": "No. I thought about telling him off, sure. But what's the point? He was part of that old money world. They don't see people like me as equals.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": "record_testimony_sundeep_no_threat"
        }
    },

 # --- Naomi Lee ---
     "naomi": {
        "START": {
            "text": "OMG, it's like, totally horrible? I sang for him last night, he seemed fine... maybe a little stressed?",
            "options": [
                {"text": "Where were you around 3 AM?", "next_node": "ASK_ALIBI"},
                {"text": "How did Cristiano seem after your performance?", "next_node": "CRISTIANO_REACTION"},
                {"text": "Were you interested in Cristiano?", "next_node": "ASK_FLIRTING"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
            "action": None
        },
        "ASK_ALIBI": {
             # Confirms Sundeep's alibi (Clue22)
            "text": "I was with Sundeep until like 1 AM. We argued a bit after dinner... but after that, honestly, I kinda needed a break. I stayed in the room mostly.",
            "options": [
                {"text": "Can Sundeep confirm that?", "next_node": "CONFIRM_ALIBI"}, # Should be "Did Sundeep stay passed out?"
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             # Records her statement confirming Sundeep passed out
             "action": ["record_testimony_naomi_sundeep_passed_out", "discover_clue22"]
        },
        "CONFIRM_ALIBI": { # Rephrased from original
            "text": "Yeah. He was super drunk. Fell asleep snoring. I could have left the room after 1 AM, I guess, but like... why would I?",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_alibi" # Records HER alibi (stayed in room mostly)
        },
        "CRISTIANO_REACTION": {
             # Context for Red Herring Clue18 (hair)
            "text": "He seemed to like my singing! I mean, he smiled a lot. Kinda... lingering? It was flattering. Sundeep got a little mad though.",
            "options": [
                {"text": "Did you spend time alone with Cristiano after?", "next_node": "TIME_ALONE_CRISTIANO"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_naomi_cristiano_liked_singing"
        },
        "TIME_ALONE_CRISTIANO": {
            "text": "Uh, no? I mean, not really. Maybe a few words after the show? He said he liked my style. That's all.",
            "options": [
                {"text": "Are you sure about that?", "next_node": "PRESS_TIME_ALONE"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_naomi_denies_time_alone"
        },
        "PRESS_TIME_ALONE": {
             # Still denies, but hints at temptation (Red Herring Clue18 context)
            "text": "I mean... maybe I thought about it? Cristiano was powerful. Charismatic. But I swear, nothing happened!",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_naomi_tempted"
        },
        "ASK_FLIRTING": {
             # Motive context (Red Herring Clue18)
            "text": "Look, it's not like I planned anything. But if he noticed me? Not my fault. A girl's gotta think about her future, right?",
            "options": [
                {"text": "Were you hoping for something more?", "next_node": "HOPING_FOR_MORE"},
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_naomi_flirting_ambition"
        },
        "HOPING_FOR_MORE": {
            "text": "Maybe... I mean, Sundeep's great but Cristiano? He was like real money. Real power. Could change a girl's life overnight.",
            "options": [
                {"text": "Leave conversation.", "next_node": "END"}
            ],
             "action": "record_testimony_naomi_hoping_for_more"
        }
    }
    # Note: Giovanna Russo has no dialogue tree as she was off-site per Clue24.
    # Her alibi is discovered via Antonello's testimony (node SAW_GIOVANNA_LEAVE).
}

# --- End of Dialogue Trees ---