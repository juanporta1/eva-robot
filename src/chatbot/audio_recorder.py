import pyaudio
import wave

# Configurar los parámetros de grabación
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "grabacion.wav"

# Inicializar PyAudio
audio = pyaudio.PyAudio()

# Configurar la grabación
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("Grabando...")



print("Grabación finalizada.")

# Detener y cerrar el stream de audio
stream.stop_stream()
stream.close()
audio.terminate()

# Guardar la grabación en un archivo WAV

