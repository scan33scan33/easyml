import aifc
import logging
import numpy
import os
import wave
import matplotlib.pyplot as plt

N_POS_SAMPLES = 1
N_NEG_SAMPLES = 1
N_TEST_SAMPLES = 1
# AUDIO_LENGTH = 10000
FFT_LENGTH = 5

def GetFeatures(filename):
    audio = wave.open(filename, 'r')
    n_frame = audio.getnframes()
    signal = audio.readframes(n_frame)
    audio.close()
    # Make MSB/LSB thing right
    y = numpy.fromstring(signal, numpy.short).byteswap()
    ffty = abs(numpy.fft.fft(y)[:FFT_LENGTH])
    ffty = ffty / sum(abs(ffty)) 
    plt.plot(range(FFT_LENGTH), ffty)
    plt.show()
    return ffty 

if __name__ == '__main__':
    # Data collection phase: get some positive examples and negative examples
    for i in range(N_POS_SAMPLES):
        print "Press Enter to Accept Input"
        raw_input()
        os.system('arecord /tmp/pos_%d.wav' % i)
    for i in range(N_NEG_SAMPLES):
        print "Press Enter to Accept Input"
        raw_input()
        os.system('arecord /tmp/neg_%d.wav' % i)
    # Feature extraction phase: do FFT
    pos_samples = []
    neg_samples = []
    for i in range(N_POS_SAMPLES):
        pos_samples.append(GetFeatures('/tmp/pos_%d.wav' % i))
    for i in range(N_NEG_SAMPLES):
        neg_samples.append(GetFeatures('/tmp/neg_%d.wav' % i))
    # Training phase: perceptron baseline
    w = numpy.array([0] * FFT_LENGTH)
    for i in range(N_POS_SAMPLES):
        x = pos_samples[i]
        p = 1.0 - float(numpy.dot(w, x) > 0)
        w = w + p * x
    for i in range(N_NEG_SAMPLES):
        x = neg_samples[i]
        p = -float(numpy.dot(w, x) > 0)
        w = w + p * x
    # Testing phase: get some random samples to classify 
    print "Press Enter to Accept Input"
    raw_input()
    os.system('arecord /tmp/test.wav')
    x = GetFeatures('/tmp/test.wav')
    print numpy.dot(w, x), numpy.dot(w, x) > 0 and "Class 1" or "Class 2"
