import numpy as np
import soundfile as sf
import torchaudio
from speechbrain.pretrained.interfaces import foreign_class

from app_utils import video_score,speech_score,text_score


# import scipy.io.wavfile as wav
# from paraformer import AudioReader, CttPunctuator, FSMNVad, ParaformerOffline

# from gradio_client import Client





import gradio as gr
import os
from consult_func import (
    advice,
    visibility,
    visibility3,
    visibility4,
    visibility_choice,
    visibility_choice2,
    visibility_choice3,
    visibility_choice4,
    visibility_choice5,
    keyword,
    save2,
)

os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
# client = Client("Liusuthu/TextDepression")


# classifier = foreign_class(
#     source="pretrained_models/local-speechbrain/emotion-recognition-wav2vec2-IEMOCAP",  # ".\\emotion-recognition-wav2vec2-IEMOCAP"
#     pymodule_file="custom_interface.py",
#     classname="CustomEncoderWav2vec2Classifier",
#     savedir="pretrained_models/local-speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
# )
# ASR_model = ParaformerOffline()
# vad = FSMNVad()
# punc = CttPunctuator()

#########################################################################################
#第四题专用函数：(经过调整，第五题也可以用)
def text_score4(text):
    text,score=text_score(text)
    return text,score,gr.Column(visible=True),text,score


def speech_score4(audio):
    text,score=speech_score(audio)
    return text,score,gr.Column(visible=True),text,score


def video_score4(video):
    text,score=video_score(video)
    return text,score,gr.Column(visible=True),text,score
#########################################################################################
#第三题专用函数：（融入keyword识别）
def text_score3(text):
    text,score=text_score(text)
    if keyword(text):
        return text,score,gr.Radio(visible=True), gr.Column(visible=False),text,score
    else:
        return text,score,gr.Radio(visible=False), gr.Column(visible=True),text,score

def speech_score3(audio):
    text,score=speech_score(audio)
    if keyword(text):
        return text,score,gr.Radio(visible=True), gr.Column(visible=False),text,score
    else:
        return text,score,gr.Radio(visible=False), gr.Column(visible=True),text,score

def video_score3(video):
    text,score=video_score(video)
    if keyword(text):
        return text,score,gr.Radio(visible=True), gr.Column(visible=False),text,score
    else:
        return text,score,gr.Radio(visible=False), gr.Column(visible=True),text,score
#########################################################################################
def clear_info():
    return (
        gr.Textbox(""),
        gr.Textbox(""),
        gr.Textbox(""),
    )
# constants
schema = "情感倾向[正向，负向]"  # Define the schema for sentence-level sentiment classification


with gr.Blocks() as consult:
    result1=gr.Number(label="第一道问答题分数",interactive=True,visible=False)
    text1=gr.Textbox(label="第一道问答题回答内容",interactive=True,visible=False)
    result2=gr.Number(label="第二道问答题分数",interactive=True,visible=False)
    text2=gr.Textbox(label="第二道问答题回答内容",interactive=True,visible=False)
    result3=gr.Number(label="第三道问答题分数",interactive=True,visible=False)
    text3=gr.Textbox(label="第三道问答题回答内容",interactive=True,visible=False)
    gr.Markdown(
        "欢迎来到这里，接下来我们来放松地聊聊天，你只要如实完整地回答我的问题就好了。"
    )
    btn1 = gr.Button("开始")
    with gr.Column(visible=False) as questions:
        # 睡眠问题
        title1 = gr.Markdown("# 睡眠")
        radio1 = gr.Radio(
            ["充足", "不足"],
            label="你最近睡眠还充足吗？",
            type="index",
            interactive=True,
        )
        with gr.Column(visible=False) as q1_1:
            radio2 = gr.Radio(
                ["存在", "不存在"],
                label="你会存在嗜睡的情况吗？比如容易一直睡过整个上午甚至一直持续睡到下午？",
                interactive=True,
            )
        with gr.Column(visible=False) as q1_2:
            radio3 = gr.Radio(
                ["不存在", "失眠", "早醒"],
                label="你是否存在失眠或早醒的情况？",
                interactive=True,
            )
        adv1 = gr.Textbox(visible=False)

        # 饮食问题
        title2 = gr.Markdown("# 饮食", visible=False)
        radio4 = gr.Radio(
            [
                "食欲正常，没有体重上的明显变化",
                "食欲亢进，体重增加",
                "食欲不振，体重减轻",
            ],
            type="index",
            label="你最近食欲如何？有任何体重上的变化吗？",
            visible=False,
            interactive=True,
        )

        # 情绪问题
        title3 = gr.Markdown("# 情绪", visible=False)
        radio5 = gr.Radio(
            ["好", "不好"], label="你最近心情还好吗？", visible=False, interactive=True
        )
        radio6 = gr.Radio(
            ["一周以内", "一周至两周", "两周以上"],
            label="你心情不好持续了多长时间呢？",
            visible=False,
            interactive=True,
        )
        with gr.Column(visible=False) as q3_2:
            gr.Markdown(
                "你这段时间真的很不容易，愿意和我说说吗？说什么都可以，也许倾诉出来会好一些呢"
            )
            radio7 = gr.Radio(
                ["文本", "语音", "视频"],
                label="请选择以哪种方式回答",
                type="index",
                interactive=True,
            )
            with gr.Column(visible=False) as ans3_1:  # 文本回答
                text3_1 = gr.Textbox(interactive=True)
                btn3_1 = gr.Button("抱抱你")
                result3_11 = gr.Textbox(label="转录结果3_1",visible=False)
                result3_12 = gr.Textbox(label="分数结果3_1",visible=False)
            # 请把audio3_2换成Audio组件
            with gr.Column(visible=False) as ans3_2:  # 语音回答
                audio3_2 = gr.Audio(
                    label="语音录制(录制结束后，请等待语音条闪烁并出现波形后再提交)", interactive=True, sources=["microphone"]
                )  # 对应out_prob.squeeze(0).numpy()[0]
                btn3_2 = gr.Button("抱抱你")
                result3_21 = gr.Textbox(label="转录结果3_2")
                result3_22 = gr.Textbox(label="分数结果3_2",visible=False)
            # 请把video3_3换成Video组件
            with gr.Column(visible=False) as ans3_3:  # 视频回答
                video3_3 = gr.Video(
                    sources=["webcam", "upload"],
                    interactive=True,
                    format='mp4',
                    width=500,
                    label="视频录制(录制结束后，请等待画面闪烁并再次出现后再提交)",
                )
                btn3_3 = gr.Button("继续")
                result3_31 = gr.Textbox(label="转录结果3_3")
                result3_32 = gr.Textbox(label="分数结果3_3",visible=False)

        # 自杀倾向问题
        radio8 = gr.Radio(
            ["想过", "没想过"],
            label="你想过死吗?",
            visible=False,
            type="index",
            interactive=True,
        )
        radio9 = gr.Radio(
            ["想过", "没想过"],
            label="那你想过怎么死吗？",
            visible=False,
            type="index",
            interactive=True,
        )
        radio10 = gr.Radio(
            [
                "没想过",
                "想过，没想过具体时间和地点",
                "想过具体做法，时间和地点，没实践过",
                "实践过",
            ],
            label="那你想过具体的做法吗？",
            visible=False,
        )
        dead_hug = gr.Markdown(
            "很抱歉听到这些话，我们非常理解并关心你的情绪，我们明白产生自杀念头的原因是复杂的，并不是你的过错。如果你愿意的话，可以多来找我们聊聊天，我们愿意充当你的知心好友，并且承诺对你说的所有话严格保密。如果可以的话，我们还建议你积极寻求专业心理医生的帮助，和他们聊聊天，讲讲自己的感受。加油！\n",
            visible=False,
        )

        # 兴趣爱好
        with gr.Column(visible=False) as q4:
            title4 = gr.Markdown("# 兴趣爱好")
            gr.Markdown("你有什么兴趣爱好吗？平常都喜欢干什么事情呢？愿意和我说说吗？")
            radio11 = gr.Radio(
                ["文本", "语音", "视频"],
                label="请选择以哪种方式回答",
                type="index",
                interactive=True,
            )
            with gr.Column(visible=False) as ans4_1:
                text4_1 = gr.Textbox(interactive=True)
                btn4_1 = gr.Button("继续")
                result4_11 = gr.Textbox(label="结果4_1",visible=False)
                result4_12 = gr.Textbox(label="分数结果4_1",visible=False)
            # 请把audio4_2换成Audio组件
            with gr.Column(visible=False) as ans4_2:
                audio4_2 = gr.Audio(
                    label="语音录制(录制结束后，请等待语音条闪烁并出现波形后再提交)", interactive=True, sources=["microphone"]
                )  # 对应out_prob.squeeze(0).numpy()[0]
                btn4_2 = gr.Button("继续")
                result4_21 = gr.Textbox(label="转录结果4_2")
                result4_22 = gr.Textbox(label="分数结果4_2",visible=False)
            # 请把video4_3换成Video组件
            with gr.Column(visible=False) as ans4_3:
                video4_3 = gr.Video(
                    sources=["webcam", "upload"],
                    interactive=True,
                    format='mp4',
                    width=500,
                    label="视频录制(录制结束后，请等待画面闪烁并再次出现后再提交)",                    
                )
                btn4_3 = gr.Button("继续")
                result4_31 = gr.Textbox(label="转录结果4_3")
                result4_32 = gr.Textbox(label="分数结果4_3",visible=False)

        # 针对无价值感、无意义感、无力感

        with gr.Column(visible=False) as q5:
            title5 = gr.Markdown("# 近期情况")
            gr.Markdown(
                "你愿意和我聊聊你最近都喜欢干些什么，或者有什么事情让你很沉浸，感到开心或者觉得很有意义吗？还有那些让你觉得自己很厉害，很有成就感的事情,比如说你做成了什么有难度的事情或者帮助了谁？什么都可以哦"
            )
            radio12 = gr.Radio(
                ["文本", "语音", "视频"],
                label="请选择以哪种方式回答",
                type="index",
                interactive=True,
            )
            with gr.Column(visible=False) as ans5_1:
                text5_1 = gr.Textbox(interactive=True)
                btn5_1 = gr.Button("提交")
                result5_11 = gr.Textbox(label="转录结果5_1",visible=False)
                result5_12 = gr.Textbox(label="分数结果5_1",visible=False)
            # 请把audio5_2换成Audio组件
            with gr.Column(visible=False) as ans5_2:
                audio5_2 = gr.Audio(
                    label="语音录制(录制结束后，请等待语音条闪烁并出现波形后再提交)", interactive=True, sources=["microphone"],
                )  # 对应out_prob.squeeze(0).numpy()[0]
                btn5_2 = gr.Button("提交")
                result5_21 = gr.Textbox(label="转录结果5_2")
                result5_22 = gr.Textbox(label="分数结果5_2",visible=False)
            # 请把video5_3换成Video组件
            with gr.Column(visible=False) as ans5_3:
                # score = gr.Textbox(label="得分")
                video5_3=gr.Video(sources=["webcam", "upload"],interactive=True,format='mp4',width=500,label="视频录制(录制结束后，请等待画面闪烁并再次出现后再提交)")
                btn5_3 = gr.Button("提交")
                result5_31 = gr.Textbox(label="转录结果5_3")
                result5_32 = gr.Textbox(label="分数结果5_3",visible=False)
            with gr.Column(visible=False) as summary:
                gr.Markdown("#### 你完成了所有的测验，点击下方按钮生成报告吧~")
                summary_button=gr.Button("生成结论")
            with gr.Column(visible=False) as final_result:
                title6 = gr.Markdown("# 咨询总结与建议")
                final_score = gr.Number(interactive=False,label="最终得分")
                adv = gr.HTML(visible=False)
                save_button=gr.Button("保存本次测试数据",visible=False)

            with gr.Column(visible=False) as save:
                with gr.Row():
                    gr.HTML("<h3 style='text-align:center;'>输入账号密码保存本次检测数据</h3><p style='text-align:center;'>若首次使用，输入账号密码后自动创建账户</p>")
                with gr.Row():
                    with gr.Column(scale=1):
                        input_name = gr.Textbox(label="用户名",interactive=True)
                        input_pwd = gr.Textbox(label="密码",interactive=True)
                        with gr.Row():
                            clear_button = gr.Button("清除")
                            submit_button = gr.Button("提交保存")
                    with gr.Column(scale=1):
                        output_info = gr.Textbox(label="输出", lines=5,interactive=False)

    
    btn1.click(visibility, outputs=questions)
    radio1.change(visibility_choice, radio1, [q1_1, q1_2])
    radio2.change(visibility3, outputs=[title2, radio4])
    radio3.change(visibility3, outputs=[title2, radio4])
    radio4.change(visibility3, outputs=[title3, radio5])
    radio5.change(visibility_choice3, radio5, [radio6, q3_2, q4])
    radio6.change(visibility, outputs=q3_2)
    radio7.change(visibility_choice2, radio7, [ans3_1, ans3_2, ans3_3])
    btn3_1.click(text_score3, text3_1, [result3_11,result3_12,radio8, q4,text1,result1])
    btn3_2.click(speech_score3,audio3_2, [result3_21,result3_22,radio8, q4,text1,result1])
    btn3_3.click(speech_score3,video3_3, [result3_31,result3_32,radio8, q4,text1,result1])
    # 关于btn3_2,btn3_3:请你设计一个函数把语音/视频中文本提取出来，然后经过keyword函数判定来决定要不要出现radio8
    radio8.change(visibility_choice4, radio8, [radio9, q4])
    radio9.change(visibility_choice4, radio9, [radio10, q4])
    radio10.change(visibility, outputs=q4)
    radio10.change(visibility4, outputs=dead_hug)
    radio11.change(visibility_choice2, radio11, [ans4_1, ans4_2, ans4_3])
    btn4_1.click(text_score4,inputs=text4_1, outputs=[result4_11,result4_12,q5,text2,result2])
    btn4_2.click(speech_score4, inputs=audio4_2, outputs=[result4_21,result4_22,q5,text2,result2])
    btn4_3.click(video_score4, inputs=video4_3, outputs=[result4_31,result4_32,q5,text2,result2])
    radio12.change(visibility_choice2, radio12, [ans5_1, ans5_2, ans5_3])
    
    btn5_1.click(text_score4,inputs=text5_1, outputs=[result5_11,result5_12,summary,text3,result3])
    btn5_2.click(speech_score4, inputs=audio5_2, outputs=[result5_21,result5_22,summary,text3,result3])
    btn5_3.click(video_score4, inputs=video5_3, outputs=[result5_31,result5_32,summary,text3,result3])

    summary_button.click(
        advice,
        [
            radio1,
            radio2,
            radio3,
            radio4,
            radio5,
            radio6,
            text1,
            radio8,
            radio9,
            radio10,
            result1,
            result2,
            result3,
        ],
        [final_result,title6, final_score, adv,save_button],
    )

    save_button.click(visibility,inputs=[],outputs=[save])
    clear_button.click(clear_info,inputs=[],outputs=[input_name, input_pwd, output_info])
    submit_button.click(save2,inputs=[input_name,input_pwd,radio1,radio2,radio3,radio4,radio5,radio6,result1,text1,radio8,radio9,radio10,result2,text2,result3,text3,adv],outputs=[output_info])