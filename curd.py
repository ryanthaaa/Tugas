import turtle

# ---------- Config ----------
WIDTH, HEIGHT = 800, 600
BG_COLOR = "white"
BUTTON_COLOR = "#8FB9FF"
BUTTON_HOVER = "#6EA0E6"
ITEM_FILL = "#FFF2CC"
ITEM_BORDER = "#E6B800"
SELECT_COLOR = "#FFB3B3"

FONT = ("Arial", 12, "normal")
TITLE_FONT = ("Arial", 16, "bold")

# UI layout
TOP_MARGIN = 40
BUTTON_W, BUTTON_H = 140, 32
BUTTON_GAP = 20
BUTTON_START_X = - (1.5 * BUTTON_W + 1.5 * BUTTON_GAP)

ITEM_START_Y = 120
ITEM_BOX_W = 220
ITEM_BOX_H = 40
ITEM_GAP = 12
ITEMS_PER_COL = 5
ITEM_COL_GAP = 260

# ---------- Data model ----------
items = []  # list of dicts: {'label': str, 'id': int}
next_id = 1

selected_item_index = None

# ---------- Turtle setup ----------
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("CRUD Visualizer with Turtle")
screen.bgcolor(BG_COLOR)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.penup()

# Track mouse position for hover effect
mouse_x, mouse_y = 0, 0

# ---------- Buttons definition ----------
buttons = []

def make_button(x, y, text, callback):
    b = {"x": x, "y": y, "w": BUTTON_W, "h": BUTTON_H, "text": text, "cb": callback}
    buttons.append(b)
    return b

def draw_rounded_rect(x, y, w, h, r=8):
    pen.goto(x + r, y)
    pen.pendown()
    for _ in range(2):
        pen.forward(w - 2*r)
        pen.circle(r, 90)
        pen.forward(h - 2*r)
        pen.circle(r, 90)
    pen.penup()

def draw_buttons():
    for b in buttons:
        x, y, w, h = b["x"], b["y"], b["w"], b["h"]
        # hover?
        hover = (x <= mouse_x <= x+w) and (y-h <= mouse_y <= y)
        color = BUTTON_HOVER if hover else BUTTON_COLOR
        pen.goto(x, y)
        pen.color("black", color)
        pen.setheading(0)
        pen.begin_fill()
        draw_rounded_rect(x, y, w, h)
        pen.end_fill()
        # text
        pen.goto(x + w/2, y - h/2 - 6)
        pen.write(b["text"], align="center", font=FONT)

# ---------- Items drawing ----------
def get_item_position(index):
    # two-column layout
    col = index // ITEMS_PER_COL
    row = index % ITEMS_PER_COL
    x = -WIDTH//2 + 80 + col * ITEM_COL_GAP
    y = ITEM_START_Y - row * (ITEM_BOX_H + ITEM_GAP)
    return x, y

def draw_items():
    pen.color("black")
    for i, it in enumerate(items):
        x, y = get_item_position(i)
        w, h = ITEM_BOX_W, ITEM_BOX_H
        # determine fill depending on selected
        if selected_item_index == i:
            fill = SELECT_COLOR
        else:
            fill = ITEM_FILL
        pen.goto(x, y)
        pen.color("black", ITEM_BORDER)
        pen.begin_fill()
        pen.goto(x, y)
        pen.pendown()
        for _ in range(2):
            pen.forward(w)
            pen.right(90)
            pen.forward(h)
            pen.right(90)
        pen.penup()
        pen.end_fill()
        pen.goto(x + 8, y - 26)
        pen.color("black")
        pen.write(f"{it['id']}. {it['label']}", font=FONT)

# ---------- CRUD operations ----------
def create_item():
    global next_id
    label = screen.textinput("Create", "Masukkan nama item baru:")
    if label is None or label.strip() == "":
        return
    items.append({"label": label.strip(), "id": next_id})
    next_id += 1
    redraw()

def read_item():
    global selected_item_index
    if selected_item_index is None:
        screen.textinput("Read", "Tidak ada item terpilih. Klik salah satu item lalu pilih Read. Tekan OK untuk lanjut.")
        return
    it = items[selected_item_index]
    screen.textinput("Read", f"Item ID {it['id']} — Label: {it['label']}\n(Press OK to close)")

def update_item():
    global selected_item_index
    if selected_item_index is None:
        screen.textinput("Update", "Tidak ada item terpilih. Klik salah satu item lalu pilih Update. Tekan OK untuk lanjut.")
        return
    it = items[selected_item_index]
    new_label = screen.textinput("Update", f"Ubah label untuk item {it['id']} (sekarang: {it['label']}):")
    if new_label is None or new_label.strip() == "":
        return
    items[selected_item_index]['label'] = new_label.strip()
    redraw()

def delete_item():
    global selected_item_index
    if selected_item_index is None:
        screen.textinput("Delete", "Tidak ada item terpilih. Klik salah satu item lalu pilih Delete. Tekan OK untuk lanjut.")
        return
    it = items.pop(selected_item_index)
    # reset selection
    selected_item_index = None
    screen.textinput("Delete", f"Item ID {it['id']} dihapus. Tekan OK.")
    redraw()

# ---------- Event handlers ----------
def on_click(x, y):
    global selected_item_index
    # check buttons
    for b in buttons:
        bx, by, bw, bh = b["x"], b["y"], b["w"], b["h"]
        if bx <= x <= bx + bw and by - bh <= y <= by:
            # call callback
            b["cb"]()
            return
    # check items
    found = False
    for i in range(len(items)):
        ix, iy = get_item_position(i)
        if ix <= x <= ix + ITEM_BOX_W and iy - ITEM_BOX_H <= y <= iy:
            selected_item_index = i
            found = True
            redraw()
            break
    if not found:
        # click outside -> deselect
        selected_item_index = None
        redraw()

def on_move(x, y):
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y
    redraw()

# ---------- Draw titles and UI ----------
def draw_title():
    pen.goto(0, HEIGHT//2 - 40)
    pen.write("Visual CRUD (Create Read Update Delete) - Turtle", align="center", font=TITLE_FONT)
    pen.goto(0, HEIGHT//2 - 62)
    pen.write("Klik tombol di atas, klik item untuk memilih", align="center", font=FONT)

def redraw():
    screen.tracer(0)
    pen.clear()
    draw_title()
    draw_buttons()
    draw_items()
    # footer / help
    pen.goto(-WIDTH//2 + 20, -HEIGHT//2 + 30)
    pen.write("Hints: Click an item box to select. Use buttons to perform CRUD. Create uses text input.", font=("Arial", 10, "normal"))
    screen.tracer(1)

# ---------- Setup buttons and handlers ----------
make_button(BUTTON_START_X, HEIGHT//2 - TOP_MARGIN, "Create", create_item)
make_button(BUTTON_START_X + (BUTTON_W + BUTTON_GAP), HEIGHT//2 - TOP_MARGIN, "Read", read_item)
make_button(BUTTON_START_X + 2*(BUTTON_W + BUTTON_GAP), HEIGHT//2 - TOP_MARGIN, "Update", update_item)
make_button(BUTTON_START_X + 3*(BUTTON_W + BUTTON_GAP), HEIGHT//2 - TOP_MARGIN, "Delete", delete_item)

# sample initial items
items.extend([{"label": "Item A", "id": 1}, {"label": "Item B", "id": 2}, {"label": "Item C", "id": 3}])
next_id = 4

# bind events
screen.onclick(on_click)
screen.onscreenclick(on_click)
screen.listen()
screen.getcanvas().bind("<Motion>", lambda e: on_move(e.x - screen.window_width()//2, screen.window_height()//2 - e.y))

# initial draw
redraw()

# keep window open
turtle.done()

