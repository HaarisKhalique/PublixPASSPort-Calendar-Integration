'''
This script is used to directly pass the schedule HTML file 
obtained manually by the user. The data is then processed and 
events are created in the user's calendar.
'''
import sys
import glob
import os
import shutil
from schedule_processor import process_html
from schedule_uploader import update_calendar

INPUT_DIR = "input"

#Deletes all files in input directory.
def delete_input_files(directory_path):
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def main():
    #Scan for any htm and html files in the /input directory.
    html_files = glob.glob(os.path.join(INPUT_DIR, "*.htm*"))
    print(f"Found {len(html_files)} files.")
    
    #End if no html files are found
    if len(html_files) == 0:
        print("No input files found.")
        sys.exit(1)

    #Process each file found in the /input directory and delete when completed.
    for file in html_files:
        html_content = open(file, 'r')
        events = process_html(html_content)
        update_calendar(events)

    print("Your shifts have been added to your calendar. Goodbye!")
    delete_input_files(INPUT_DIR)
    exit()
if __name__ == '__main__':
    main()