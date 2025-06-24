import tkinter as tk
from tkinter import *
from PIL import Image as PILImage, ImageTk
from pathlib import Path
import numpy as np
from joblib import load
import threading
import os

# === Serial Setup ===
import serial
import time

arduino_port = "COM5"  # Your Arduino COM port
baud_rate = 9600

arduino_port = "COM5"  # Replace with your port
baud_rate = 9600
num_entries = 2  # Set the number of entries you want to read

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to Arduino on {arduino_port}")
    time.sleep(2)

    for _ in range(num_entries):
        line = ser.readline().decode("utf-8", errors='ignore').strip()
        if line:
            try:
                temp, hum, soil, air = map(float, line.split(","))
                print(f"Temperature: {temp}°C | Humidity: {hum}% | Soil Moisture: {soil} | Air Quality: {air}")
            except ValueError:
                print("Waiting for valid data...")

except serial.SerialException:
    print("Could not connect to Arduino. Check port and cable.")

# === Resource Paths ===
def get_base_path():
    return Path(__file__).parent

def get_resource_path(relative_path):
    return get_base_path() / "resources" / relative_path

# === Load Model ===
model = load(get_resource_path("data/fruit_model.pkl"))

# === Fruit Info (extendable) ===
fruit_info = {
    "Guava": {
    "name": "Guava",
    "fruit_family": "Myrtaceae",
    "scientific_name": "Psidium guajava",
    "sunlight_requirement": "Full Sun",
    "temperature": "23°C to 28°C",
    "humidity": "60% to 80%",
    "image": get_resource_path("assets/guava.png"),
    "description": """Guava is a tropical fruit known for its sweet, aromatic flavor and high vitamin C content. It has green or yellow skin and pink or white flesh. Guava trees are hardy, thrive in well-drained soils, and are valued for both fresh eating and juice production.
    **How to Grow:**
    1. Prepare the site: Ensure well-drained soil and remove weeds.
    2. Plant: Dig a hole twice the size of the root ball and plant the guava sapling.
    3. Water: Water thoroughly after planting and mulch to retain moisture.
    4. Sunlight & Care: Provide full sunlight, water regularly, especially during dry spells, and fertilize lightly during the growing season."""
},

"Apple": {
    "name": "Apple",
    "fruit_family": "Rosaceae",
    "scientific_name": "Malus domestica",
    "sunlight_requirement": "Full Sun",
    "temperature": "15°C to 24°C",
    "humidity": "50% to 70%",
    "image": get_resource_path("assets/apple.png"),
    "description": """Apple is a crisp, juicy fruit with red, green, or yellow skin and white flesh. Apples are enjoyed fresh or in various dishes, and are known for their sweet to tart flavor. They grow best in temperate climates with well-drained, slightly acidic soil.
    **How to Grow:**
    1. Location: Choose a sunny spot with slightly acidic, well-drained loam.
    2. Plant: Dig a wide hole and plant the apple sapling at the same depth as in the nursery.
    3. Water & Mulch: Water deeply after planting and mulch around the base to retain moisture and suppress weeds.
    4. Pruning: Prune annually to shape the tree and encourage fruiting. Water regularly, especially during flowering and fruit development."""
},

"Blueberry": {
    "name": "Blueberry",
    "fruit_family": "Ericaceae",
    "scientific_name": "Vaccinium corymbosum",
    "sunlight_requirement": "Full Sun",
    "temperature": "13°C to 21°C",
    "humidity": "60% to 70%",
    "image": get_resource_path("assets/blueberry.png"),
    "description": """Blueberry is a small, round berry with a deep blue color and sweet-tangy flavor. It is rich in antioxidants and dietary fiber. Blueberries thrive in acidic, organic-rich soils and are popular in desserts, cereals, and smoothies.
    **How to Grow:**
    1. Soil Preparation: Prepare a raised bed with acidic, organic-rich soil.
    2. Plant: Plant blueberry bushes 4–5 feet apart.
    3. Water & Mulch: Water thoroughly after planting and keep soil consistently moist; mulch with pine needles or bark to maintain acidity.
    4. Fertilize & Prune: Fertilize with an acid-loving plant fertilizer in spring. Prune in late winter to remove weak branches and promote growth."""
},

"Grape": {
    "name": "Grape",
    "fruit_family": "Vitaceae",
    "scientific_name": "Vitis vinifera",
    "sunlight_requirement": "Full Sun",
    "temperature": "15°C to 30°C",
    "humidity": "50% to 60%",
    "image": get_resource_path("assets/grape.png"),
    "description": """Grape is a small, juicy fruit that grows in clusters and comes in green, red, or purple varieties. Grapes are enjoyed fresh, dried as raisins, or used for juice and wine. They grow best in well-drained, sandy or loamy soils.
    **How to Grow:**
    1. Support: Install sturdy trellises or supports before planting.
    2. Plant: Plant grapevines in rows, spacing them 6–8 feet apart.
    3. Water & Mulch: Water well after planting and mulch to retain moisture.
    4. Pruning & Fertilize: Prune annually to encourage healthy vines and fruit production. Water regularly during dry periods, and fertilize lightly in early spring."""
},

"Banana": {
    "name": "Banana",
    "fruit_family": "Musaceae",
    "scientific_name": "Musa acuminata",
    "sunlight_requirement": "Full Sun",
    "temperature": "26°C to 30°C",
    "humidity": "70% to 90%",
    "image": get_resource_path("assets/banana.png"),
    "description": """Banana is a long, curved fruit with a yellow peel and soft, sweet flesh. Bananas are rich in potassium and grow rapidly in warm, humid climates with fertile, well-drained soil.
    **How to Grow:**
    1. Location: Select a sunny, sheltered spot with rich, well-drained soil.
    2. Plant: Dig a deep hole and plant the banana sucker upright.
    3. Water & Mulch: Water generously after planting and keep soil moist; mulch thickly to retain moisture and add nutrients.
    4. Fertilize & Suckers: Fertilize monthly with compost or manure. Remove suckers to allow the main plant to thrive."""
},

"Kiwi": {
    "name": "Kiwi",
    "fruit_family": "Actinidiaceae",
    "scientific_name": "Actinidia deliciosa",
    "sunlight_requirement": "Full Sun to Partial Shade",
    "temperature": "14°C to 24°C",
    "humidity": "60% to 80%",
    "image": get_resource_path("assets/kiwi.png"),
    "description": """Kiwi is a small, oval fruit with fuzzy brown skin and bright green flesh speckled with tiny black seeds. It has a sweet-tart flavor and is high in vitamin C. Kiwi vines need deep, fertile, well-drained soils and regular watering.
    **How to Grow:**
    1. Support: Erect a strong trellis for vine support.
    2. Plant: Plant male and female kiwi plants near each other for pollination, spacing vines about 10 feet apart.
    3. Water & Mulch: Water regularly and mulch to keep roots cool.
    4. Pruning & Fertilize: Prune annually to control growth and improve fruiting. Fertilize in spring and summer."""
},

"Mango": {
    "name": "Mango",
    "fruit_family": "Anacardiaceae",
    "scientific_name": "Mangifera indica",
    "sunlight_requirement": "Full Sun",
    "temperature": "24°C to 30°C",
    "humidity": "50% to 60%",
    "image": get_resource_path("assets/mango.png"),
    "description": """Mango is a juicy tropical fruit with sweet, aromatic orange-yellow flesh. Mango trees thrive in deep, well-drained sandy loam soils and are prized for their delicious fruit, eaten fresh or used in smoothies and desserts.
    **How to Grow:**
    1. Location & Plant: Dig a deep, wide hole in a sunny area and plant the mango sapling.
    2. Water & Mulch: Water deeply after planting and mulch to retain moisture.
    3. Watering & Fertilizing: Water regularly during dry periods, but avoid waterlogging. Fertilize with a balanced fertilizer during the growing season.
    4. Pruning: Prune lightly to shape the tree and remove dead branches."""
},

"Pomegranate": {
    "name": "Pomegranate",
    "fruit_family": "Lythraceae",
    "scientific_name": "Punica granatum",
    "sunlight_requirement": "Full Sun",
    "temperature": "20°C to 35°C",
    "humidity": "40% to 60%",
    "image": get_resource_path("assets/pomegranate.png"),
    "description": """Pomegranate is a round fruit with thick reddish skin and juicy, ruby-red seeds. It is rich in antioxidants and grows best in loamy or sandy soils with good drainage.
    **How to Grow:**
    1. Soil Prep & Plant: Prepare the soil by loosening and removing weeds. Plant pomegranate saplings in full sun, spacing them 10–12 feet apart.
    2. Water & Mulch: Water deeply after planting and mulch to conserve moisture.
    3. Watering & Pruning: Water regularly, especially during flowering and fruiting. Prune annually to remove dead wood and shape the plant.
    4. Fertilize: Fertilize lightly in early spring."""
},

"Pear": {
    "name": "Pear",
    "fruit_family": "Rosaceae",
    "scientific_name": "Pyrus communis",
    "sunlight_requirement": "Full Sun",
    "temperature": "16°C to 24°C",
    "humidity": "50% to 70%",
    "image": get_resource_path("assets/pear.png"),
    "description": """Pear is a bell-shaped fruit with green, yellow, or red skin and soft, juicy flesh. Pears have a mild, sweet flavor and grow well in deep, fertile, well-drained loamy soils.
    **How to Grow:**
    1. Location & Plant: Choose a sunny location and dig a hole twice as wide as the root ball. Plant the sapling at the same depth as in the nursery.
    2. Water & Mulch: Water thoroughly and mulch to retain moisture.
    3. Pruning & Fertilize: Prune annually to encourage healthy growth. Water regularly, especially during dry spells, and fertilize in early spring for optimal fruiting."""
},

"Lemon": {
    "name": "Lemon",
    "fruit_family": "Rutaceae",
    "scientific_name": "Citrus limon",
    "sunlight_requirement": "Full Sun",
    "temperature": "21°C to 28°C",
    "humidity": "50% to 70%",
    "image": get_resource_path("assets/lemon.png"),
    "description": """Lemon is a bright yellow citrus fruit with a tart, tangy flavor. Lemons are valued for their high vitamin C content and are widely used in beverages and cooking. They grow best in well-drained, slightly acidic soils.
    **How to Grow:**
    1. Location & Plant: Plant the sapling in a sunny spot with good air circulation.
    2. Water & Mulch: Water deeply after planting and mulch to conserve moisture. Water regularly, keeping the soil moist but not soggy.
    3. Fertilize & Prune: Fertilize with citrus fertilizer in spring and summer. Prune to maintain shape and remove dead branches.
    4. Protection: Protect young plants from frost if necessary."""
},

"Dragonfruit": {
    "name": "Dragonfruit",
    "fruit_family": "Cactaceae",
    "scientific_name": "Hylocereus undatus",
    "sunlight_requirement": "Full Sun",
    "temperature": "18°C to 26°C",
    "humidity": "50% to 70%",
    "image": get_resource_path("assets/dragonfruit.png"),
    "description": """Dragonfruit, or pitaya, has vibrant pink or yellow skin and white or red flesh dotted with tiny black seeds. It is mildly sweet and grows best in sandy, well-drained soils in warm climates.
    **How to Grow:**
    1. Support: Build a vertical support or trellis for the climbing cactus.
    2. Plant: Plant cuttings or young plants at the base of the support.
    3. Water & Mulch: Water moderately, allowing soil to dry slightly between waterings. Mulch to retain moisture and suppress weeds.
    4. Fertilize & Pruning: Fertilize monthly during the growing season. Prune to control growth and encourage flowering."""
},

"Jamun": {
    "name": "Jamun",
    "fruit_family": "Myrtaceae",
    "scientific_name": "Syzygium cumini",
    "sunlight_requirement": "Full Sun",
    "temperature": "20°C to 32°C",
    "humidity": "60% to 80%",
    "image": get_resource_path("assets/jamun.png"),
    "description": """Jamun, or Indian blackberry, is a small, oval, deep purple fruit with a sweet and slightly astringent taste. It is often eaten fresh or used in juices and grows well in deep, well-drained loamy soils.
    **How to Grow:**
    1. Location & Plant: Select a sunny spot and dig a large planting hole. Plant the sapling upright and fill with soil.
    2. Water & Mulch: Water thoroughly and mulch to retain moisture. Water regularly, especially in the first two years.
    3. Fertilize & Pruning: Fertilize annually with organic compost. Prune lightly to remove dead wood and shape the tree."""
},

"Cherries": {
    "name": "Cherries",
    "fruit_family": "Rosaceae",
    "scientific_name": "Prunus avium",
    "sunlight_requirement": "Full Sun",
    "temperature": "16°C to 24°C",
    "humidity": "60% to 70%",
    "image": get_resource_path("assets/cherries.png"),
    "description": """Cherries are small, round fruits with glossy red or dark purple skin and juicy flesh. They are enjoyed fresh or in desserts and thrive in well-drained, sandy loam soils.
    **How to Grow:**
    1. Location & Plant: Plant cherry saplings in a sunny, sheltered location. Space trees about 20 feet apart for good air flow.
    2. Water & Mulch: Water deeply after planting and mulch to conserve moisture.
    3. Pruning & Fertilize: Prune annually to encourage fruiting and remove weak branches. Water regularly, especially during dry periods, and fertilize in early spring."""
},


"Strawberry": {
    "name": "Strawberry",
    "fruit_family": "Rosaceae",
    "scientific_name": "Fragaria × ananassa",
    "sunlight_requirement": "Full Sun",
    "temperature": "15°C to 26°C",
    "humidity": "60% to 80%",
    "image": get_resource_path("assets/strawberry.png"),
    "description": """Strawberry is a bright red, heart-shaped berry with a sweet, juicy flavor. Strawberries thrive in well-drained, sandy loam soils and are enjoyed fresh, in desserts, and jams.
    **How to Grow:**
    1. Soil Prep & Plant: Prepare raised beds or rows with loose, fertile soil. Plant strawberry runners 12–18 inches apart.
    2. Water & Mulch: Water thoroughly after planting and mulch with straw. Water regularly to keep soil moist.
    3. Fertilize & Runners: Fertilize lightly during the growing season. Remove runners to focus energy on fruit production."""
},

"Mousambi": {
    "name": "Mousambi",
    "fruit_family": "Rutaceae",
    "scientific_name": "Citrus limetta",
    "sunlight_requirement": "Full Sun",
    "temperature": "20°C to 28°C",
    "humidity": "50% to 70%",
    "image": get_resource_path("assets/mousambi.png"),
    "description": """Mousambi, or sweet lime, is a citrus fruit with greenish-yellow skin and pale, juicy, sweet flesh. It is refreshing and commonly used for juice. Mousambi trees grow best in well-drained, fertile soils.
    **How to Grow:**
    1. Location & Plant: Plant the sapling in a sunny location with good drainage.
    2. Water & Mulch: Water deeply after planting and mulch to retain moisture. Water regularly, especially during dry periods.
    3. Fertilize & Pruning: Fertilize with citrus fertilizer in spring and summer. Prune to maintain shape and remove dead or diseased wood.
    4. Protection: Protect young trees from frost and strong winds."""
}




}
welcome_root = Tk()
# === App State ===
Temperature = StringVar()
Humidity = StringVar()
Sun = StringVar()
Moisture = StringVar()
AirQuality = StringVar()

# === Main GUI Windows ===
def show_result():
    temp = int(entry_1.get())
    hum = int(entry_2.get())
    sun = int(entry_3.get())
    moist = int(entry_4.get())
    aq = int(entry_5.get())

    sun = 50 if sun == 0 else 100
    inputs = np.array([[temp, hum, sun, moist, aq]])
    fruit = model.predict(inputs)[0].strip().title()

    print("Predicted fruit:", fruit)

    # Result Window
    result = Toplevel()
    result.title("AgriVision | Prediction")
    result.geometry("750x600")
    result.configure(bg="lightgreen")

    Label(result, text="Prediction Result", font=("Arial", 16, "bold"), bg="lightgreen").place(x=20, y=20)
    Label(result, text=f"Fruit Name: {fruit}", font=("Arial", 12), bg="lightgreen").place(x=20, y=60)

    # Fruit Info Lookup
    info = fruit_info.get(fruit, {})
    image_path = info.get("image")
    desc = info.get("description", "Description not available.")
    family = info.get("fruit_family", "N/A")
    sci_name = info.get("scientific_name", "N/A")
    sunlight = info.get("sunlight_requirement", "N/A")
    temp_range = info.get("temperature", "N/A")
    humidity = info.get("humidity", "N/A")

    # Display Image
    if image_path and os.path.exists(image_path):
        fruit_img = PILImage.open(image_path).resize((220, 220))
        fruit_img = ImageTk.PhotoImage(fruit_img)
        Label(result, image=fruit_img, bg="lightgreen").place(x=500, y=30)
        result.image = fruit_img  # prevent GC

    # Display Additional Info
    Label(result, text=f"Family: {family}", font=("Arial", 11), bg="lightgreen").place(x=20, y=90)
    Label(result, text=f"Scientific Name: {sci_name}", font=("Arial", 11), bg="lightgreen").place(x=20, y=115)
    Label(result, text=f"Sunlight: {sunlight}", font=("Arial", 11), bg="lightgreen").place(x=20, y=140)
    Label(result, text=f"Temperature: {temp_range}", font=("Arial", 11), bg="lightgreen").place(x=20, y=165)
    Label(result, text=f"Humidity: {humidity}", font=("Arial", 11), bg="lightgreen").place(x=20, y=190)

    # Description
    Label(result, text="Description & Growing Tips", font=("Arial", 14, "bold"), bg="lightgreen").place(x=20, y=230)
    desc_label = Label(result, text=desc, font=("Arial", 10), wraplength=700, justify=LEFT, bg="lightgreen")
    desc_label.place(x=20, y=260)


def open_sensor_input():
    welcome_root.destroy()
    global entry_1, entry_2, entry_3, entry_4, entry_5

    input_win = Tk()
    input_win.title("AgriVision | Sensor Input")
    input_win.geometry("650x400")
    input_win.configure(bg="white")

    Label(input_win, text="Enter Sensor Values", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    # Form Fields
    form_frame = Frame(input_win, bg="white")
    form_frame.pack(pady=20)

    labels = ["Temperature (°C)", "Humidity (%)", "Sunlight", "Soil Moisture", "Air Quality"]
    vars_ = [Temperature, Humidity, Sun, Moisture, AirQuality]
    entries = []

    for i, label in enumerate(labels):
        Label(form_frame, text=label + ":", font=("Arial", 12), bg="white").grid(row=i, column=0, sticky=W, padx=10, pady=5)
        entry = Entry(form_frame, textvariable=vars_[i], font=("Arial", 12), width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    entry_1, entry_2, entry_3, entry_4, entry_5 = entries

    Button(input_win, text="Predict Fruit", font=("Arial", 12), bg="green", fg="white",
           command=lambda: threading.Thread(target=show_result).start()).pack(pady=20)

    input_win.mainloop()

# === Welcome Window ===

welcome_root.title("AgriVision")
welcome_root.geometry("500x400")
welcome_root.configure(bg="white")

# Logo
logo_path = get_resource_path("assets/logo.png")
logo_img = PILImage.open(logo_path).resize((200, 200))
logo_photo = ImageTk.PhotoImage(logo_img)
Label(welcome_root, image=logo_photo, bg="white").pack(pady=10)

# Text
Label(welcome_root, text="WELCOME TO AGRIVISION", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
Label(welcome_root, text="Cultivate your passion for plants with\nthe knowledge and tools provided by AgriVision.",
      font=("Arial", 12), bg="white", justify=CENTER).pack(pady=5)

# Start Button
Button(welcome_root, text="Let's start", font=("Arial", 12), bg="green", fg="white",
       command=open_sensor_input).pack(pady=20)

welcome_root.mainloop()
