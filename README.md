# Mashup Generator (Assignment - UCS654)

This repository contains the implementation of the **Mashup Generator Assignment**.  
The project is completed in two parts:

- **Program 1:** Command Line Mashup Generator  
- **Program 2:** Web Service Mashup Generator (Flask + Render Deployment)

The mashup is created by downloading audio from YouTube, trimming the first `y` seconds from each video, merging them, and generating the final output in `.mp3` format (and `.zip` in Program 2).

---

# Program 1 (Command Line Program)

### Description:
Program 1 is a Python script that generates a mashup directly from the command line.  
It takes the singer name, number of videos, duration of each clip, and output filename as input.

The script uses:
- `yt-dlp` for downloading YouTube audio
- `ffmpeg` for audio conversion
- `pydub` for trimming and merging audio clips

### Input:
- Singer Name
- Number of videos (n)
- Duration of each clip (y seconds)
- Output mp3 file name

- <img width="460" height="22" alt="image" src="https://github.com/user-attachments/assets/a1a5c13d-84f9-4f6a-bbc7-68f335a82a49" />


### Output:
- A single mashup `.mp3` file

- <img width="462" height="66" alt="image" src="https://github.com/user-attachments/assets/a0346e89-d035-4de5-864e-5dc6cdde4cdd" />


### Run Program 1:
python 102303184.py "Sharry Mann" 20 30 output.mp3


# Program 2 (Web Service Mashup)

### Description
Program 2 is a Flask-based web service that generates mashups through a website UI.  
The user enters singer name, number of videos, duration, and email ID.

After processing:
- A mashup `.mp3` file is created  
- The mashup is compressed into a `.zip` file  
- The ZIP is sent to the user's email using **SendGrid**  
  *(If email sending fails, a download link is shown as a backup)*  

---

### Features
- User-friendly web form  
- Email validation using `email-validator`  
- ZIP file generation  
- Optional download link backup system  
- Deployed on **Render** cloud platform  

---

### Input
- Singer Name  
- Number of videos (n)  
- Duration of each clip (y seconds)  
- Email ID  

---

### Output
- Mashup ZIP file sent to email  
- Backup download link shown on website  

---

### Deployment (Program 2)
The web service is deployed on **Render** using Docker.  
Environment variables required:
- `SENDGRID_API_KEY`  
- `FROM_EMAIL`  

---

### Tech Stack Used
- Python  
- Flask  
- yt-dlp  
- ffmpeg  
- pydub  
- SendGrid API  
- Docker  
- Render Cloud Hosting


 ### Screenshot of website

<img width="1847" height="876" alt="image" src="https://github.com/user-attachments/assets/07286a0d-647f-4966-80f5-981613c7c6b2" />


---

### Link

https://mashup-web.onrender.com/

### Notes
- On free cloud hosting platforms, YouTube sometimes blocks automated downloads due to bot detection.  
- In that case, the mashup may work correctly on local system but fail on Render server.  
- Download link expires after some time because Render free instances restart.


# Author

Sommit
