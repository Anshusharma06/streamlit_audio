import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io.wavfile import read, write
import io
import wave

audio_file = st.file_uploader("Choose a File", type="wav")
if audio_file is not None:
    audio_bytes = audio_file.read()
    samplerate, sig = read(io.BytesIO(audio_bytes))
    sig = sig[:,0]
    
    st.write(f"rate: {samplerate} Hz")
    n = len(sig)
    st.write(f"number of samples: {n}")
    length = n / samplerate
    st.write(f"length: {length} s")
    t = np.linspace(0., length, n)
    

    f_orig, Pxx_den_orig = signal.periodogram(sig, fs=samplerate)

    cutoff =  st.sidebar.slider("Cutoff frequency [Hz]", 1., 10000., 500.)
    order =  st.sidebar.slider("Order: ", 1, 10, 3)
    
    
    b, a = signal.butter(order, cutoff, 'lp', fs=samplerate)

    y = signal.filtfilt(b, a, sig)
    
    plt.plot(t, sig, t, y)
    plt.legend(('Original', 'Filtered'), loc='best')
    plt.grid(True)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    st.pyplot()

    f, Pxx_den = signal.periodogram(y, fs=samplerate)
    plt.semilogy(f_orig, Pxx_den_orig, f, Pxx_den)
    plt.legend(('Original', 'Filtered'), loc='best')
    plt.grid()
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    st.pyplot()


