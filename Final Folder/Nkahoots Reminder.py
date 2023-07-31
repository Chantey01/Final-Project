# Program: N'Kahoots Beauty Bot
# Date: July 25,2023
# Programmer: Chantey Chasteen
# Description: This program is a skincare guide that helps users identify their skin type and provides personalized
#              skincare routines and product recommendations based on the skin type selected. Users can select their
#              skin type from the available options (Dry, Oily, Combination, Sensitive) and view recommended skincare
#              products and a daily skincare schedule. Additionally, users have the option to set a daily reminder
#              for their skincare routine.
#
# Features:
# - GUI created using Python's tkinter library
# - Displays instructions on how to pick the correct skin type
# - Allows users to select their skin type from buttons and view descriptions for each skin type
# - Shows recommended products and a skincare schedule for the selected skin type
# - Provides a "Set Daily Reminder" feature to set a daily notification for the skincare routine
# - Saves the application date and time to a CSV file
#
# Programming Details:
# - The code is divided into functions to improve modularity and readability.
# - Constants are used to store paths and fixed values for easier maintenance.
# - Error handling is implemented to handle invalid inputs and exceptions gracefully.
# - The program uses Python dictionaries to store data for each skin type (skin_data) and best times to wash face (best_times).
# - The GUI components (labels, buttons, etc.) are created and arranged using the tkinter library.
# - Images are displayed using the PIL library (Python Imaging Library).
# - Regular expressions (re module) are used for input validation.
# - The program employs object-oriented programming principles to organize related functionalities.

import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta
from tkinter import ttk
import threading
import csv
import os
import re  # Import the regular expression module for input validation

# Sub to record the current application date and time to a CSV file
def record_application_date():
    now = datetime.now()
    with open("application_dates.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S")])

record_application_date()

# Constants
IMAGE_DIR = "/Users/chanteychasteen/Desktop/GUI/Final Folder/images"


# Updated skin_data with detailed skincare schedules and tips for each skin type
skin_data = {
    "Dry": {
        # List of recommended products for dry skin
        "products": ["CeraVe Moisturizing Cream", "Neutrogena Hydro Boost Water Gel", "La Roche-Posay Lipikar Balm AP+"],
        # Description of dry skin
        "description": "Dry skin often feels tight and rough, lacking proper moisture and natural oils. It may appear dull, flaky, or even itchy. Proper hydration, gentle cleansers, \nand nourishing moisturizers are essential to restore its natural balance and achieve a healthy, radiant complexion.",
        # Daily skincare routine for dry skin
        "schedule": "Morning Routine for Dry Skin:\n"
                    "1. Cleanse your face with a mild, hydrating cleanser.\n"
                    "2. Apply a nourishing moisturizer with hyaluronic acid.\n"
                    "3. Use a sunscreen with SPF 30 or higher.\n\n"
                    "Evening Routine for Dry Skin:\n"
                    "1. Double cleanse with an oil-based cleanser followed by a creamy cleanser.\n"
                    "2. Apply a hydrating toner to balance the skin's pH.\n"
                    "3. Use a serum with ingredients like vitamin E and C to combat dryness.\n"
                    "4. Apply a thicker moisturizer to lock in hydration.\n"
                    "5. Optional: Use a facial oil for added nourishment.\n",
        # Tips for dry skin
        "tips": "Tips for Dry Skin:\n"
                "1. Drink plenty of water to keep your skin hydrated.\n"
                "2. Avoid using harsh, alcohol-based products that can dry out your skin.\n"
                "3. Consider adding a weekly hydrating mask to your routine.\n",
        # List of image names for products suitable for dry skin
        "images": ["dry_product01.jpg", "dry_product2.jpg", "dry_product03.jpg"]
    },
    "Oily": { # Data for other skin types follows in a similar structure
        "products": ["Cetaphil Pro Oil Removing Foam Wash", "Paula's Choice Skin Perfecting 2% BHA Liquid Exfoliant", "Neutrogena Oil-Free Moisture Broad Spectrum SPF 35"],
        "description": "Oily skin tends to produce excess sebum, resulting in a shiny, greasy appearance. It is more prone to acne and clogged pores. Using oil-free, \n non-comedogenic products and maintaining a consistent skincare routine can help balance and control oil production.",
        "schedule": "Morning Routine for Oily Skin:\n"
                    "1. Cleanse your face with a gel-based or foaming cleanser.\n"
                    "2. Use a lightweight, oil-free moisturizer.\n"
                    "3. Apply a sunscreen with SPF 30 or higher.\n\n"
                    "Evening Routine for Oily Skin:\n"
                    "1. Double cleanse with a gentle cleanser to remove makeup and oil.\n"
                    "2. Use a toner with ingredients like witch hazel to control excess oil.\n"
                    "3. Apply a light gel-based moisturizer.\n"
                    "4. Use a spot treatment for acne-prone areas.\n"
                    "5. Optional: Use an oil-absorbing sheet during the day.\n",
        "tips": "Tips for Oily Skin:\n"
                "1. Avoid heavy, pore-clogging products.\n"
                "2. Use oil-absorbing sheets during the day to control shine.\n"
                "3. Don't over-wash your face as it can lead to more oil production.\n",
        "images": ["oily_product1.jpg", "oily_product2.jpg", "oily_product3.jpg"]
    },
    "Combination": {
        "products": ["CeraVe Foaming Facial Cleanser", "The Ordinary Niacinamide 10% + Zinc 1%", "Clinique Dramatically Different Moisturizing Gel"],
        "description": "Combination skin is characterized by having both oily and dry areas on the face. The T-zone (forehead, nose, and chin) tends to be oilier, while the cheeks are drier.\n A balanced skincare routine is crucial, using products suitable for both skin types to maintain a healthy complexion.",
        "schedule": "Morning Routine for Combination Skin:\n"
                    "1. Cleanse your face with a gentle cleanser.\n"
                    "2. Apply a lightweight moisturizer on the dry areas.\n"
                    "3. Use an oil-free moisturizer on the oily areas.\n"
                    "4. Apply a sunscreen with SPF 30 or higher.\n\n"
                    "Evening Routine for Combination Skin:\n"
                    "1. Double cleanse with a cleanser suitable for both dry and oily areas.\n"
                    "2. Use a toner to balance the skin's pH.\n"
                    "3. Apply a lightweight moisturizer on the dry areas.\n"
                    "4. Use an oil-free moisturizer on the oily areas.\n"
                    "5. Optional: Use a spot treatment for acne-prone areas.\n",
        "tips": "Tips for Combination Skin:\n"
                "1. Pay attention to the different needs of your T-zone and cheeks.\n"
                "2. Consider using a weekly exfoliating treatment to prevent clogged pores.\n"
                "3. Use oil-absorbing sheets on the T-zone during the day.\n",
        "images": ["combo_product1.jpg", "combo_product2.jpg", "combo_product3.jpg"]
    },
    "Sensitive": {
        "products": ["Vanicream Gentle Facial Cleanser", "Avene Thermal Spring Water", "Cetaphil Daily Hydrating Lotion"],
        "description": "Sensitive skin is easily irritated and reactive to various factors, such as environmental triggers, fragrances, or certain skincare ingredients.\n It requires gentle and hypoallergenic products that soothe and protect the skin's barrier.",
        "schedule": "Morning Routine for Sensitive Skin:\n"
                    "1. Cleanse your face with a mild, fragrance-free cleanser.\n"
                    "2. Apply a lightweight, hypoallergenic moisturizer.\n"
                    "3. Use a sunscreen with SPF 30 or higher.\n\n"
                    "Evening Routine for Sensitive Skin:\n"
                    "1. Double cleanse with a gentle cleanser to remove makeup and impurities.\n"
                    "2. Use a calming toner with ingredients like chamomile or aloe vera.\n"
                    "3. Apply a soothing serum with hyaluronic acid.\n"
                    "4. Use a fragrance-free moisturizer.\n"
                    "5. Optional: Apply a nourishing facial oil for added hydration.\n",
        "tips": "Tips for Sensitive Skin:\n"
                "1. Avoid products with harsh chemicals and fragrances.\n"
                "2. Perform patch tests when trying new products.\n"
                "3. Keep your skincare routine simple and avoid over-exfoliating.\n",
        "images": ["sen_product1.jpg", "sen_product2.jpg", "sen_product3.jpg"]
    }
}


# Dictionary containing best times to wash face based on skin type
best_times = {
    "Dry": "Best time to wash your face is once a day, preferably in the evening.",
    "Oily": "Best time to wash your face is twice a day, once in the morning and once before bed.",
    "Combination": "Best time to wash your face is twice a day, once in the morning and once before bed.",
    "Sensitive": "Best time to wash your face is twice a day, once in the morning and once before bed."
}
# Display a reminder message for skincare routine consistency
def display_reminder(skin_type):
    reminder = "Consistency is key for healthy, glowing skin! 🌟\n"
    reminder += f"You're one day closer to turning your {skin_type} skin into healthier, radiant skin!"
    messagebox.showinfo("Reminder", reminder)

# Open a new window to display recommended products and skincare schedule for the selected skin type
def open_product_window(skin_type): # Code for the product window follows
    product_window = tk.Toplevel(root)
    product_window.title("Products for {} Skin".format(skin_type))

    skin_label = tk.Label(product_window, text="Skin Type: {}".format(skin_type))
    skin_label.pack()

    # Best times to wash face label
    best_times_label = tk.Label(product_window, text=best_times[skin_type])
    best_times_label.pack(pady=5)

    description_label = tk.Label(product_window, text="Description:")
    description_label.pack()

    description_details_label = tk.Label(product_window, text=skin_data[skin_type]["description"])
    description_details_label.pack(pady=5)

    # The button to open the skincare schedule window
    schedule_button = tk.Button(product_window, text="View your Skincare Schedule", command=lambda st=skin_type: open_schedule_window(st, product_window))
    schedule_button.pack(pady=5)


    for index, product in enumerate(skin_data[skin_type]["products"], start=1):
        product_frame = tk.Frame(product_window)
        product_frame.pack(pady=10)

        # Label to display the product name with a bold font
        product_label = tk.Label(product_frame, text=product, font=("Helvetica", 12, "bold"))
        product_label.pack(pady=5)
        # Get the image name and path for the current product
        image_name = skin_data[skin_type]["images"][index - 1]
        image_path = os.path.join(IMAGE_DIR, image_name)
        try:
            # Attempt to open the image and display it with a size of 150x150 pixels
            image = Image.open(image_path)
            image = image.resize((150, 150))
            photo = ImageTk.PhotoImage(image)
            # Label to display the product image
            product_image_label = tk.Label(product_frame, image=photo)
            product_image_label.image = photo
            product_image_label.pack(pady=5)

            # Get the product description
            product_description = get_product_description(skin_type, index)

            # Display the product description with wraplength set to 300 (adjust as needed)
            product_description_label = tk.Label(product_frame, text="Product Description:\n{}".format(product_description), wraplength=300)
            product_description_label.pack()
        except FileNotFoundError:
            print(f"Image not found: {image_path}")
            product_description_label = tk.Label(product_frame, text="Product Description: N/A")
            product_description_label.pack()

    # Button to close the product window (exit button)
    exit_button = tk.Button(product_window, text="Exit", command=product_window.destroy)
    exit_button.pack(pady=10)
# Get the detailed product description for a specific skin type and product index
def get_product_description(skin_type, index):
    # Add the details of each product description here
    descriptions = {
        "Dry": [
            "CeraVe Moisturizing Cream: A popular and effective product specifically formulated for dry skin. It contains essential ceramides and hyaluronic acid, which help to restore and retain the skin's natural moisture barrier. The non-greasy formula provides long-lasting hydration, making it suitable for both the face and body.",
            "Neutrogena Hydro Boost Water Gel: A lightweight, gel-based moisturizer that instantly hydrates the skin. It is formulated with hyaluronic acid, which attracts and locks in moisture, leaving the skin smooth and supple without feeling greasy.",
            "La Roche-Posay Lipikar Balm AP+: An ultra-nourishing balm designed to soothe and replenish dry, uncomfortable skin. It contains shea butter and niacinamide, which help to repair the skin's natural barrier and provide long-lasting hydration."
        ],
        "Oily": [
            "Cetaphil Pro Oil Removing Foam Wash: A foaming facial cleanser specially formulated for oily and acne-prone skin. It effectively removes excess oil, dirt, and impurities without over-drying the skin, leaving it clean and refreshed.",
            "Paula's Choice Skin Perfecting 2% BHA Liquid Exfoliant: A leave-on exfoliant with 2% salicylic acid (BHA) that helps to unclog pores, reduce blackheads, and smooth the skin's texture. It also contains green tea extract for added antioxidant benefits.",
            "Neutrogena Oil-Free Moisture Broad Spectrum SPF 35: An oil-free, non-comedogenic moisturizer with SPF 35 sun protection. It provides lightweight hydration and helps to protect the skin from harmful UV rays without clogging pores or causing breakouts."
        ],
        "Combination": [
            "CeraVe Foaming Facial Cleanser: A gentle foaming cleanser suitable for both oily and dry areas. It effectively removes impurities and excess oil while maintaining the skin's natural moisture balance.",
            "The Ordinary Niacinamide 10% + Zinc 1%: A lightweight serum containing niacinamide and zinc that helps to regulate sebum production, minimize pores, and improve overall skin texture. It is suitable for combination and oily skin types.",
            "Clinique Dramatically Different Moisturizing Gel: A lightweight, oil-free gel moisturizer that provides hydration to the skin without leaving a greasy residue. It is formulated to balance moisture levels for both dry and oily areas."
        ],
        "Sensitive": [
            "Vanicream Gentle Facial Cleanser: A gentle and non-comedogenic cleanser suitable for sensitive and reactive skin. It effectively removes impurities without causing irritation or dryness.",
            "Avene Thermal Spring Water: A soothing and calming mist that provides instant relief to sensitive and irritated skin. It is enriched with minerals to help restore the skin's natural balance.",
            "Cetaphil Daily Hydrating Lotion: A lightweight, hydrating lotion that is non-greasy and ideal for sensitive skin. It provides long-lasting moisture and helps to protect the skin's barrier."
        ]
    }

    # Return the product description based on the skin type and product index
    return descriptions[skin_type][index - 1]

def open_schedule_window(skin_type, product_window):
    def set_reminder():
        reminder_window = tk.Toplevel(schedule_window)
        reminder_window.title("Set Daily Reminder")

        date_label = tk.Label(reminder_window, text="Date (MM-DD):")
        date_label.pack()
        date_entry = tk.Entry(reminder_window)
        date_entry.pack()

        time_label = tk.Label(reminder_window, text="Time (HH:MM):")
        time_label.pack()
        time_entry = tk.Entry(reminder_window)
        time_entry.pack()

        am_pm_frame = tk.Frame(reminder_window)
        am_pm_frame.pack(pady=5)

        am_var = tk.StringVar(value="AM")
        am_button = tk.Radiobutton(am_pm_frame, text="AM", variable=am_var, value="AM")
        am_button.pack(side=tk.LEFT)

        pm_var = tk.StringVar(value="PM")
        pm_button = tk.Radiobutton(am_pm_frame, text="PM", variable=pm_var, value="PM")
        pm_button.pack(side=tk.LEFT)

        # Call the set_reminder_handler function with necessary arguments
        set_reminder_button = tk.Button(reminder_window, text="Set Reminder", command=lambda: set_reminder_handler(date_entry, time_entry, am_var))
        set_reminder_button.pack(pady=5)

        # Create the schedule window
    schedule_window = tk.Toplevel(product_window)
    schedule_window.title("Daily Skincare Schedule for {} Skin".format(skin_type))
    # Label for the skincare schedule
    schedule_label = tk.Label(schedule_window, text="Skincare Schedule:")
    schedule_label.pack()
    # Label displaying the skincare schedule details based on the selected skin type
    schedule_details_label = tk.Label(schedule_window, text=skin_data[skin_type]["schedule"])
    schedule_details_label.pack(pady=5)
    # Label for displaying the best times to wash face based on the selected skin type
    best_times_label = tk.Label(schedule_window, text="Best Times to Wash Face:")
    best_times_label.pack()
    # Label displaying the best times to wash face details based on the selected skin type
    best_times_details_label = tk.Label(schedule_window, text=best_times[skin_type])
    best_times_details_label.pack(pady=5)
    # Button to set a daily reminder for the skincare routine
    reminder_button = tk.Button(schedule_window, text="Set Daily Reminder", command=set_reminder)
    reminder_button.pack(pady=5)

def set_reminder_handler(date_entry, time_entry, am_var):
        # Retrieve the date, time, and AM/PM selection from user inputs
        date = date_entry.get()
        time = time_entry.get()
        am_pm = am_var.get()

        # Validate date format (MM-DD)
        if not re.match(r"^\d{2}-\d{2}$", date):
            messagebox.showerror("Invalid Date", "Please enter the date in the format MM-DD.")
            return

        # Validate time format (HH:MM)
        if not re.match(r"^\d{2}:\d{2}$", time):
            messagebox.showerror("Invalid Time", "Please enter the time in the format HH:MM.")
            return
        # Convert the user-entered date, time, and AM/PM to a datetime object
        reminder_datetime = datetime.strptime(date + " " + time + " " + am_pm, "%m-%d %I:%M %p")
        # Check if the chosen time has already passed, prompt to set an appointment for tomorrow or the following day if needed
        if reminder_datetime <= datetime.now():
            if messagebox.askyesno("Time Passed", "The chosen time has already passed. Would you like to set an appointment for tomorrow or the following day?"):
                reminder_datetime += timedelta(days=1)
            else:
                return
         # Calculate the time interval until the reminder should be displayed
        reminder_interval = (reminder_datetime - datetime.now()).total_seconds()
        # Use threading to schedule the reminder display at the specified time
        threading.Timer(reminder_interval, lambda: display_reminder(skin_type)).start()
        messagebox.showinfo("Reminder Set", "Daily reminder has been set.")
         
        

def show_skin_type_instructions():
    messagebox.showinfo("How to Pick Your Skin Type",
                        "Welcome to N'kahoots Skin Type Selector!\n\n"
                        "Please read the descriptions of each skin type below and select the one that best "
                        "matches your skin characteristics. Once you choose your skin type, you will see "
                        "the recommended products and skincare schedule.\n\n"
                        "Dry Skin: Lacks moisture and often feels tight and rough. Proper hydration, gentle cleansers, and nourishing moisturizers are essential for a healthy, radiant complexion.\n\n"
                        "Oily Skin: Produces excess sebum, resulting in a shiny, greasy appearance. Balancing oil production and using non-comedogenic products can help control shine and maintain a clearer complexion.\n\n"
                        "Combination Skin: Characterized by both oily and dry areas. A skincare routine addressing both types is essential for a balanced complexion.\n\n"
                        "Sensitive Skin: Easily irritated and reactive to various factors. Using gentle, hypoallergenic products can help soothe and protect sensitive skin.\n\n"
                        "Reminder: After selecting your skin type and viewing the recommended products and skincare schedule, you have the option to set a daily reminder for your skincare routine.\n Click on the 'Set Daily Reminder' button to choose a date and time for your daily reminder. If the chosen time has already passed, you will be prompted to set an appointment for tomorrow or the following day.\n\n"
                        "Consistency is key for achieving healthy, glowing skin! Your daily reminder will help you stay on track with your skincare routine and work towards improving your skin's health and appearance.\n")


# Display the skin description with wraplength set to 500 (adjust as needed)
    skin_description_label = tk.Label(root, text=description, wraplength=500)
    skin_description_label.pack()

# the main window
root = tk.Tk()
root.title("N'Kahoots Beauty Bot")

# Skin Type Selector Instructions
instruction_label = tk.Label(root, text="How to Pick Your Skin Type", font=("Helvetica", 14, "bold"))
instruction_label.pack(pady=10)

show_instructions_button = tk.Button(root, text="Read Me!", command=show_skin_type_instructions)
show_instructions_button.pack()

# The buttons for each skin type with descriptions
button_data = [
    ("Dry", "Dry skin lacks moisture and often feels tight and rough.\nProper hydration, gentle cleansers, and nourishing moisturizers are essential for a healthy, radiant complexion."),
    ("Oily", "Oily skin produces excess sebum, resulting in a shiny, greasy appearance.\nBalancing oil production and using non-comedogenic products can help control shine and maintain a clearer complexion."),
    ("Combination", "Combination skin has both oily and dry areas.\nA skincare routine addressing both types is essential for a balanced complexion."),
    ("Sensitive", "Sensitive skin is easily irritated and reactive to various factors.\nUsing gentle, hypoallergenic products can help soothe and protect sensitive skin.")
]
# Loop through the skin types and create buttons for each with their descriptions
for skin_type, description in button_data:
    button = tk.Button(root, text=skin_type, command=lambda st=skin_type: open_product_window(st))
    button.pack(pady=5)

    desc_label = tk.Label(root, text=description)
    desc_label.pack()

# Exit button callback function
def exit_application():
    if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
        root.destroy()
# Button to exit the application
exit_button = tk.Button(root, text="Exit", command=exit_application)
exit_button.pack(pady=5)


root.mainloop()
