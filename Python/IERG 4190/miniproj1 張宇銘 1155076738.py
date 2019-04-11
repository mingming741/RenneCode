#!/usr/bin/env python
""" About this project, I discussed with Hu Zixuan(1155043803),Yang Shihuan(1155076733).
        It is the first time that I use python. I use spyder as the editer and test many
    times. I discuss this with my classmate together and finally we get answer like this
"""
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
# import additional packages as needed

def load_wave(filename):
    """Load a wave signal from a specified file.
        This function should return a pair as (rate, x),
        where:
        - rate: the sampling rate
        - x:    a vector that represents a sample sequence.
    """
    (rate, x) = scipy.io.wavfile.read(filename, mmap=False)
    return rate, x
    pass

def find_note_begins(x):
    """Find the beginning index of each chunk.
        This function should return a vector of indices,
        where each index corresponds to the begining of a chunk.
    """
    y = x[:, 0:1]
    index_arr = []
    peak_threshold = 2800
    time_threshold = 8000
    peak_value = 0
    index_value = 0
    i = 0
    while i < len(y) :
        if y[i] > peak_threshold :        
            peak_value = y[i]
            index_value = i
            j = i
            while j < i + time_threshold :             
                if y[j] > peak_value :
                    peak_value = y[j]
                    index_value = j
                j = j + 1
            index_arr.append(index_value)
            i = i + time_threshold
        else :
            i = i + 1
    return index_arr
    pass

def compute_principal_freq(x, rate, b):
    """Compute the principal frequency of a chunk.
        Arguments:
        - x:        The vector of samples
        - rate:     The sampling rate
        - b:        The begining of a chunk.
        This function returns the principal frequency of a chunk,
        in terms of Hertz.
        Note:
        - You can fix the chunk length to be 16384.
    """
    y = x[:, 0]  
    time_threshold = 16384
    z = y[b:b+time_threshold] 
    fz = np.fft.fft(z) 
    freq = np.fft.fftfreq(len(fz)) 
    max_ampitude = 0
    max_index = 0
    i = 0
    while i < len(fz):
        if abs(fz[i]) > max_ampitude :
            max_ampitude = abs(fz[i])
            max_index = i
        i = i + 1  
    pri_freq = freq[max_index]
    return abs(pri_freq * rate)
    pass


def analyze_wave(filename):
    """Complete the whole analysis procedure.
        This function returns a tuple comprised of
        three parts:
        - x:            The loaded sequence of samples
        - note_begins:  The beginning index of each chunk
        - note_freqs:   The principal frequency of each chunk
    """
    # Step 1: Load wave from file
    (rate, x) = load_wave(filename)
    # Step 2: find the begining position of each note
    note_begins = find_note_begins(x)
    # Step 3: compute the principal frequency of each note
    note_freqs = [compute_principal_freq(x, rate, b) for b in note_begins]
    # return results
    return x, note_begins, note_freqs

if __name__ == '__main__':
    # main script
    x, note_begins, note_freqs = analyze_wave("cnotes.wav")
    # Step 2: find the begining position of each note 
    n = len(note_begins)
    assert len(note_freqs) == n
    # display the results
    for i in range(n):
        b = note_begins[i]
        f = note_freqs[i]
        print "Note %2d:  begins at %6d,  freq = %.1f" % (i, b, f)
    # plotting the note beginning positions
    # (please comment out this part if you don't want to see the plots)
    plt.plot(
        range(len(x)), x, 'b-',
        note_begins, x[note_begins], 'r+', markersize=16)
    plt.show()
