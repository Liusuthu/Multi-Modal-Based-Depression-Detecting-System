import os

import gradio as gr
from openai import OpenAI

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
###量表函数###
def visibility():
    return gr.Column(visible=True)

def scale2json(choice1,choice2,choice3,choice4,choice5,choice6,choice7,choice8,choice9,choice10,choice11,choice12,choice13,choice14,choice15,choice16,choice17,choice18,choice19,choice20):
    score = 0
    global initial_prompt
    choices = [choice1,choice2,choice3,choice4,choice5,choice6,choice7,choice8,choice9,choice10,choice11,choice12,choice13,choice14,choice15,choice16,choice17,choice18,choice19,choice20]
    if None in choices:
        gr.Warning("您有未勾选的题目，请确认后再次提交")
    else:
        for i in range(len(choices)):
            match i:
                case 1|4|5|10|11|13|15|16|17|19:
                    score += 4 - choices[i]
                case _:
                    score += choices[i] + 1
        s = round(1.25*score, 0)
        DEPRESS="无抑郁体验" if s<53 else "可能有轻度抑郁倾向" if s<=62 else "可能有中度抑郁倾向" if s<=72 else "可能有重度抑郁倾向"
        SLEEP="夜间睡眠良好"if choice4==0 else "有时夜间睡眠不好" if choice4==1 else "经常夜间睡眠不好" if choice4==2 else "总是夜间睡眠不好"
        EAT="饮食状态差，不如平时" if choice5==0 else "饮食状态经常不如平时" if choice5==1 else "饮食状态正常" if choice5==2 else "饮食状态良好"
        WEIGHT="体重正常" if choice7==0 else "有时体重会减轻" if choice7==1 else "体重经常会减轻" if choice7==2 else "体重相较于平时总是减轻"
        MOOD1="很少感到沮丧郁闷" if choice1==0 else "有时感到沮丧郁闷" if choice1==1 else "经常感到沮丧郁闷" if choice1==2 else "总是感到沮丧郁闷"
        MOOD2="几乎没有想哭的感觉" if choice3==0 else "有时会有想哭的感觉" if choice3==1 else "经常会有想哭的感觉" if choice3==2 else "总是会想哭"
        MOOD3="不容易发怒" if choice15==0 else "有时容易发怒" if choice15==1 else "经常容易发怒" if choice15==2 else "总是容易发怒"
        MOOD=MOOD1+", "+MOOD2+", "+MOOD3
        TIRED="很少感到疲劳" if choice10==0 else "有时会感到疲劳" if choice10==1 else "经常会感到疲劳" if choice10==2 else "总是感到疲劳"
        ANXIETY="几乎不会烦躁" if choice13==0 else "有时会坐立不安、难以平静" if choice13==1 else "经常会坐立不安、难以平静" if choice13==2 else"总是坐立不安、感觉难以平静"
        PHYSICAL=TIRED+", "+ANXIETY
        VALUE1="从来不觉得自己有用、不可或缺" if choice17==0 else "只有有时会觉得自己有用、不可或缺" if choice17==1 else "觉得自己是有用的、不可或缺的"
        VALUE2="很少觉得自己的生活有意义" if choice18==0 else "有时才会觉得自己的生活有意义" if choice18==1 else "觉得自己的生活是有意义的"
        VALUE=VALUE1+", "+VALUE2
        SUICIDE="无自杀倾向" if choice19==0 else "有时会觉得自己死了别人会过得更好" if choice19==1 else "经常会觉得自己死了别人会过得更好" if choice19==2 else "总觉得自己死了别人会过得更好"

        json_info=r"""
{{
    "抑郁情况":"{}",
    "睡眠状况":"{}",
    "饮食状况":"{}",
    "体重状况":"{}",
    "心情状况":"{}",
    "日常生理状况":"{}",
    "价值感":"{}",
    "自杀倾向":"{}",
}}
""".format(DEPRESS,SLEEP,EAT,WEIGHT,MOOD,PHYSICAL,VALUE,SUICIDE,)
        
        if choice19>=2:
            gr.Info("如果你感到难以坚持下去，想要结束自己的生命，请一定不要灰心，请通过电话联系我们(4000-100-525, 再拨2)，我们会陪伴在你身边！")

        initial_prompt="""你是一名【专业的心理咨询师】，以下是你的用户的【基本情况】，由JSON格式给出："""+json_info+"""当你和用户交谈时，你需要【主动】向用户提问，并【围绕】用户的【基本情况】展开，【负面】的基本情况需要【着重】展开。
首先，你需要进行【自我介绍】，然后根据用户的基本情况【展开详细的咨询】，但是【不能一下抛出所有问题，需要逐条提问】，主动向用户【提问】相关的问题并基于相应的【建议】。
在你认为询问完毕后，你需要【向用户确认是否结束咨询】，得到【肯定的回复后】，再生成一个【咨询报告】，包含【用户情况】、【相应建议】、【最终总结】，先以Markdown格式输出，再以JSON格式输出。
最后你需要告诉用户，诊断已结束，你不会主动提问，但受咨询者可以继续向你提问感兴趣的问题，你会作出回答。"""
    
    return gr.Column(visible=True),s,initial_prompt
############


###Chatbot函数###
def predict(message, history):
    global initial_prompt
    history_openai_format = []
    history_openai_format.append({"role": "assistant", "content":initial_prompt})
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message})
  
    response = client.chat.completions.create(model='gpt-4-turbo-preview',
       messages= history_openai_format,
        temperature=1.0,
        stream=True)

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
              partial_message = partial_message + chunk.choices[0].delta.content
              yield partial_message
##############


CHAT_SECTION=gr.ChatInterface(
    predict,
    chatbot=gr.Chatbot(
        height=400,
        bubble_full_width=False,
        avatar_images=(os.path.join(os.path.dirname(__file__), "patient_ava.png"), os.path.join(os.path.dirname(__file__), "docter_ava.png")),
        likeable=True,
    ),
    # textbox=gr.Textbox(placeholder="在此输入消息...",),
    retry_btn="🔄重新生成",
    undo_btn="↩️撤回信息",
    clear_btn="🗑️清空信息",
    stop_btn="停止生成",
    submit_btn="发送",
    
)

with gr.Blocks() as SCALE_AND_CONSULT:
     ###量表环节
     with gr.Column():
        gr.Markdown("**在此项检测模式中，用户需要首先填写一份量表，随后系统将根据量表的填写情况对用户进行更细致的咨询，最终结合用户的回答状况给出诊断结果。**")
        gr.Markdown("首先进行量表填写。本评定量表为临床上常用于抑郁症检测的SDS(Self-rating depression scale)量表，共有20个项目，请您根据最近一星期以来的实际感受，选择与您的情况最相符的答案。")
        gr.Markdown("A：从无或偶尔（过去一周内，出现这类情况的日子不超过一天）")
        gr.Markdown("B：有时（过去一周内，有1-2天有过这类情况）")
        gr.Markdown("C：经常（过去一周内，有3-4天有过这类情况）")
        gr.Markdown("D：总是如此（过去一周内，有5-7天有过类似情况）")
        # gr.Markdown("评分范围与标准：")
        # gr.Markdown("0-52: 无抑郁体验&emsp;&emsp;53-62: 轻度抑郁&emsp;&emsp;63-72: 中度抑郁&emsp;&emsp;72-80: 重度抑郁")
        btn = gr.Button("继续")
        with gr.Column(visible=False) as question:
            r1 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "1.我感到心里沮丧，郁闷",type = "index")
            r2 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "2.我感到早晨心情最好",type = "index")
            r3 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "3.我要哭或想哭",type = "index")
            r4 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "4.我夜间睡眠不好",type = "index")
            r5 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "5.我吃饭像平常一样多",type = "index")
            r6 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "6.我的性功能正常",type = "index")
            r7 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "7.我感到体重减轻",type = "index")
            r8 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "8.我为便秘烦恼",type = "index")
            r9 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "9.我的心跳比平时快",type = "index")
            r10 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "10.我无故感到疲劳",type = "index")
            r11 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "11.我的头脑像往常一样清楚",type = "index")
            r12 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "12.我做事情像平时一样不感到困难",type = "index")
            r13 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "13.我坐卧不安，难以保持平静",type = "index")
            r14 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "14.我对未来感到有希望",type = "index")
            r15 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "15.我比平时更容易激怒",type = "index")
            r16 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "16.我觉得决定什么事情很容易",type = "index")
            r17 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "17.我感到自己是有用的和不可缺少的人",type = "index")
            r18 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "18.我的生活很有意义",type = "index")
            r19 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "19.假若我死了别人会过得更好",type = "index")
            r20 = gr.Radio(["A.从无或偶尔","B.有时","C.经常","D.总是如此"],label = "20.我仍旧喜爱自己平时喜爱的东西",type = "index")
            # btn2 = gr.Button("提交")
            btn_json=gr.Button("提交问卷并进入咨询")
        with gr.Column(visible=False) as JSON:
            with gr.Row():
                score = gr.Textbox(label="得分",visible=False)
            with gr.Row():
                output_json=gr.Textbox(label="scale2jsonprompt",visible=False)
            with gr.Row():
                gr.Markdown("**接下来，系统将根据量表的填写结果，与用户进行咨询交流。**")
            with gr.Row():
                with gr.Column():
                    CHAT_SECTION.render()
            with gr.Row():
                with gr.Column():
                    gr.Video(sources=["webcam", "upload"],)
                with gr.Column():
                    gr.Audio(sources=["microphone"])
            with gr.Row():
                generate=gr.Button("结束聊天，生成最终结果(待开发)")
        
        btn.click(visibility,outputs=question)
        btn_json.click(scale2json,[r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20],[JSON,score,output_json])
