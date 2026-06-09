import os
import wave

def check_audio(file_path):
    # 1. Check if the file actually exists on the system
    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found!"}
        
    # 2. Check if the file is empty (size is 0 bytes)
    if os.path.getsize(file_path) == 0:
        return {"status": "error", "message": "File is empty or chunk is incomplete."}

    # 3. Check the file extension (We only support WAV for now)
    filename = os.path.basename(file_path)
    if not filename.lower().endswith('.wav'):
        return {"status": "error", "message": "Unsupported format! Only .wav files are allowed."}

    # 4. Try to open the file to check for corruption or damage
    try:
        # wave.open will crash if the WAV header or stream is corrupted
        with wave.open(file_path, 'rb') as f:
            channels = f.getnchannels()
            rate = f.getframerate()
            frames = f.getnframes()
            
            # If frames are 0, it means the audio has no data inside
            if frames == 0:
                return {"status": "error", "message": "Audio is corrupted, found 0 frames."}
                
            # Simple formula to calculate duration
            duration = frames / float(rate)
            
            # If everything goes well, return the success data
            return {
                "status": "success",
                "message": "Audio is completely valid!",
                "duration": round(duration, 2),
                "channels": channels,
                "sample_rate": rate
            }
            
    except Exception as e:
        # If wave.open fails, the file is either broken or not a real WAV
        return {"status": "error", "message": "File is damaged or format is invalid."}


# --- TESTING THE CODE ---
if __name__ == "__main__":
    # Create a fake wav file containing text to test the error handling
    test_file = "test_song.wav"
    
    with open(test_file, "w") as f:
        f.write("This is just a fake text file, not a real audio file!")

    # Run the function on the fake file
    print("Testing with fake file:")
    result = check_audio(test_file)
    print(result)

    # Clean up and delete the test file
    if os.path.exists(test_file):
        os.remove(test_file)