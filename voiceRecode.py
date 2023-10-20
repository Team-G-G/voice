import pyaudio
import wave
import io
import os
import keyboard
import speech_recognition as sr

# PyAudio 설정
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
OUTPUT_FILENAME = "recorded_audio.wav"
OUTPUT_TEXT_FILENAME = "transcribed_text.txt"
recording = False

# Google Cloud Speech-to-Text API 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your_service_account_key.json'

# 녹음 시작


def start_recording():
    global recording
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("녹음 시작...")
    frames = []

    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    print("오디오 파일이 WAV 형식으로 저장되었습니다.")
    transcribe_audio()

# 녹음 중지


def stop_recording():
    global recording
    recording = False

# Google Cloud Speech-to-Text API를 사용하여 음성을 텍스트로 변환


def transcribe_audio():
    r = sr.Recognizer()
    with sr.AudioFile(OUTPUT_FILENAME) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google_cloud(audio)
        print("음성을 텍스트로 변환한 결과:")
        print(text)
        with open(OUTPUT_TEXT_FILENAME, "w") as text_file:
            text_file.write(text)
        print("텍스트가 파일로 저장되었습니다.")
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        print(f"Google Cloud Speech API 오류: {e}")


while True:
    try:
        if keyboard.is_pressed('a'):
            print("녹음을 시작합니다...")
            recording = True
            start_recording()
        elif keyboard.is_pressed('s'):
            if recording:
                print("녹음을 중지합니다...")
                stop_recording()
        else:
            pass
    except:
        break
