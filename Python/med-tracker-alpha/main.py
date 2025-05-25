import sqlite3
import subprocess
from plyer import notification
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from datetime import datetime
def notify(title, message):
    if platform == "linux":
        subprocess.run(["notify-send", "-a", "MedTracker", title, message])
    elif platform == "android":
        from plyer import notification
        notification.notify(title=title, message=message, timeout=5)



# Load UI.
Builder.load_file("ui.kv")

# DB Helper.
def init_db():
    conn = sqlite3.connect("meds.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            med_time TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Main widget logic
class MedForm(BoxLayout):
    med_name = StringProperty("")
    dosage = StringProperty("")
    med_time = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.on_key_down)
        Clock.schedule_interval(self.check_med_time, 60)  # Check every minute
        Clock.schedule_interval(lambda dt: self.update_med_list(), 5)  # Update every 5 seconds
        
    def check_med_time(self, dt):
        now = datetime.now().strftime("%H:%M")
        conn = sqlite3.connect("meds.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, dosage, med_time, stock FROM medications")
        for med_id, name, dosage, time_str, stock in cursor.fetchall():
            if now == time_str:
                if stock > 0:
                    notify("Time for Medication", f"{name} ({dosage}) - {stock} left.")
                    cursor.execute(
                        "UPDATE medications SET stock = stock - 1 WHERE id = ?",
                        (med_id,)
                )
                else:
                    notify("Out of Stock", f"{name} is out of stock!")
        conn.commit()
        conn.close()

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        focused = self.get_focused_textinput()

        if key == 9:
            self.focus_next_textinput(focused)
            return True
        
        elif key == 13:
            if self.med_name and self.dosage and self.med_time:
                self.add_medication()
            else:  
                notify(
                    title="Error",
                    message="Please fill in all fields.",
                )
            return True
        
        return False
    
    def get_focused_textinput(self):
        for child in [self.ids.med_name_input, self.ids.dosage_input, self.ids.med_time_input]:
            if isinstance(child, TextInput) and child.focus:
                return child
        return None
    
    def focus_next_textinput(self, current):
        inputs = [self.ids.med_name_input, self.ids.dosage_input, self.ids.med_time_input]
        if current in inputs:
            idx = inputs.index(current)
            next_idx = (idx + 1) % len(inputs)
            inputs[next_idx].focus = True
        else:
            inputs[0].focus = True

    def add_medication(self):
        conn = sqlite3.connect("meds.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO medications (name, dosage, med_time)
            VALUES (?, ?, ?)
        ''', (self.med_name, self.dosage, self.med_time))
        conn.commit()
        conn.close()

        # The notification part.

        notify(
            title="Medication Added.",
            message=f"{self.med_name} ({self.dosage}) at {self.med_time} saved.",
        )


        print(f"Added {self.med_name} ({self.dosage}) to the database.")
        self.med_name = ""
        self.dosage = ""
        self.med_time = ""

    def add_stock(self):
        if not self.med_name:
            notify(
                title="Error",
                message="Please enter a medication name.",
            )
            self.update_med_list()
            return
        conn = sqlite3.connect("meds.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE medications SET stock = stock + 1 WHERE name = ?", (self.med_name,))
        if cursor.rowcount == 0:
            notify(
                "Error", f"No medication named '{self.med_name}' found.")
        else:
            notify(
                "Stock Updated",
                f"Added stock for {self.med_name}.",
            )
        self.update_med_list()
        conn.commit()
        conn.close()
    
    def deduct_stock(self):
        if not self.med_name:
            notify("Error", "Please enter a medication name.")
            return
        conn = sqlite3.connect("meds.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE medications SET stock = stock - 1 WHERE name = ? AND stock > 0", (self.med_name,))
        if cursor.rowcount == 0:
            notify(
                "Error", f"No medication named '{self.med_name}' found or out of stock.")
        else:
            notify(
                "Stock Updated",
                f"Deducted stock for {self.med_name}.",
            )
        self.update_med_list()
        conn.commit()
        conn.close()

    def on_kv_post(self, base_widget):
        self.update_med_list()

    def update_med_list(self):
        conn = sqlite3.connect("meds.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, dosage, med_time, stock FROM medications")
        meds = cursor.fetchall()
        conn.close()
        self.ids.meds_view.data = [
            {
                "name": name,
                "dosage": dosage,
                "med_time": med_time,
                "stock": stock
            }
            for name, dosage, med_time, stock in meds
        ]
        
class MedApp(App):
    def build(self):
        init_db()
        return MedForm()
    
if __name__ == "__main__":
    MedApp().run()