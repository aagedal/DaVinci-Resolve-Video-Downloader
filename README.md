# DaVinci Resolve Video Downloader


### About
A python script for DaVinci Resolve (Studio) for macOS (support for other platforms may come in the future). Intended to be started from within Resolve.
The script starts a GUI where you can paste a link to a YouTube, TikTok, Instagram, or other web video. Click the Download-button to download to a specified location using yt-dlp.

Once Download is complete, the script will re-encode non-mp4 files to .mp4 using ffmpeg, to ensure compatibility.

Then the script automatically imports the video into DaVinci Resolve Media Pool.



## Installation
Copy the .py-file into the folder into DaVinci Resolves script-folder so that Resolve can find it. You may need to restart Resolve for it to show up.

#### Blackmagic Design-installer version:
~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver/

#### Mac App Store version: NOTE
~/Library/Containers/com.blackmagic-design.DaVinciResolveAppStore/Data/Library/Application\ Support/Fusion/Scripts/Deliver/


## Usage
- Run this script from DaVinci Resolve's dropdown menu: Workspace -> Scripts


## Goals
[] Make it remember your chosen download-folder.
	- Work not started.
[] Update UI to display download and conversion process
	- Work not started.



#### Inspired by
This project is inspired by a similar project by neezr: https://github.com/neezr/YouTube-Downloader-for-DaVinci-Resolve.
I started by just doing small improvements in a fork, but now the code changes are so significant that it feels more like a separate project. I still wanted to give some credit to the original project.
