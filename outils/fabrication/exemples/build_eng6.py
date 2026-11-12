"""Anglais 6e « Hello! Words for school and home » — élève allophone non lecteur : écouter, regarder, répéter au micro."""
import json, sys
sys.path.insert(0, "/home/claude/eng6")
from helpers import uid, durl, pano, info, find, scene, check, errors
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
P15 = "/home/claude/out15/medias/panos"; OBJ = "/home/claude/out16/medias/obj"
def P(path):
    im = Image.open(path).convert("RGB")
    if im.size != (4096, 2048): im = im.resize((4096, 2048), Image.LANCZOS)
    im.save("/tmp/p4k.jpg", quality=92); e = pano("/tmp/p4k.jpg"); e["name"] = path.split("/")[-1]; return e
def obj(k):
    im = Image.open(f"{OBJ}/{k}.jpg").convert("RGB"); s = min(1, 900 / im.width, 900 / im.height)
    if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return durl(im, 85)
def say(phrase, az, el, ex="", img=None, text="", exS=None, textS=None, accept=None, title=None):
    h = {"id": uid(), "type": "say", "title": title or phrase.rstrip(".!?"), "question": phrase, "explanation": ex, "az": az, "el": el}
    if text: h["text"] = text
    if textS: h["textS"] = textS
    if exS: h["explanationS"] = exS
    if img: h["image"] = obj(img)
    if accept: h["accept"] = accept
    return check(h, phrase)
def inf(title, text, az, el, textS=None):
    h = info(title, text, az, el)
    if textS: h["textS"] = textS
    return h
def fnd(q, taz, tel, ex, az, el, tol=13, exS=None):
    h = find(q, taz, tel, ex, az, el, tol); h["title"] = "Find it!"
    if exS: h["explanationS"] = exS
    return h
S = []
# 1 ------------------------------------------------------------------ Hello!
S.append(scene("Hello!", P(f"{P15}/yard.jpg"),
 "Hello! Welcome to school! Look around you. Touch a point and listen. Then touch Speak and repeat. The yellow points with a microphone are for you: listen and speak!",
 [inf("the school", "This is a school. It is big.", -75, 24, "This is a school."),
  inf("a tree", "This is a tree. It is green.", 18, 32, "This is a tree."),
  inf("the playground", "This is the playground. Children play here.", -40, -24, "This is the playground."),
  say("Hello!", -150, 4, "Hello! Hi!"),
  say("Good morning!", -115, -10, "Good morning! We say it in the morning."),
  say("How are you?", 55, -6, "How are you? Now answer: I'm fine, thank you."),
  say("I'm fine, thank you.", 90, -6, "I'm fine, thank you!"),
  say("What's your name?", 143, -14, "What's your name? Answer: my name is… and say your name!"),
  say("Goodbye!", 165, 0, "Goodbye! See you!"),
  fnd("Find the door.", 2, 6, "Here is the door of the school. Come in!", -20, -6, 14),
  fnd("Find the bin.", 125, -5, "Here is the bin. Put your paper in the bin!", 100, 8, 10)]))
S[0]["introS"] = "Hello! Touch the points. Listen and repeat."
# 2 ------------------------------------------------------------------ My classroom
S.append(scene("My classroom", P(f"{P15}/class1.jpg"),
 "This is a classroom. There are desks, chairs and a board. Touch the microphones. Listen to the words and repeat them.",
 [say("the board", -8, 6, "The board. The teacher writes on the board."),
  inf("the teacher's desk", "This is the teacher's desk.", 12, -8),
  say("a desk", 99, -30, "A desk. I sit at my desk."),
  say("a chair", 65, -36, "A chair. Sit down on your chair."),
  say("a window", -82, 15, "A window. Open the window!"),
  say("the door", 146, 6, "The door. Close the door, please."),
  say("a school bag", 24, -22, "A school bag. My books are in my school bag.", accept=["school bag", "bag"]),
  say("a book", 45, -16, "A book. Open your book!"),
  fnd("Find the clock.", -162, 3, "Here is the clock. Say: a clock!", -130, 10, 10),
  fnd("Find an orange school bag.", -160, -9, "Here is the orange school bag!", -125, -12, 11)]))
S[1]["introS"] = "This is a classroom. Listen and repeat."
# 3 ------------------------------------------------------------------ In class
S.append(scene("In class", P(f"{P15}/class2.jpg"),
 "Now we are in class. What is in your pencil case? Look at the pictures, listen and repeat. Then learn to speak to your teacher.",
 [say("a pencil", -150, -4, "A pencil. I write with a pencil.", img="pencil_1"),
  say("a pen", -125, 0, "A pen. A blue pen.", img="pen_2"),
  say("scissors", -100, -4, "Scissors. I cut paper with scissors.", img="scissors_1"),
  say("a pencil case", -75, 0, "A pencil case. My pencils are in my pencil case.", img="pencilcase_0"),
  say("an exercise book", -50, -4, "An exercise book. I write in my exercise book.", img="exercisebook_0", accept=["exercise book"]),
  inf("the board", "This is the board. The teacher writes on the board.", 117, 12),
  say("I don't understand.", 62, 2, "I don't understand. The teacher can help you."),
  say("Can you repeat, please?", 88, -4, "Can you repeat, please? Say it to your teacher."),
  say("Can I go to the toilet, please?", -22, -6, "Can I go to the toilet, please? Yes, you can!"),
  say("Sorry!", 150, -6, "Sorry! We say sorry when we make a mistake."),
  fnd("Find the bin.", 26, -10, "Here is the bin.", 0, -4, 9)]))
S[2]["introS"] = "We are in class. Look, listen and repeat."
# 4 ------------------------------------------------------------------ Lunch time
S.append(scene("Lunch time!", P(f"{P15}/canteen.jpg"),
 "It's twelve o'clock. It's lunch time! This is the canteen. What can you eat and drink? Look, listen and repeat.",
 [inf("the cook", "This is the cook. She makes lunch. Say: thank you!", -126, 2),
  say("Thank you!", -128, -18, "Thank you! The cook is happy."),
  say("an apple", 111, -10, "An apple. Apples are red or green.", img="apple_0"),
  say("a banana", 60, 2, "A banana. Bananas are yellow.", img="banana_3"),
  say("bread", 78, -8, "Bread. I eat bread.", img="bread_3"),
  say("orange juice", 133, -24, "Orange juice. I drink orange juice.", img="juice_0"),
  say("water", 40, -2, "Water. I drink water.", img="water_2"),
  say("I'm hungry.", -160, 6, "I'm hungry. I want to eat."),
  say("I'm thirsty.", 145, 8, "I'm thirsty. I want to drink."),
  say("Can I have some water, please?", 20, 10, "Can I have some water, please? Here you are!"),
  fnd("Find the apples.", -2, -42, "Here are the apples, in a bowl!", -20, -10, 12),
  fnd("Find the flowers.", 171, -2, "Here are the flowers. They are red.", 150, -14, 10)]))
S[3]["introS"] = "Lunch time! Look, listen and repeat."
# 5 ------------------------------------------------------------------ At home
cred = ("Photos 360°: schoolyard and classroom 2 by PantheraLeo1359531 (CC BY-SA 4.0, CC BY 4.0); classroom 1 by Jiazheng0609 (CC BY-SA 4.0); "
        "canteen by Lauri Veerde (CC BY-SA 4.0); kitchen: Carl Sandburg Home, NPS (public domain). Pictures: Wikimedia Commons (see the teacher's notes). Voice: Piper.")
S.append(scene("At home", P("/home/claude/work/kitchen.jpg"),
 "School is finished. Now you are at home, in the kitchen. Listen and repeat the words. Then say good night!",
 [say("the kitchen", -20, 12, "The kitchen. We cook in the kitchen."),
  say("the fridge", -70, 4, "The fridge. The milk is in the fridge."),
  say("the table", 8, -28, "The table. We eat at the table."),
  say("a chair", -38, -26, "A chair. Sit down, please."),
  say("milk", -95, -10, "Milk. I drink milk for breakfast."),
  say("Good night!", 120, 0, "Good night! Sleep well."),
  say("See you tomorrow!", 150, -6, "See you tomorrow! Goodbye!"),
  fnd("Find the flowers.", 2, -6, "Here are the flowers. They are yellow.", 40, 6, 11),
  inf("Credits", cred, -160, -16)]))
S[4]["introS"] = "This is the kitchen. Listen and repeat."
C = {"id": uid(), "title": "Hello! Words for school and home", "matiere": "Anglais", "niveau": "6e", "voix": "en-GB",
     "objectif": "Listen, look and repeat! Learn English words for school and for every day.", "scenes": S}
# simplifié : explications courtes
for s in S:
    for h in s["hotspots"]:
        if h["type"] == "say" and h.get("explanation") and "explanationS" not in h: h["explanationS"] = h["question"]
        if h["type"] == "info" and "textS" not in h and h["title"] != "Credits": h["textS"] = h["text"].split(". ")[0].rstrip(".") + "."
if errors: print("\n".join(errors)); sys.exit(1)
json.dump(C, open("/home/claude/eng6/cours.json", "w"), ensure_ascii=False)
print(len(S), "scènes", sum(len(s["hotspots"]) for s in S), "points", sum(1 for s in S for h in s["hotspots"] if h["type"] == "say"), "répétitions")
