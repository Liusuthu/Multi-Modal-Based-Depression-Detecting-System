import gradio as gr
import torch
import time
import numpy as np
import mediapipe as mp
from PIL import Image
import cv2
# from pytorch_grad_cam.utils.image import show_cam_on_image
import scipy.io.wavfile as wav
# Importing necessary components for the Gradio app
from model import pth_model_static, pth_model_dynamic, cam, pth_processing
from face_utils import get_box, display_info
from config import DICT_EMO, config_data
from plot import statistics_plot
from moviepy.editor import AudioFileClip

import soundfile as sf
import torchaudio
from speechbrain.pretrained.interfaces import foreign_class
from paraformer import AudioReader, CttPunctuator, FSMNVad, ParaformerOffline
from gradio_client import Client
##############################################################################################
client = Client("Liusuthu/TextDepression")

mp_face_mesh = mp.solutions.face_mesh


classifier = foreign_class(
    source="pretrained_models/local-speechbrain/emotion-recognition-wav2vec2-IEMOCAP",  # ".\\emotion-recognition-wav2vec2-IEMOCAP"
    pymodule_file="custom_interface.py",
    classname="CustomEncoderWav2vec2Classifier",
    savedir="pretrained_models/local-speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
)
ASR_model = ParaformerOffline()
vad = FSMNVad()
punc = CttPunctuator()


#########################################################################################
def text_api(text:str):
    result = client.predict(
        text,  # str  in '输入文字' Textbox component
        api_name="/predict",
    )
    return result

#######################################################################
#规范函数，只管值输入输出：
def text_score(text):
    if text==None:
        gr.Warning("提交内容为空！")
    else:
        string=text_api(text)
        part1 = str.partition(string, r"text")
        want1 = part1[2]
        label = want1[4:6]
        part2 = str.partition(string, r"probability")
        want2 = part2[2]
        prob = float(want2[3:-4])
        if label=="正向":
            score=-np.log10(prob*10)
        else:
            score=np.log10(prob*10)
        # print("from func:text_score————,text:",text,",score:",score)
        return text,score

def speech_score(audio):
    if audio==None:
        gr.Warning("提交内容为空！请等待音频加载完毕后再尝试提交！")
    else:
        print(type(audio))
        print(audio)
        sample_rate, signal = audio  # 这是语音的输入
        signal = signal.astype(np.float32)
        signal /= np.max(np.abs(signal))
        sf.write("data/a.wav", signal, sample_rate)
        signal, sample_rate = torchaudio.load("data/a.wav")
        signal1 = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(
            signal
        )
        torchaudio.save("data/out.wav", signal1, 16000, encoding="PCM_S", bits_per_sample=16)
        Audio = "data/out.wav"
        speech, sample_rate = AudioReader.read_wav_file(Audio)
        if signal == "none":
            return "none", "none", "haha"
        else:
            segments = vad.segments_offline(speech)
            text_results = ""
            for part in segments:
                _result = ASR_model.infer_offline(
                    speech[part[0] * 16 : part[1] * 16], hot_words="任意热词 空格分开"
                )
                text_results += punc.punctuate(_result)[0]
    
            out_prob, score, index, text_lab = classifier.classify_batch(signal1)
            print("from func:speech_score————type and value of prob:")
            print(type(out_prob.squeeze(0).numpy()))
            print(out_prob.squeeze(0).numpy())
            print("from func:speech_score————type and value of resul_label:")
            print(type(text_lab[-1]))
            print(text_lab[-1])
            #return text_results, out_prob.squeeze(0).numpy(), text_lab[-1], Audio
            prob=out_prob.squeeze(0).numpy()
            #print(prob)
            score2=10*prob[0]-10*prob[1]
            if score2>=0:
                score2=np.log10(score2)
            else:
                score2=-np.log10(-score2)
            # print("from func:speech_score————score2:",score2)
            # print("from func:speech_score————",text_lab[-1])
            
            text,score1=text_score(text_results)
            # # text_emo=str(get_text_score(text_results))
            # print("from func:speech_score————text:",text,",score1:",score1)
            score=(2/3)*score1+(1/3)*score2
            
    
            return text,score


def video_score(video):
    if video==None:
        gr.Warning("提交内容为空！请等待视频加载完毕后再尝试提交！")
    else:
        cap = cv2.VideoCapture(video)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = np.round(cap.get(cv2.CAP_PROP_FPS))
    
        path_save_video_face = 'result_face.mp4'
        vid_writer_face = cv2.VideoWriter(path_save_video_face, cv2.VideoWriter_fourcc(*'mp4v'), fps, (224, 224))
    
        # path_save_video_hm = 'result_hm.mp4'
        # vid_writer_hm = cv2.VideoWriter(path_save_video_hm, cv2.VideoWriter_fourcc(*'mp4v'), fps, (224, 224))
    
        lstm_features = []
        count_frame = 1
        count_face = 0
        probs = []
        frames = []
        last_output = None
        last_heatmap = None 
        cur_face = None
    
        with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    
            while cap.isOpened():
                _, frame = cap.read()
                if frame is None: break
    
                frame_copy = frame.copy()
                frame_copy.flags.writeable = False
                frame_copy = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(frame_copy)
                frame_copy.flags.writeable = True
    
                if results.multi_face_landmarks:
                    for fl in results.multi_face_landmarks:
                        startX, startY, endX, endY  = get_box(fl, w, h)
                        cur_face = frame_copy[startY:endY, startX: endX]
    
                        if count_face%config_data.FRAME_DOWNSAMPLING == 0:
                            cur_face_copy = pth_processing(Image.fromarray(cur_face))
                            with torch.no_grad():
                                features = torch.nn.functional.relu(pth_model_static.extract_features(cur_face_copy)).detach().numpy()
    
                            # grayscale_cam = cam(input_tensor=cur_face_copy)
                            # grayscale_cam = grayscale_cam[0, :]
                            # cur_face_hm = cv2.resize(cur_face,(224,224), interpolation = cv2.INTER_AREA)
                            # cur_face_hm = np.float32(cur_face_hm) / 255
                            # heatmap = show_cam_on_image(cur_face_hm, grayscale_cam, use_rgb=False)
                            # last_heatmap = heatmap
            
                            if len(lstm_features) == 0:
                                lstm_features = [features]*10
                            else:
                                lstm_features = lstm_features[1:] + [features]
    
                            lstm_f = torch.from_numpy(np.vstack(lstm_features))
                            lstm_f = torch.unsqueeze(lstm_f, 0)
                            with torch.no_grad():
                                output = pth_model_dynamic(lstm_f).detach().numpy()
                            last_output = output
    
                            if count_face == 0:
                                count_face += 1
    
                        else:
                            if last_output is not None:
                                output = last_output
                                # heatmap = last_heatmap
    
                            elif last_output is None:
                                output = np.empty((1, 7))
                                output[:] = np.nan
                                
                        probs.append(output[0])
                        frames.append(count_frame)
                else:
                    if last_output is not None:
                        lstm_features = []
                        empty = np.empty((7))
                        empty[:] = np.nan
                        probs.append(empty)
                        frames.append(count_frame)                        
    
                if cur_face is not None:
                    # heatmap_f = display_info(heatmap, 'Frame: {}'.format(count_frame), box_scale=.3)
    
                    cur_face = cv2.cvtColor(cur_face, cv2.COLOR_RGB2BGR)
                    cur_face = cv2.resize(cur_face, (224,224), interpolation = cv2.INTER_AREA)
                    cur_face = display_info(cur_face, 'Frame: {}'.format(count_frame), box_scale=.3)
                    vid_writer_face.write(cur_face)
                    # vid_writer_hm.write(heatmap_f)
    
                count_frame += 1
                if count_face != 0:
                    count_face += 1
    
            vid_writer_face.release()
            # vid_writer_hm.release()
    
            stat = statistics_plot(frames, probs)
    
            if not stat:
                return None, None
    
        #for debug
        print("from func:video_score————")
        print(type(frames))
        print(frames)
        print(type(probs))
        print(probs)        
        # to calculate scores
        nan=float('nan')
        s1 = 0
        s2 = 0
        s3 = 0
        # s4 = 0
        # s5 = 0
        # s6 = 0
        # s7 = 0
        frames_len=len(frames)
        for i in range(frames_len):
            if np.isnan(probs[i][0]):
                frames_len=frames_len-1
            else: 
                s1=s1+probs[i][0]
                s2=s2+probs[i][1]
                s3=s3+probs[i][2]
                # s4=s4+probs[i][3]
                # s5=s5+probs[i][4]
                # s6=s6+probs[i][5]
                # s7=s7+probs[i][6]
        s1=s1/frames_len
        s2=s2/frames_len
        s3=s3/frames_len
        # s4=s4/frames_len
        # s5=s5/frames_len
        # s6=s6/frames_len
        # s7=s7/frames_len
        # scores=[s1,s2,s3,s4,s5,s6,s7]
        # scores_str=str(scores)
        # score1=0*scores[0]-8*scores[1]+4*scores[2]+0*scores[3]+2*scores[4]+2*scores[5]+4*scores[6]
        #print("from func:video_score————score1=",score1)
        #print("from func:video_score————logs:")
        # with open("local_data/data.txt",'a', encoding="utf8") as f:
        #     f.write(scores_str+'\n')
    
        # with open("local_data/data.txt",'r', encoding="utf8") as f:
        #     for i in f:
        #         print(i)
    
    
        print(str([s1,s2,s3]))
        if s1>=0.4:
            score1=0
        else:
            if s2>=s3:
                score1=-1
            else:
                score1=+1
        #trans the audio file
        my_audio_clip = AudioFileClip(video)
        my_audio_clip.write_audiofile("data/audio.wav",ffmpeg_params=["-ac","1"])
    
        audio = wav.read('data/audio.wav')
    
        text,score2=speech_score(audio)
    
        #print("from func:video_score————text:",text)
    
        score=(score1+6*score2)/7
        #print("from func:video_score————score:",score)
        return text,score
#######################################################################

