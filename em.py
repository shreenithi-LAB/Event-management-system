import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import re
from datetime import date

# Sample in-memory event storage
events = []

# Function Definitions
def add_event():
    name = entry_name.get()
    date_val = entry_date.get()
    time = entry_time.get()
    location = entry_location.get()
    attendees = entry_attendees.get()
    category = category_var.get()
    description = text_description.get("1.0", tk.END).strip()

    if not name or not date_val or not time or not location or not attendees:
        messagebox.showwarning("Input Error", "Please fill all required fields.")
        return

    if not re.match(r"\d{4}-\d{2}-\d{2}", date_val):
        messagebox.showerror("Date Format Error", "Use YYYY-MM-DD format.")
        return

    if not re.match(r"\d{2}:\d{2}$", time):
        messagebox.showerror("Time Format Error", "Use HH:MM format.")
        return

    try:
        attendees = int(attendees)
    except ValueError:
        messagebox.showerror("Attendees Error", "Attendees must be a number.")
        return

    event = {
        "name": name,
        "date": date_val,
        "time": time,
        "location": location,
        "attendees": attendees,
        "category": category,
        "description": description
    }
    events.append(event)
    view_events()
    clear_form()
    messagebox.showinfo("Success", "Event added successfully!")

def update_event():
    selected = listbox_events.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select an event to update.")
        return
    index = selected[0]
    name = entry_name.get()
    date_val = entry_date.get()
    time = entry_time.get()
    location = entry_location.get()
    attendees = entry_attendees.get()
    category = category_var.get()
    description = text_description.get("1.0", tk.END).strip()

    if not name or not date_val or not time or not location or not attendees:
        messagebox.showwarning("Input Error", "Please fill all required fields.")
        return

    if not re.match(r"\d{4}-\d{2}-\d{2}", date_val):
        messagebox.showerror("Date Format Error", "Use YYYY-MM-DD format.")
        return

    if not re.match(r"\d{2}:\d{2}$", time):
        messagebox.showerror("Time Format Error", "Use HH:MM format.")
        return

    try:
        attendees = int(attendees)
    except ValueError:
        messagebox.showerror("Attendees Error", "Attendees must be a number.")
        return

    events[index] = {
        "name": name,
        "date": date_val,
        "time": time,
        "location": location,
        "attendees": attendees,
        "category": category,
        "description": description
    }
    view_events()
    messagebox.showinfo("Success", "Event updated successfully!")

def delete_event():
    selected = listbox_events.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select an event to delete.")
        return
    index = selected[0]
    events.pop(index)
    view_events()
    clear_form()
    messagebox.showinfo("Deleted", "Event deleted successfully.")

def clear_all_events():
    if messagebox.askyesno("Clear All", "Are you sure you want to clear all events?"):
        events.clear()
        view_events()
        clear_form()

def clear_form():
    entry_name.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_date.insert(0, date.today().strftime("%Y-%m-%d"))
    entry_time.delete(0, tk.END)
    entry_location.delete(0, tk.END)
    entry_attendees.delete(0, tk.END)
    category_var.set("Conference")
    text_description.delete("1.0", tk.END)

def view_events():
    listbox_events.delete(0, tk.END)
    for i, event in enumerate(events):
        display = f"{i+1}. {event['name']} | {event['date']} {event['time']} | {event['location']} | {event['category']} | {event['attendees']} Attendees"
        listbox_events.insert(tk.END, display)
    label_count.config(text=f"Total Events: {len(events)}")

def show_event_popup(event=None):
    selected = listbox_events.curselection()
    if not selected:
        return
    index = selected[0]
    e = events[index]

    detail_window = tk.Toplevel(root)
    detail_window.title("Event Details")
    detail_window.geometry("400x300")
    detail_window.configure(bg="#ffffff")

    tk.Label(detail_window, text="📌 Event Details", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(pady=10)

    details = f"""
Name: {e['name']}
Date: {e['date']}
Time: {e['time']}
Location: {e['location']}
Attendees: {e['attendees']}
Category: {e['category']}
Description:
{e['description']}
    """

    tk.Label(detail_window, text=details, justify="left", bg="#ffffff", font=("Segoe UI", 10)).pack(padx=20)

def search_event():
    query = entry_search.get().lower()
    listbox_events.delete(0, tk.END)
    count = 0
    for i, event in enumerate(events):
        if (query in event["name"].lower() or
            query in event["location"].lower() or
            query in event["category"].lower()):
            display = f"{i+1}. {event['name']} | {event['date']} {event['time']} | {event['location']} | {event['category']} | {event['attendees']} Attendees"
            listbox_events.insert(tk.END, display)
            count += 1
    label_count.config(text=f"Search Results: {count}")

def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Time", "Location", "Attendees", "Category", "Description"])
        for event in events:
            writer.writerow([event["name"], event["date"], event["time"],
                             event["location"], event["attendees"],
                             event["category"], event["description"]])
    messagebox.showinfo("Exported", f"Events exported to {file_path}")

# Hover effect functions for buttons
def on_enter(e):
    e.widget['background'] = '#00796b'
    e.widget['foreground'] = 'white'

def on_leave(e):
    e.widget['background'] = '#ffffff'
    e.widget['foreground'] = 'black'

# GUI Setup
root = tk.Tk()
root.title("Event Management System")
root.geometry("950x950")
root.resizable(False, False)

canvas = tk.Canvas(root, bg="#e0f7fa")
canvas.pack(fill="both", expand=True)

# Gradient-like header banner
header_frame = tk.Frame(canvas, bg="#00acc1", height=60)
header_frame.pack(fill="x")

header_label = tk.Label(header_frame, text="🌟 Event Management System 🌟",
                        font=("Segoe UI", 20, "bold"), fg="#ffffff", bg="#00acc1")
header_label.pack(pady=10)

frame_main = tk.Frame(canvas, bg="#e0f7fa")
frame_main.place(relwidth=1, relheight=1)

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.configure("TLabel", background="#e0f7fa", font=("Segoe UI", 10))
style.configure("TLabelframe", background="#b2ebf2", font=("Segoe UI", 11, "bold"))
style.configure("TEntry", padding=4)

notebook = ttk.Notebook(frame_main)
notebook.pack(expand=True, fill='both', padx=20, pady=20)

# Event Form Tab
tab_form = ttk.Frame(notebook)
notebook.add(tab_form, text='➕ Add / Update Event')

frame_form = ttk.LabelFrame(tab_form, text="📝 Event Details", padding=10)
frame_form.pack(padx=20, pady=20, fill="x")

fields = [
    ("Event Name", "entry_name"),
    ("Event Date (YYYY-MM-DD)", "entry_date"),
    ("Event Time (HH:MM)", "entry_time"),
    ("Event Location", "entry_location"),
    ("Attendees (Number)", "entry_attendees")
]

widgets = {}
for i, (label, var_name) in enumerate(fields):
    ttk.Label(frame_form, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=8)
    entry = ttk.Entry(frame_form, width=50)
    entry.grid(row=i, column=1, padx=10, pady=8)
    widgets[var_name] = entry

entry_name = widgets["entry_name"]
entry_date = widgets["entry_date"]
entry_time = widgets["entry_time"]
entry_location = widgets["entry_location"]
entry_attendees = widgets["entry_attendees"]

entry_date.insert(0, date.today().strftime("%Y-%m-%d"))  # Default today's date

ttk.Label(frame_form, text="Category").grid(row=5, column=0, sticky="w", padx=5, pady=8)
category_var = tk.StringVar(value="Conference")
category_menu = ttk.Combobox(frame_form, textvariable=category_var,
                             values=["Conference", "Workshop", "Webinar", "Festival", "Meetup"], state="readonly")
category_menu.grid(row=5, column=1, padx=10, pady=8)

ttk.Label(frame_form, text="Description").grid(row=6, column=0, sticky="nw", padx=5, pady=8)
text_description = tk.Text(frame_form, height=5, width=50)
text_description.grid(row=6, column=1, padx=10, pady=8)

frame_buttons = ttk.Frame(tab_form)
frame_buttons.pack(pady=15)

btn_add = tk.Button(frame_buttons, text="➕ Add Event", command=add_event, bg="#ffffff", fg="black", font=("Segoe UI", 10, "bold"), relief="raised", borderwidth=2)
btn_add.grid(row=0, column=0, padx=10)
btn_add.bind("<Enter>", on_enter)
btn_add.bind("<Leave>", on_leave)

btn_update = tk.Button(frame_buttons, text="✏️ Update Event", command=update_event, bg="#ffffff", fg="black", font=("Segoe UI", 10, "bold"), relief="raised", borderwidth=2)
btn_update.grid(row=0, column=1, padx=10)
btn_update.bind("<Enter>", on_enter)
btn_update.bind("<Leave>", on_leave)

btn_delete = tk.Button(frame_buttons, text="🗑️ Delete Event", command=delete_event, bg="#ffffff", fg="black", font=("Segoe UI", 10, "bold"), relief="raised", borderwidth=2)
btn_delete.grid(row=0, column=2, padx=10)
btn_delete.bind("<Enter>", on_enter)
btn_delete.bind("<Leave>", on_leave)

btn_clear = tk.Button(frame_buttons, text="❌ Clear All", command=clear_all_events, bg="#ffffff", fg="black", font=("Segoe UI", 10, "bold"), relief="raised", borderwidth=2)
btn_clear.grid(row=0, column=3, padx=10)
btn_clear.bind("<Enter>", on_enter)
btn_clear.bind("<Leave>", on_leave)

# Event List Tab
tab_list = ttk.Frame(notebook)
notebook.add(tab_list, text='🔍 View / Search Events')

frame_search = ttk.LabelFrame(tab_list, text="🔎 Search", padding=10)
frame_search.pack(fill="x", padx=20, pady=20)

ttk.Label(frame_search, text="Search by Name / Location / Category").pack(anchor="w")
entry_search = ttk.Entry(frame_search, width=60)
entry_search.pack(side="left", padx=5, pady=5)
ttk.Button(frame_search, text="🔍 Search", command=search_event).pack(side="left", padx=5)
ttk.Button(frame_search, text="📤 Export to CSV", command=export_to_csv).pack(side="left", padx=5)
ttk.Button(frame_search, text="🔄 Refresh", command=view_events).pack(side="left", padx=5)

frame_list = ttk.LabelFrame(tab_list, text="📋 All Events", padding=10)
frame_list.pack(fill="both", expand=True, padx=20, pady=10)

listbox_events = tk.Listbox(frame_list, width=100, height=20, bg="#ffffff", fg="#000000", font=("Segoe UI", 10))
listbox_events.pack(padx=10, pady=10)
listbox_events.bind('<Double-1>', show_event_popup)

label_count = ttk.Label(tab_list, text="Total Events: 0", font=("Segoe UI", 10, "bold"))
label_count.pack(pady=10)

# Animated marquee text banner
def marquee():
    current_text = marquee_label.cget("text")
    marquee_label.config(text=current_text[1:] + current_text[0])
    root.after(150, marquee)

marquee_label = tk.Label(root, text="📢 Welcome to Event Manager - Manage, View & Export Events Easily! 📢",
                         font=("Segoe UI", 10, "italic"), bg="#e0f7fa", fg="#00695c")
marquee_label.pack(pady=5)
marquee()

view_events()
root.mainloop()
