from tkinter import Tk, Label, Button, messagebox, Frame
from tkinter.filedialog import askopenfilename, asksaveasfilename
import moviepy as mp
import os

root = Tk()
root.geometry("400x200")
root.minsize(600, 400)
root.maxsize(600, 400)
root.title("Video to Audio Converter COOL STUFF")

# Main frame
main_frame = Frame(root, padx=20, pady=20)
main_frame.pack(expand=True, fill="both")

# Title label
title_label = Label(main_frame, text="Video to Audio Converter", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Input file label
input_label = Label(main_frame, text="No file selected", font=("Arial", 10), fg="gray")
input_label.pack(pady=5)

# Button frame
button_frame = Frame(main_frame)
button_frame.pack(pady=20)

def select_video():
    file_path = askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")])
    if file_path:
        input_label.config(text=os.path.basename(file_path), fg="black")
        # store selected video path in module-level variable to avoid assigning new attributes to Tk instance
        global video_file
        video_file = file_path

def convert_to_audio():
    try:
        video_path = video_file
    except NameError:
        messagebox.showerror("Error", "Please select a video file first")
        return
    
    output_path = asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav"), ("All files", "*.*")])
    if output_path:
        try:
            video = mp.VideoFileClip(video_path)
            audio = video.audio
            if audio is not None:
                # call without verbose/logger kwargs to avoid unexpected keyword errors
                audio.write_audiofile(output_path)
                messagebox.showinfo("Success", "Audio extracted successfully!")
            else:
                messagebox.showerror("Error", "Video file has no audio track")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

# Buttons
select_btn = Button(button_frame, text="Select Video", command=select_video, width=20, bg="#4CAF50", fg="white", font=("Arial", 10))
select_btn.pack(pady=5)

convert_btn = Button(button_frame, text="Convert to Audio", command=convert_to_audio, width=20, bg="#2196F3", fg="white", font=("Arial", 10))
convert_btn.pack(pady=5)

root.mainloop()