# -*- coding:utf-8 -*-
import logging

from paraformer import AudioReader, CttPunctuator, FSMNVad, ParaformerOffline
import numpy as np
import sounddevice as sd
import time
import soundfile as sf
import chardet
import torch

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(levelname)s] [%(filename)s:%(lineno)d %(module)s.%(funcName)s] %(message)s",
)
recorded_audio = []
sample_rate = 16000

def luyin():
    def callback(indata, frames, time, status):
        if status:
            print('录音错误:', status)
        if recording:
            # 将录音数据追加到变量中
            # if indata.copy()>1.5 or indata.copy()< -1.5:
            arr = np.array(indata.copy())  # 假设数组中有416个元素

            sum_value = np.sum(arr)


            recorded_audio.append(indata.copy())

    a = int(input('请输入数字1开始:'))
    if a == 1:
        recording = True
        stream = sd.InputStream(callback=callback, channels=1, samplerate=sample_rate, blocksize=4096)
        stream.start()
        begin = time.time()
        b = int(input('请输入数字2停止:'))
        if b == 2:
            recording = False
            print("Stop recording")
            stream.stop()
            fina = time.time()
            t = fina - begin
            print('录音时间为%ds' % t)
            # print(recorded_audio)
            if len(recorded_audio) == 0:
                return "none"
            else:
                signal = np.vstack(recorded_audio)




                sf.write("out.wav",np.array(signal),sample_rate)
                # signal = torch.from_numpy(np.squeeze(signal)).float()
                # print(signal)
                # # result = chardet.detect(signal)
                # # print(result['encoding'])
                # recorded_audio.clear()
                return signal



if __name__ == "__main__":
    logging.info("Testing offline asr")
    luyin()
    audio = "out.wav"
    speech, sample_rate = AudioReader.read_wav_file(audio)
    model = ParaformerOffline()
    vad = FSMNVad()
    punc = CttPunctuator()

    segments = vad.segments_offline(speech)
    results = ""
    for part in segments:
        _result = model.infer_offline(
            speech[part[0] * 16 : part[1] * 16], hot_words="任意热词 空格分开"
        )
        results += punc.punctuate(_result)[0]
    logging.info(results)





