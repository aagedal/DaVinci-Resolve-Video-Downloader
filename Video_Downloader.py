# Video Downloader for DaVinci Resolve

# Usage:
# Run this script from DaVinci Resolve's dropdown menu: Workspace -> Scripts -> Video Downloader
# Select your project folder and paste a YouTube URL into the text field
# The video will automatically be downloaded as .mp4-file with the highest available resolution, placed in your project folder and imported to your Media Pool

# Install:
#Mac App Store version:
#~/Library/Containers/com.blackmagic-design.DaVinciResolveAppStore/Data/Library/Application\ Support/Fusion/Scripts/Deliver/

#Blackmagic installer version:
#~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver/

# Install Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Install ffmpeg and yt-dlp with homebrew: brew install ffmpeg && brew install yt-dlp

import os, subprocess
import platform
import tkinter as tk
from tkinter import filedialog



# Check if FFMPEG exists
if os.path.exists('/opt/homebrew/bin/ffmpeg') and os.path.exists('/opt/homebrew/bin/yt-dlp'):
	result = subprocess.run(['/opt/homebrew/bin/ffmpeg', '-version'], stdout=subprocess.PIPE)
	#print(result.stdout)
else:
	root_errormsg = tk.Tk()

	def copy_homebrew_to_clipboard():
		root_errormsg.clipboard_clear()
		root_errormsg.clipboard_append('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
		root_errormsg.update()

	def copy_ffmpeg_to_clipboard():
		root_errormsg.clipboard_clear()
		root_errormsg.clipboard_append("brew install ffmpeg && brew install yt-dlp")
		root_errormsg.update()

	root_errormsg.wm_title("FFMPEG or YT-DLP not found")
	err_msg = tk.Label(root_errormsg, text="Module 'ffmpeg' or 'yt-dlp' not found!\n\n'Video Downloader for DaVinci Resolve' requires the external module 'ffmpeg' and 'yt-dlp' for downloading YouTube videos.\nPlease install ffmpeg by opening the command line interface and running:")
	err_msg.pack(side="top", fill="x", pady=10)

	homebrew_install_string = '"/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
	err_msg2 = tk.Label(root_errormsg, fg="black", bg="white", text=homebrew_install_string)
	err_msg2.pack(side="top", fill="x", pady=10)

	copy_button = tk.Button(text="Copy command!", command=copy_homebrew_to_clipboard)
	copy_button.pack(side="top")

	err_msg3 = tk.Label(root_errormsg, text="And then run:")
	err_msg3.pack(side="top", fill="x", pady=10)

	ffmpeg_install_string = "brew install ffmpeg && brew install yt-dlp"
	err_msg4 = tk.Label(root_errormsg, fg="black", bg="white", text=ffmpeg_install_string)
	err_msg4.pack(side="top", fill="x", pady=10)

	copy_button = tk.Button(text="Copy command!", command=copy_ffmpeg_to_clipboard)
	copy_button.pack(side="top")

	l_ok_button = tk.Button(root_errormsg, text="Okay", command=root_errormsg.destroy)
	root_errormsg.mainloop()

	exit

# Get user directory
import getpass as gt
currentUser = gt.getuser()
home = "/Users/" + currentUser

download_location = home + "/Movies/DaVinci_YouTube_Downloader/"


def downloadVideo(link):
		print("Starting download" + "\n")
		if link == "":
			print("Link is empty. Skipping download." + "\n")
			pass
		else:
			print("Link is not empty, starting download." + "\n")
		
        #yt-dlp path
		yt_dlp_path = "/opt/homebrew/bin/yt-dlp"

        #yt-dlp get filename
		yt_dlp_filename_args = [yt_dlp_path, link, "--print", "filename", "--restrict-filenames", "--ignore-config", "-o", download_location + "%(title)s-%(id)s.%(ext)s", "--skip-download"]
		yt_dlp_filename_pipe = subprocess.run(yt_dlp_filename_args, stdout=subprocess.PIPE)
		print("yt_dlp_filename is set to:")
		print(yt_dlp_filename_pipe.stdout.decode('UTF-8').partition('\n')[0])
		yt_dlp_filename = yt_dlp_filename_pipe.stdout.decode('UTF-8').partition('\n')[0]

		print("yt-dlp filename initial output:")
		print(yt_dlp_filename)

		yt_dlp_filename_mp4 = ""

		# Change printed output file name to .mp4 to match actually downloaded and reencoded file name and path
		if yt_dlp_filename.endswith(".webm"):
			new_name = yt_dlp_filename[:-4]
			yt_dlp_filename_mp4 = new_name + "mp4"


		print("MP4 filename is:")
		print(yt_dlp_filename_mp4)
        
		#yt-dlp download subprocess here
		yt_dlp_args = [yt_dlp_path, link, "--restrict-filenames", "-f", "bestvideo*+bestaudio/best", "--recode-video", "mp4", "--ignore-config", "-o", download_location + "%(title)s-%(id)s.%(ext)s"]


		# Run process with terminal readout
		with subprocess.Popen(yt_dlp_args, stdout=subprocess.PIPE, bufsize=0) as p:
			char = p.stdout.read(1)
			while char != b'':
				print(char.decode('UTF-8'), end='', flush=True)
				char = p.stdout.read(1)


		# Add files to Resolve after Download and Remux... Error with Remux. Unsure why.
		if os.path.exists(yt_dlp_filename_mp4):
			print(f"Done! Downloaded {yt_dlp_filename_mp4} to {download_location} \n")
			print("Adding downloaded file to MediaPool")
			resolve.GetMediaStorage().AddItemsToMediaPool(yt_dlp_filename_mp4)
		else:
			print("Output file not found.")


#GUI

def gui_download_event():
	global entryField, downloadbutton
	url = entryField.get()
	if len(url) > 0:
		print(url)
		downloadbutton.configure(state="disabled", text="Downloading...")
		entryField.configure(state="disabled")
		try:
			downloadVideo(url)
		except Exception: #Problem with merging audio and video
			print("Problem with merging audio and video")
			pass
		downloadbutton.configure(state="normal", text="Download")
		entryField.configure(state="normal")
		entryField.delete(0, "end")


def gui_change_filelocation_event():
	global filedownload_label, download_location
	previous_filelocation = download_location #resetting after canceling out the prompt window
	download_location = filedialog.askdirectory()
	if not download_location:
		download_location = previous_filelocation
	filedownload_label.configure(text=download_location)
	print("The file location is: " + download_location)

def gui_reset_filelocation_event():
	global filedownload_label, download_location, STANDARD_FILE_LOCATION
	download_location = STANDARD_FILE_LOCATION
	filedownload_label.configure(text=download_location)


window = tk.Tk()
window.title("Aagedals YouTube Downloader for DaVinci Resolve")
window.geometry("650x200")
BG_COLOR = '#28282e'
FG_COLOR = '#cac5c4'
window.configure(background=BG_COLOR)

top_text = tk.Label(window, text=top_text_variable, textvariable=top_text_variable, bg=BG_COLOR, fg=FG_COLOR)
top_text.pack(side="top",expand=True,fill="both")


entryField = tk.Entry(window)
entryField.pack(side="top",expand=True,fill="both")

downloadbutton = tk.Button(window, text="Download", command=gui_download_event)
downloadbutton.pack(side="top",expand=True,fill="both")




filedownload_label = tk.Label(window, text=download_location, anchor="w", bg=BG_COLOR, highlightbackground = "gray", highlightthickness=2, fg=FG_COLOR)
filedownload_label.pack(side="top",expand=True,fill="both")


filelocation_button = tk.Button(window, text="Change download folder", command=gui_change_filelocation_event, padx=5, pady=10)
filelocation_button.pack(side="left",expand=True,fill="both")


filereset_button = tk.Button(window, text="Reset download folder", command=gui_reset_filelocation_event, padx=5, pady=10)
filereset_button.pack(side="left",expand=True,fill="both")



window.mainloop()
