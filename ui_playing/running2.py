import PySimpleGUI as sg
import os
import platform
def clear_terminal():
    os_name = platform.system()
    if os_name == "Windows":
        os.system("cls")
    else:
        os.system("clear")
        
# start the program with a clear terminal
clear_terminal()

# Define the GUI layout for the "Unit Conversion" tab
unit_conversion_layout = [
    [sg.Text("Select pace unit:", font=("Helvetica", 24))],
    [sg.Radio("min/km", "pace_unit", key="unit_km", default=True, font=("Helvetica", 24)),
     sg.Radio("min/mile", "pace_unit", key="unit_mile", font=("Helvetica", 24))],
    [sg.Text("Enter pace in minutes:", font=("Helvetica", 24)),
     sg.Input(key="pace_min", size=(4, 1), font=("Helvetica", 24), enable_events=True)],
    [sg.Text("Enter pace in seconds:", font=("Helvetica", 24)),
     sg.Input(key="pace_sec", size=(4, 1), font=("Helvetica", 24), enable_events=True)],
    [sg.Button("Convert", key="convert_btn", font=("Helvetica", 24)), sg.Button("OK", key="OK1", font=("Helvetica", 24))],
    [sg.Text("", key="converted_pace", font=("Helvetica", 32), visible=False)]
]

# Define the GUI layout for the "Race Predictor" tab
race_predictor_layout = [
    [sg.Text("Predicted Pace (min:sec):", font=("Helvetica", 24))],
    [sg.Input(key="predicted_pace", size=(6, 1), font=("Helvetica", 24), enable_events=True)],
    [sg.Text("Distance (km):", font=("Helvetica", 24))],
    [sg.Input(key="distance", size=(6, 1), font=("Helvetica", 24), enable_events=True)],
    [sg.Button("Calculate", key="calculate_btn", font=("Helvetica", 24)),sg.Button("OK", font=("Helvetica", 24), key="OK2")],
    [sg.Text("", key="race_time", font=("Helvetica", 32), visible=False)]
]

interval_layout = [
    [sg.Text('Interval Pace (min:sec):', font=("Helvetica", 24)), sg.Input(key='-PACE-', size=(6, 1), font=("Helvetica", 24))],
    [sg.Text('Distance:', font=("Helvetica", 24)), sg.Combo(['100m', '200m', '400m', '600m', '800m', '1000m', '1600m'], key='-DISTANCE-', size=(6, 1), font=("Helvetica", 24))],
    [sg.Button('Convert', key="Convert_interval", size=(10, 1), font=("Helvetica", 24)), sg.Button('Ok', key="OK3", size=(10, 1), font=("Helvetica", 24))],
    [sg.Text("", key="Interval_time", font=("Helvetica", 32), visible=False)]
]

# Define the GUI layout for the "Speed Conversion" tab
speed_conversion_layout = [
    [sg.Text("Select conversion:", font=("Helvetica", 24))],
    [sg.Radio("To mph", "conversion", key="mph", default=True, font=("Helvetica", 24)),
     sg.Radio("To kph", "conversion", key="kph", font=("Helvetica", 24))],
    [sg.Text("Enter speed in min:sec per km:", font=("Helvetica", 24)),
     sg.Input(key="speed", size=(6, 1), font=("Helvetica", 24), enable_events=True)],
    [sg.Button("Convert", key="convert_speed", font=("Helvetica", 24)), sg.Button("OK", key="OK4", font=("Helvetica", 24))],
    [sg.Text("", key="converted_speed", font=("Helvetica", 32), visible=False)]
]

# Define the GUI layout for the "kph to min:km" tab
kph_to_min_km_layout = [
    [sg.Text("Enter speed in km/h:", font=("Helvetica", 24))],
    [sg.Input(key="kph_input", size=(6, 1), font=("Helvetica", 24), enable_events=True)],
    [sg.Button("Convert", key="convert_kph", font=("Helvetica", 24)), sg.Button("OK", key="OK5", font=("Helvetica", 24))],
    [sg.Text("", key="converted_pace_kph", font=("Helvetica", 32), visible=False)]
]

# Define the GUI layout for the "mph to min:miles" tab
mph_to_min_miles_layout = [
    [sg.Text("Enter speed in mph:", font=("Helvetica", 24))],
    [sg.Input(key="mph_input", size=(6, 1), font=("Helvetica", 24), enable_events=True)],
    [sg.Button("Convert", key="convert_mph", font=("Helvetica", 24)), sg.Button("OK", key="OK6", font=("Helvetica", 24))],
    [sg.Text("", key="converted_pace_mph", font=("Helvetica", 32), visible=False)]
]

# Define the main layout with the tab group
layout = [
    [sg.TabGroup([[sg.Tab("Metric <-> Imperial", unit_conversion_layout),
                   sg.Tab("Race Predictor", race_predictor_layout),
                   sg.Tab("Interval time", interval_layout),
                   sg.Tab("Convert to mph/kph", speed_conversion_layout),
                   sg.Tab("kph to min:km", kph_to_min_km_layout),
                   sg.Tab("mph to min:miles", mph_to_min_miles_layout),
                   ]],
                 font=("Helvetica", 24))]
]

# set that the calulations have not been run
tab1_result = [False]
tab2_result = [False]
tab3_result = [False]
tab4_result = [False]
tab5_result = [False]
tab6_result = [False]

# Create the window
window = sg.Window("Running calculations", layout)

# Function to convert the pace and update the window
def convert_pace():
    try:
        # Get the values entered by the user
        pace_min = int(values["pace_min"]) if values["pace_min"].isdigit() else 0
        pace_sec = int(values["pace_sec"]) if values["pace_sec"].isdigit() else 0

        # Convert pace to min:sec format
        total_sec = pace_min * 60 + pace_sec
        pace_min_sec = divmod(total_sec, 60)
        pace_min_sec_format = f"{pace_min_sec[0]}:{pace_min_sec[1]:02d}"

        # Convert pace to min/km or min/mile format
        if values["unit_km"]:
            convert_from = 'min/km'
            convert_to = 'min/mile'
            pace_km = total_sec / 60 / (1 / 1.60934)  # Convert min/km to min/mile
            pace_km_min = int(pace_km)
            pace_km_sec = int((pace_km % 1) * 60)
            pace_km_format = f"{pace_km_min}:{pace_km_sec:02d}"
            pace_formatted = pace_km_format
            window["converted_pace"].update(f"min/mile: {pace_formatted}", font=("Helvetica", 32), visible=True)
        else:
            convert_from = 'min/mile'
            convert_to = 'min/km'
            pace_mile = total_sec / 60 / (1 * 1.60934)  # Convert min/mile to min/km
            pace_mile_min = int(pace_mile)
            pace_mile_sec = int((pace_mile % 1) * 60)
            pace_mile_format = f"{pace_mile_min}:{pace_mile_sec:02d}"
            pace_formatted = pace_mile_format
            window["converted_pace"].update(f"min/km: {pace_formatted}", font=("Helvetica", 32), visible=True)

        return_list = [True, convert_from, convert_to, pace_min, pace_sec, pace_formatted ]
        return return_list

    except ValueError:
        sg.popup_error("Invalid input. Please enter numeric values for pace.")
        return_list = [False, '', '', 0, 0, '' ]
        return return_list

# Function to calculate the race time and update the window
def calculate_race_time():
    try:
        # Get the values entered by the user
        predicted_pace = values["predicted_pace"]
        distance = float(values["distance"]) if values["distance"].replace(".", "", 1).isdigit() else 0.0

        # Calculate the race time
        pace_min, pace_sec = predicted_pace.split(":")
        total_sec_per_km = int(pace_min) * 60 + int(pace_sec)
        race_time_sec = total_sec_per_km * distance

        # Convert the race time to hours, minutes, and seconds
        race_time_hour, remainder = divmod(race_time_sec, 3600)
        race_time_min, race_time_sec = divmod(remainder, 60)

        # Format the race time as "h:mm:ss"
        race_time_format = f"{int(race_time_hour)}:{int(race_time_min):02d}:{int(race_time_sec):02d}"

        # Update the window with the race time
        window["race_time"].update(f"Race Time: {race_time_format}", font=("Helvetica", 32), visible=True)

        return_list = [True, predicted_pace, distance, race_time_format]

        return return_list

    except ValueError:
        sg.popup_error("Invalid input. Please enter numeric values for predicted pace and distance.")
        return_list = [False, 0, 0, '' ]
        return return_list

def calc_time():
    try:
        interval_pace = values['-PACE-']
        input_distance = values['-DISTANCE-']
        distance = int(input_distance[:-1])
        minutes, seconds = map(int, interval_pace.split(':'))
        total_seconds = minutes * 60 + seconds
        pace_per_meter = total_seconds / 1000  # Pace per meter
        time = pace_per_meter * float(distance)
        minutes = int(time // 60)
        seconds = int(time % 60)
        window["Interval_time"].update(f"Time: {minutes} min {seconds} sec to go {distance} meters.",
                                    font=("Helvetica", 32), visible=True)
        
        return_list = [True, interval_pace, input_distance, minutes, seconds]
        return return_list
    
    except ValueError:
        sg.popup_error("Invalid input. Please enter numeric values for pace and distance.")
        return_list = [False, '', '', 0, 0]
        return return_list

# Function to convert the speed and update the window
def convert_speed():
    try:
        # Get the values entered by the user
        speed_input = values["speed"]

        # Split the input into minutes and seconds
        if ":" in speed_input:
            minutes, seconds = map(int, speed_input.split(":"))
        else:
            minutes, seconds = 0, int(speed_input)

        # Calculate the total seconds
        total_seconds = minutes * 60 + seconds

        # Convert speed to mph or kph format
        if values["mph"]:
            # Calculate the pace per kilometer
            pace_per_km = total_seconds / 60

            # Convert pace per kilometer to pace per mile
            # pace_per_mile = pace_per_km / 1.60934
            pace_per_mile = pace_per_km * 1.60934

            # Calculate speed in miles per hour
            converted_speed = 60 / pace_per_mile

            unit = "mph"
        else:
            # Calculate the speed in kilometers per hour
            converted_speed = (60 * 60) / total_seconds

            unit = "kph"

        window["converted_speed"].update(f"{unit}: {converted_speed:.2f}", visible=True)

        return_list = [True, speed_input, unit, converted_speed]
        return return_list

    except ValueError:
        sg.popup_error("Invalid input. Please enter a valid speed in the format 'minutes:seconds' or 'seconds'.")
        return_list = [False, '', '', 0]
        return return_list
    
# Function to convert kph to min:km and update the window
def convert_kph_to_min_km():
    try:
        # Get the value entered by the user
        kph_input = values["kph_input"]

        # Convert kph to min:km format
        pace_km = 60 / float(kph_input)
        pace_km_min = int(pace_km)
        pace_km_sec = int((pace_km % 1) * 60)
        pace_km_format = f"{pace_km_min}:{pace_km_sec:02d}"
        pace_formatted = pace_km_format

        # Update the window with the converted pace
        window["converted_pace_kph"].update(f"min/km: {pace_formatted}", font=("Helvetica", 32), visible=True)

        return_list = [True, kph_input, pace_formatted]
        return return_list

    except ValueError:
        sg.popup_error("Invalid input. Please enter a valid speed in km/h.")
        return_list = [False, '', '']
        return return_list

# Function to convert mph to min:miles and update the window
def convert_mph_to_min_miles():
    try:
        # Get the value entered by the user
        mph_input = values["mph_input"]

        # Convert mph to min:miles format
        pace_mile = 60 / float(mph_input)
        pace_mile_min = int(pace_mile)
        pace_mile_sec = int((pace_mile % 1) * 60)
        pace_mile_format = f"{pace_mile_min}:{pace_mile_sec:02d}"
        pace_formatted = pace_mile_format

        # Update the window with the converted pace
        window["converted_pace_mph"].update(f"min/mile: {pace_formatted}", font=("Helvetica", 32), visible=True)

        return_list = [True, mph_input, pace_formatted]
        return return_list

    except ValueError:
        sg.popup_error("Invalid input. Please enter a valid speed in mph.")
        return_list = [False, '', '']
        return return_list
    
# Event loop to process events
while True:
    event, values = window.read()

    # Check if the window is closed
    if event == sg.WINDOW_CLOSED:
        break

    # Convert button event in "Unit Conversion" tab 1
    if event == "convert_btn":
        tab1_result = convert_pace()

    # Calculate button event in "Race Predictor" tab 2
    if event == "calculate_btn":
        tab2_result = calculate_race_time()

    # convert button (3nd tab) event
    if event == "Convert_interval":
         tab3_result = calc_time()

    # convert button (4th tab) event
    if event == "convert_speed":
         tab4_result = convert_speed()
    
    # Convert button event in "kph to min:km" tab
    if event == "convert_kph":
        tab5_result = convert_kph_to_min_km()

     # Convert button event in "mph to min:miles" tab
    if event == "convert_mph":
        tab6_result = convert_mph_to_min_miles()

    # OK button event
    if event == "OK1" or event == "OK2" or event == "OK3" or event == "OK4" or event == "OK5" or event == "OK6":
        break

# Confirm tab 1 ran (this is in index 0), and then print the last results from it
if tab1_result[0] == True:
    print(f"Converted {tab1_result[3]}:{tab1_result[4]} {tab1_result[1]} to {tab1_result[5]} {tab1_result[2]}")

# Confirm tab 2 ran (this is in index 0), and then print the last results from it
if tab2_result[0] == True:
    print(f"With a pace of {tab2_result[1]} min/km, for a distance of {tab2_result[2]} km, it will take {tab2_result[3]} (h:min:sec) to finish")

# Confirm tab 3 ran (this is in index 0), and then print the last results from it
if tab3_result[0] == True:
    print(f"With a pace of {tab3_result[1]} min/km, for a distance of {tab3_result[2]}, it will take {tab3_result[3]}:{tab3_result[4]} (min:sec) to finish")

# Confirm tab 4 ran (this is in index 0), and then print the last results from it
if tab4_result[0] == True:
    print(f"Converted {tab4_result[1]} min/km to {tab4_result[3]:.2f} {tab4_result[2]}")

# Confirm tab 5 ran (this is in index 0), and then print the last results from it
if tab5_result[0] == True:
    print(f"Converted {tab5_result[1]} km/h to {tab5_result[2]} min/km")

# Confirm tab 6 ran (this is in index 0), and then print the last results from it
if tab6_result[0] == True:
    print(f"Converted {tab6_result[1]} mph to {tab6_result[2]} min/mile")

# Close the window
window.close()
