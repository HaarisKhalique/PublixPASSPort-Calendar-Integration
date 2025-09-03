'''
This script is used to directly pass the schedule HTML file 
obtained manually by the user. The data is then processed and 
events are created in the user's calendar.
'''
import sys
import glob
import os
from schedule_processor import process_html
from schedule_uploader import update_calendar

def main():
    #Scan for any htm and html files in the /input directory.
    html_files = glob.glob(os.path.join("input", "*.htm*"))
    print(f"Found {len(html_files)} files.")
    
    #End if no html files are found
    if len(html_files) == 0:
        print("No input files found.")
        sys.exit(1)

    #Process each file found in the /input directory and delete when completed.
    for file in html_files:
        print(f"Processing {file}...")
        html_content = open(file, 'r')
        events = process_html(html_content)
        update_calendar(events)

        print(f"Schedule data uploaded. Deleting {file}...")
        os.remove(file)

    print("All files have been processed. Goodbye!")
    exit()
if __name__ == '__main__':
    main()