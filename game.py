from js import document

def print_output(text):
    out = document.getElementById('output')
    out.innerHTML += text + "<br/>"
    out.scrollTop = out.scrollHeight

def start_game():
    print_output("✅ Minimal test works!")

start_game()
