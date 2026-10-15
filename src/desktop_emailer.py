import os
import time
from RPA.Windows import Windows
from src.logger import logger

class RobocorpEmailer:
    def __init__(self, receiver_email):
        self.receiver_email = receiver_email
        
        # Initialize the RPA Windows library
        self.win = Windows()
        
        # Exact absolute path for the output directory containing the markdown files
        self.output_dir = r"C:\Users\abdul\OneDrive\Desktop\Linked Matrix\Linked Matrix\django_scraper\output"
        
        # Target files to attach
        self.files_to_attach = ['part1.md', 'part2.md', 'part3.md']

    def send_automated_email(self):
        try:
            logger.info("Initializing Robocorp Windows Automation for Thunderbird...")
            
            # 1. Launch Mozilla Thunderbird
            self.win.windows_run(r"C:\Program Files\Mozilla Thunderbird\thunderbird.exe")
            time.sleep(5)  # Buffer for VM/App load time
            
            # 2. Control the main Thunderbird window
            self.win.control_window("regex:.*Thunderbird.*")
            logger.info("Main window acquired. Clicking 'Write' button...")
            
            # 3. Click the "Write" (New Message) button using the exact Automation ID
            self.win.click("id:folderPaneWriteMessage")
            time.sleep(3)  # Wait for the Compose window to render
            
            # 4. Target the new Compose Window
            # (Note: Using regex allows catching the window regardless of the exact title)
            self.win.control_window("regex:.*Write:.*")
            
            logger.info("Filling email fields (To, Subject, Body)...")
            
            # 5. Enter Receiver Email
            self.win.set_value("id:toAddrInput", self.receiver_email)
            self.win.send_keys(keys="{Enter}")  # FIX: explicitly telling it to press keys, not find a locator
            time.sleep(1)
            
            # 6. Enter Subject
            self.win.set_value("id:msgSubject", "Automated Report: Django Notes Scraped Data")
            time.sleep(1)
            
            # 7. Enter Message Body using the extracted path locator
            body_text = "Hello Team,\n\nThe Django Notes scraper has successfully generated the markdown files.\nPlease find them attached below.\n\nRegards,\nCore Python RPA Bot"
            
            # Pehle box par click karke focus lein, phir as a keyboard input keys send karein
            self.win.click("path:13|4|1|1")
            time.sleep(0.5)
            self.win.send_keys(keys=body_text)
            time.sleep(1)
            
            logger.info("Attaching markdown files sequentially...")
            
            # 8. Loop through and attach files using the native Windows file picker
            for file_name in self.files_to_attach:
                file_path = os.path.join(self.output_dir, file_name)
                
                if os.path.exists(file_path):
                    # Open the attachment dialog via keyboard shortcut
                    self.win.send_keys(keys="{Ctrl}{Shift}a")
                    time.sleep(1.5)  # Wait for the file dialog to open
                    
                    # FIX: Use regex to catch the window to avoid bracket () parsing issues
                    self.win.control_window("regex:.*Attach.*")
                    time.sleep(0.5)
                    
                    # Type the absolute file path and hit Enter
                    self.win.send_keys(keys=file_path)
                    time.sleep(0.5)
                    self.win.send_keys(keys="{Enter}")
                    time.sleep(1.5)  # Buffer for attachment processing
                    
                    # Return focus to the Compose window
                    self.win.control_window("regex:.*Write:.*")
                    logger.info(f"Successfully attached: {file_name}")
                else:
                    logger.warning(f"File not found, skipping attachment: {file_path}")
            
            # 9. Click the Send button using the exact Automation ID
            self.win.click("id:button-send")
            
            logger.info("Email dispatch sequence executed successfully via RPA.Windows!")

        except Exception as e:
            logger.error(f"Critical failure in Windows UI Automation: {e}")