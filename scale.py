import os
import pandas as pd
import numpy as np
import datetime
import gradio as gr

os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

s=0

def visibility():
    return gr.Column(visible=True)


def Score(choice1,choice2,choice3,choice4,choice5,choice6,choice7,choice8,choice9,choice10,choice11,choice12,choice13,choice14,choice15,choice16,choice17,choice18,choice19,choice20):
    score = 0
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
        global s
        s = round(1.25*score, 0)
        if s < 53:
            return gr.Column(visible=True),s,"被测试者无抑郁体验。心情明朗,轻松愉快,对自己身体和情绪健康有良好的感受,对自己的现状感到满意。","被试无抑郁体验，希望保持。被试的生活很开心,也很轻松,感到生活充实,健康状况良好,对未来充满希望,如果条件许可,被试可以了解一些必要的心理知识,为今后保持健康的心理奠定基础。",gr.Button(visible=True)
        if 53 <= s <= 62:
            return gr.Column(visible=True),s,"通过测试表明被试属于轻度抑郁。偶尔有些郁闷、压抑。被测者在遇到挫折和烦恼时,会出现暂时的情绪低落。","需要认识到这些情绪，并学习调节情绪的方法，参考建议：不要掩饰自己的负面情绪、过多地压抑自己,要学会倾诉和宣泄等方式来进行自我调节。培养积极的认知方式,改变对自己的认识,全面认识自我,悦纳自我,善待自我。",gr.Button(visible=True)
        if 63 <= s <= 72:
            return gr.Column(visible=True),s,"被测试者表现出中度抑郁。你最近时常出现心境低落现象，通常情况下，继续进行工作、社交或家务活动已有一定困难。","建议从以下几方面改善抑郁状态：不草率对事件下结论；学会理性的思考方式，避免情绪性推理；避免“我必须”，“我一定”这类的自我对话；对自身做出尽可能正确和公平的评价等。学会一些自我保护措施，一旦发现自己产生了抑郁的观念或行为，可以及时运用自身力量主动挑战自己的观念和行为，如“我是否只看到了生活的黑暗面？”等；相信他人的正确评价，不要否认他人的夸奖。",gr.Button(visible=True)
        if s > 72:
            return gr.Column(visible=True),s,"被测试者的测验结果为重度抑郁。从结果中可以看出，你总感到心境低落，总处于压抑、抑郁、悲伤、失望、沮丧或忧伤的情绪状态之中。你抑郁症状已十分明显，社会功能明显损害，除了在极有限的范围内，几乎不可能继续进行社交、工作或家务活动。","被测试者表现出重度抑郁。你的抑郁症状已十分明显，社会功能明显损害，除了在极有限的范围内，几乎不可能继续进行社交、工作或家务活动。应当尽快进行心理咨询",gr.Button(visible=True)




def save1(username,password,score,exp,adv):
    if (username=='' or password==''):
        return '请填写完整信息'

    new_data1=[score,exp,adv]
    user_login_df=pd.read_csv('./user_login/login.csv',encoding='gbk',converters = {'password':str})
    user_login=user_login_df.set_index('username')['password'].T.to_dict()
    user_data1_df=pd.read_csv('./user_data/data_1.csv',encoding='gbk')

    results=''
    is_usn=(username in user_login)
    if(is_usn):
        pswd_crct=(password==user_login[username])
    if(is_usn and pswd_crct):
        results='登录成功，存储报告成功。'
        user_data1_df.loc[len(user_data1_df)]=[username,datetime.date.today(),
                                             datetime.datetime.now().strftime('%H:%M:%S')]+new_data1
        user_data1_df.to_csv('./user_data/data_1.csv',encoding='gbk',index=False)
    elif(is_usn):
        results='密码错误！'
    else:
        user_login_df.loc[len(user_login_df)]=[username,password]
        user_data1_df.loc[len(user_data1_df)]=[username,datetime.date.today(),
                                             datetime.datetime.now().strftime('%H:%M:%S')]+new_data1
        user_login_df.to_csv('./user_login/login.csv',encoding='gbk',index=False)
        user_data1_df.to_csv('./user_data/data_1.csv',encoding='gbk',index=False)
        results='账户不存在，已创建新的账户并保存数据。'

        
    return results


def clear_info():
    return (
        gr.Textbox(""),
        gr.Textbox(""),
        gr.Textbox(""),
    )

    

with gr.Blocks() as scale: 
    with gr.Column():
        gr.Markdown("本评定量表为临床上常用于抑郁症检测的SDS(Self-rating depression scale)量表，本量表共有20个项目，请您根据最近一星期以来你的实际感受，选择一个与您的情况最相符合的答案。")
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
            btn2 = gr.Button("提交")
        with gr.Column(visible=False) as result:
            score = gr.Textbox(label="得分",interactive=False)
            exp = gr.Textbox(label="结果解释",interactive=False)
            adv = gr.Textbox(label="指导建议",interactive=False)
            save_btn = gr.Button("保存本次检测数据")
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
        
        btn.click(visibility,outputs=question)
        btn2.click(Score,[r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20],[result,score,exp,adv,save_btn])
        save_btn.click(visibility,inputs=[],outputs=[save])
        clear_button.click(clear_info,inputs=[],outputs=[input_name, input_pwd, output_info])
        submit_button.click(save1,inputs=[input_name,input_pwd,score,exp,adv,],outputs=[output_info])
        