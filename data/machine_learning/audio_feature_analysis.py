import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load an audio file
audio_path = 'path_to_your_audio_file.wav'
y, sr = librosa.load(audio_path)

# Extract audio features
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
chroma = librosa.feature.chroma_stft(y=y, sr=sr)
mfcc = librosa.feature.mfcc(y=y, sr=sr)
spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

# Plot some of the features
plt.figure(figsize=(12, 8))

plt.subplot(4, 1, 1)
librosa.display.specshow(chroma, y_axis='chroma')
plt.colorbar()
plt.title('Chromagram')

plt.subplot(4, 1, 2)
librosa.display.specshow(mfcc)
plt.colorbar()
plt.title('MFCC')

plt.subplot(4, 1, 3)
plt.plot(librosa.times_like(spectral_centroid), spectral_centroid)
plt.title('Spectral Centroid')

plt.subplot(4, 1, 4)
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr)
librosa.display.specshow(tempogram, x_axis='time', y_axis='tempo')
plt.colorbar()
plt.title('Tempogram')

plt.tight_layout()
plt.show()
