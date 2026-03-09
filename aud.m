% === GESTURE-TO-SPEECH DEMO (Complete + Voice Output) ===
clear; close all; clc;

% 1. SIMULATE GESTURE (MPU6050-like)
Fs = 50; t = 0:1/Fs:2;
gesture_wave = sin(2*pi*2*t) + 0.2*randn(size(t));
figure(1); plot(t, gesture_wave); 
title('Simulated Wave Gesture (MPU6050 X-accel)'); 
xlabel('Time (s)'); ylabel('Accel (g)'); grid on;

% 2. CLASSIFY GESTURE
energy = sum(gesture_wave.^2);
if energy > 5
    detected_gesture = 'wave'; word = 'What??';
else
    detected_gesture = 'idle'; word = '';
end
fprintf('Detected: %s → "%s"\n', detected_gesture, word);

% 3. TEXT-TO-SPEECH (Windows Native - NO TOOLBOX NEEDED)
if ~isempty(word)
    % Add Windows Speech Assembly
    NET.addAssembly('System.Speech');
    
    % Create speech synthesizer
    obj = System.Speech.Synthesis.SpeechSynthesizer;
    obj.Volume = 100;      % 0-100
    obj.Rate = 0;          % -10 to +10
    
    % SPEAK "hi" - YOU WILL HEAR IT!
    Speak(obj, word);
    fprintf('✅ SPEAKING: %s\n', word);
    
    % ALSO generate FSK for demo
    fc1 = 1200; fc2 = 2200; Fs_audio = 8000; duration_bit = 0.02;
    word_ascii = uint8(word);  
    word_bits = dec2bin(word_ascii, 8) - '0'; 
    word_bits = word_bits(:)';  
    
    fsk_sig = [];
    for bit = word_bits
        t_bit = 0:1/Fs_audio:duration_bit-1/Fs_audio;
        if bit == 1
            fsk_sig = [fsk_sig, sin(2*pi*fc1*t_bit)];  
        else
            fsk_sig = [fsk_sig, sin(2*pi*fc2*t_bit)];  
        end
    end
    
    % FSK Visualization
    figure(2); 
    subplot(2,1,1); plot((0:length(fsk_sig)-1)/Fs_audio, fsk_sig); 
    title('FSK Signal Time Domain ("hi")'); xlabel('Time (s)'); grid on;
    subplot(2,1,2); spectrogram(fsk_sig,128,120,256,Fs_audio,'yaxis');
    title('FSK Spectrum');
    
    % Play FSK tones too (optional)
    sound(fsk_sig, Fs_audio);
    
else
    fprintf('❌ No gesture detected\n');
end

