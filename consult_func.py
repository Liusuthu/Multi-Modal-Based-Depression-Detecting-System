import gradio as gr
import os
import pandas as pd
import numpy as np
import datetime
from app_utils import text_score

os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

# def advice1(radio1, radio2, radio3):
# 睡眠
def advice1(radio1, radio2, radio3):
    importance = "睡眠对于人体健康和整体功能有着重要的作用，健康而规律的睡眠作息能够保证第二天的充沛精力与良好心情。"
    current = ""
    if radio1 == 0:
        if radio2 == "存在":
            current = """从交流中，我们得知你的睡眠时间充足，但是存在嗜睡的状况。对于当代的大学生而言，\
由于课业、科研、社工等等各方各面的压力，熬夜赶工是常见的现象，也有不少同学因此而养成了晚睡晚起的习惯。\
每个人有着自己不同的生活习惯，如果这种生活方式没有明显影响你的健康和日常功能，并且你能够适应这样的规律，\
那么这样的作息安排是可以接受的。但需要提醒你的是，如果你的嗜睡有比较严重的症状，比如出现了白天过度疲倦、精神不振的情况，\
则有可能是由于睡眠障碍或一些心理健康问题引起的，若长期处于这种状态中，建议你主动咨询医生以进行详细的评估，\
并积极调整自己的作息习惯。\
"""
            return importance + current
        else:
            current = """从交流中，我们得知你的睡眠时间充足，睡眠习惯良好。我们深知，对于当代的大学生而言，\
由于课业、科研、社工等等各方各面的压力，熬夜赶工是常见的现象，这很大程度上影响到个体的身心健康。\
我们很开心能听到你养成了良好的作息习惯，这对你的学习和工作是大有裨益的，请继续保持！即使将来因为个别情况需要熬夜，\
也请多多注意身体的承受能力，并积极将作息调整到正轨中！\
"""
            return importance + current

    else:
        if radio3 == "不存在":
            current = """从交流中，我们得知你的睡眠时间不足，但是并没有失眠或早醒的问题。每个人有着自己不同的生活习惯，\
如果当前的睡眠时长能让你在第二天的学习和工作中保持较为良好的状态，那么则不用太过担心。但如果睡眠时间不足导致你在白天中出现过度疲惫、\
头晕等等不良情况，我们建议你适当调整自己的睡眠作息，适当提早入睡时间，或者适当延后起床时间都是可以的。当然，\
调整作息是一个比较漫长的过程，你也不需要给自己太多压力，更不要因此而焦虑，以至于过度影响到了自己情绪，造成了更不好的后果。\
"""
            return importance + current

        elif radio3 == "失眠":
            current = """从交流中，我们得知你存在一定程度上的失眠问题。失眠或许可能对你的身体和心理造成一定程度上的负面影响，\
但请不要因此而焦虑，这是很常见的现象，可能与神经衰弱、睡眠浅有关，这也当然不是你的过错。如果你有比较轻微的失眠问题，\
我们建议你可以主动积极地做出一些改变，比如积极和舍友沟通好作息时间，购买窗帘、耳塞，以及避免在睡前饮食、输入咖啡因等等，\
这些小事能一定程度上帮助你更好地入睡；如果你有稍微明显的失眠问题，则除了上面的那些做法外，你还可以试着在睡前减少电子屏幕的使用时间，\
尝试做一些睡前阅读、冥想、听轻音乐等习惯，让你的内心平静下来，以更好地入睡；如果你认为自己的失眠问题比较严重了，\
我们建议你尽快联系专业的心理咨询师以及心理医生，寻求专业人士的帮助，不论去校医院、心理中心以及校外的医院，都是不错的选择。\
我们也真心希望你能早日摆脱失眠的困扰，当然了，调整作息是一个比较漫长的过程，你也不需要给自己太多压力，更不要因此而焦虑，以至于过度影响到了自己的情绪。\
"""
            return importance + current

        else:
            current = """从交流中，我们得知你因为早醒而存在睡眠不足的问题。早醒者通常早于期望醒来，并且无法重新入睡，这可能会导致白天疲劳和不适。\
要想改变早醒的现状，保证充足的睡眠，可以 努力地尽量保持每天相同的入睡时间，即使在周末也尽量保持一致。这有助于调整生物钟，提高睡眠质量。\
此外，创造舒适的睡眠环境、减少刺激物也同样重要，你可以购置窗帘、耳塞等，这有助于防止你因为光照或响声而被吵醒。如果你已经做出了很多努力但仍无法解决该问题，\
我们建议你尽快联系专业的心理咨询师以及心理医生，寻求专业人士的帮助，对自己的生活习惯以及作息做出更加科学的调整。\
我们也真心希望你能早日摆脱早醒的困扰，当然了，调整作息是一个比较漫长的过程，你也不需要给自己太多压力，更不要因此而焦虑，以至于过度影响到了自己的情绪。\
"""
            return importance + current


# 饮食
def advice2(radio4):
    importance = "饮食规律对于维护身体健康和促进整体健康至关重要。"
    if radio4 == 0:
        current = """
当前你的饮食习惯较为良好，食欲正常且没有体重上的明显变化，要保持住当前的状态。此外，积极参与体育锻炼也是必要的，\
不仅有助于增强体质，也有助于养成良好的生活习惯，保持身心健康。当然，在一段时间内，如果自己的体重存在波动，也是正常现象，\
不需要太过于在意，更不要因此而焦虑。
"""
        return importance + current
    elif radio4 == 1:
        current = """
当前你存在食欲亢进和体重增加的问题，这可能由多种原因引起，比如激素变化、情绪变化、缺乏运动、作息饮食不规律等等，\
你可以仔细想想自己可能因为哪些因素而导致了当前的情况，并尝试着慢慢去改变，将其引导到较为正常的状态上去。\
如果食欲亢进和体重增加已经对你的生活产生了比较大的影响，请尽快寻求专业医生的帮助，进行全面的评估。\
医生可以帮助确定潜在原因，并制定相应的治疗计划，可能包括药物治疗、心理治疗、饮食和运动指导等。\
你也应该根据自身的情况制定适合自己的健康计划，以维护身体健康。\
"""
        return importance + current
    else:
        current = """
当前你存在食欲不振和体重减轻的问题，这可能由多种原因引起，比如消化系统与代谢问题、心理压力、缺乏运动、作息饮食不规律等等，\
你可以仔细想想自己可能因为哪些因素而导致了当前的情况，并尝试着慢慢去改变，将其引导到较为正常的状态上去。\
如果这件事情已经对你的生活产生了比较大的影响，请尽快寻求专业医生的帮助，进行全面的评估。\
医生可以帮助确定潜在原因，并制定相应的治疗计划，可能包括药物治疗、心理治疗、饮食和运动指导等。\
你也应该根据自身的情况制定适合自己的健康计划，以维护身体健康。\
"""
        return importance + current
    # # 有关饮食问题的建议
    # if radio4 == 0:
    #     return "不存在"
    # if radio4 == 1:
    #     return "增重"
    # else:
    #     return "消瘦"


# 心情
def advice3(radio5, radio6):
    importance = (
        "保持良好心情对于整体健康和生活质量至关重要。积极的情绪和心态有助于降低压力水平，增强抗挫折能力，\
也对心理健康有益，有助于缓解焦虑和抑郁，促进更健康的人际关系。"
    )
    if radio5 == "好":
        current = """你的心情处在较好的水平，这是非常好的，请继续保持。\
"""
        return importance + current
    else:
        if radio6 == "一周以内":
            current = """通过上面的交流，我们得知你有较为短期的心情低落，这或许是由于近期内有一些不顺利的事情造成的，\
这是自然现象，不必太过紧张。首先，尝试认识到自己的情绪，并允许自己感受这种情绪，而不是压抑或忽视。\
其次，寻找能够缓解压力和焦虑的方式，如进行深呼吸、冥想或轻松的身体活动。此外，与亲友分享感受，倾诉心声也可能有助于减轻负面情绪。\
保持健康的生活方式，包括良好的睡眠、均衡饮食和适度的运动，对提升心情有积极作用。最重要的是，给自己一些宽容和理解，明白情绪波动是正常的生活体验，而积极的应对方式有助于渡过情绪低谷。\
相信在积极的包容和面对下，这种情况会有所缓和的。
"""
            return importance + current
        elif radio6 == "一周至两周":
            current = """通过上面的交流，我们得知你有长达一两周的心情低落，这种情况值得我们更加关注并考虑采取积极的措施。\
首先，与朋友、家人或专业人士分享你的感受，倾诉可能有助于缓解内心的负担。同时，关注自己的生活方式，确保足够的睡眠、均衡的饮食和适度的运动，\
这对于心理健康至关重要。也可以考虑寻求专业心理健康帮助，如心理治疗或咨询服务，专业人士可以提供更深入的支持和指导。\
最重要的是，要认识到情绪低落可能需要更多关注和处理，而不是试图独自承受，相信在积极的包容和面对下，这种情况会有所缓和的。\
"""
            return importance + current
        else:
            current = """通过上面的交流，我们得知你有长于两周的心情低落，这可能是一种严重的心理健康状况，需要寻求专业帮助。\
首先，考虑咨询心理健康专业人士，如心理医生、精神科医生或心理治疗师。专业人士可以进行深入的评估，帮助识别问题的根本原因，并提供相应的治疗计划。\
同时，与家人和朋友分享你的感受，并让他们了解你的状况。亲密的人陪伴和支持对于康复过程非常重要。\
应避免自行处理或忽视严重的情绪低落，因为这可能影响到日常生活和整体健康。如果有自杀倾向或紧急情况，立即寻求紧急医疗帮助，拨打紧急电话或前往最近的急诊室。\
你要认识到寻求专业帮助并与他人分享你的感受是勇敢和有效的做法，可以为康复创造更好的机会。专业心理健康团队能够提供适当的治疗、支持和指导，帮助你渡过情绪低谷，重建积极的生活态度。\
"""
            return importance + current

    # # 有关情绪问题的建议
    # if radio5 == "好":
    #     return "不存在情绪问题"
    # if radio5 == "不好":
    #     return "抑郁情绪持续了" + radio6


# 自杀
def advice4(radio5, text3_1, radio8, radio9, radio10):
    # 有关自杀倾向的建议
    if radio5 == "不好":
        if keyword(text3_1):
            if radio8 == 0:
                if radio9 == 0:
                    if radio10 == "没想过":
                        return ",有自杀倾向"
                    if radio10 == "想过，没想过具体时间和地点":
                        return ",自杀倾向较严重"
                    if radio10 == "想过具体做法，时间和地点，没实践过":
                        return ",自杀倾向严重"
                    if radio10 == "实践过":
                        return ",有过自杀行为"
                else:
                    return ",有自杀倾向"
        else:
            return " "
    else:
        return " "


def score_analysis(score):
    if score>=50:
        return "你的分数高于50，这意味着你的负面情绪占比较高，你可能有轻微的抑郁倾向，这可能与你最近的学习、生活状态有关。"
    else:
        return "你的分数低于50，这意味着你的心理状态正常健康，请继续保持！"

def advice(
    radio1, radio2, radio3, radio4, radio5, radio6, text3_1, radio8, radio9, radio10,result1,result2,result3
):
    # symptoms = ""
    # if advice1(radio1, radio2, radio3) == "不存在" and advice2(radio4) == "不存在":
    #     symptoms = "不存在睡眠、饮食问题且"
    # if advice1(radio1, radio2, radio3) != "不存在" and advice2(radio4) == "不存在":
    #     symptoms = "存在" + advice1(radio1, radio2, radio3) + "问题，不存在饮食问题且"
    # if advice1(radio1, radio2, radio3) == "不存在" and advice2(radio4) != "不存在":
    #     symptoms = "不存在睡眠问题，存在" + advice2(radio4) + "问题且"
    print(result1,result2,result3)
    if result1==0:
        final_score=(((-1+result2+result3)/3)+1)*50
    else:
        final_score=(((0.5*result1+result2+result3)/3)+1)*50
    print(final_score)
    
    SCORE_ANALYSIS=score_analysis(final_score)
    SLEEP = advice1(radio1, radio2, radio3)
    EAT = advice2(radio4)
    MOOD = advice3(radio5, radio6)
    SUICIDE =" " #"自杀这里还没想好啊。"
    INTEREST = """兴趣爱好对于个体的生活质量和心理健康至关重要。拥有积极的兴趣爱好不仅为日常生活增添乐趣，还有助于缓解压力、减轻焦虑和提高心理幸福感。
兴趣爱好提供了一个追求个人兴趣和激发创造力的平台，有助于保持积极的心态。通过投身于喜欢的活动，个体能够建立社交关系，拓展社交圈，
这对于心理健康和人际互动都是非常有益的。此外，兴趣爱好也为个体提供了逃避日常压力和烦扰的机会，促使身心得到放松和恢复。
"""
    RECENT = " "  #"可以看出你的近期情况不错，继续保持。"
    SUMMARY = "一次测量结果只是当下心理状态的反应，并不能代表你的长期状态。抑郁症症状因人而异，并不应当只以是否存在上述症状来判断，并且可能存在上述症状以外更个人化的症状。如果存在强烈的各种不适或者怀疑自己有抑郁症，建议及时去进行专业检查和干预治疗。最后，不论测试结果如何，都请你保持怀抱的心态接受接下来的每一天。也欢迎你多来拜访我们的APP，持续关注自己的健康状态，我们一直在这里等你~"

    # FINAL_ADVICE = """     
    # <h1 style='text-align:center;'>检测报告</h1>
    # <h3 style='text-align:center;'>得分分析</h3>
    # &emsp;&emsp;{0}\n
    # <h3 style='text-align:center;'>睡眠状况</h3>
    # &emsp;&emsp;{1}\n
    # <h3 style='text-align:center;'>饮食状况</h3>
    # &emsp;&emsp;{2}\n
    # <h3 style='text-align:center;'>情绪状况</h3>
    # &emsp;&emsp;{3}\n
    # &emsp;&emsp;{4}\n
    # <h3 style='text-align:center;'>兴趣爱好</h3>
    # &emsp;&emsp;{5}\n
    # <h3 style='text-align:center;'>近期情况</h3>
    # &emsp;&emsp;{6}\n
    # <h3 style='text-align:center;'>结语</h3>
    # &emsp;&emsp;{7}\n
    # """.format(SCORE_ANALYSIS, SLEEP, EAT, MOOD, SUICIDE, INTEREST, RECENT, SUMMARY)
    FINAL_ADVICE = """     
    <h1 style='text-align:center;'>检测报告</h1>
    <h3 style='text-align:center;'>得分分析</h3>
    &emsp;&emsp;{0}\n
    <h3 style='text-align:center;'>睡眠状况</h3>
    &emsp;&emsp;{1}\n
    <h3 style='text-align:center;'>饮食状况</h3>
    &emsp;&emsp;{2}\n
    <h3 style='text-align:center;'>情绪状况</h3>
    &emsp;&emsp;{3}\n
    <h3 style='text-align:center;'>结语</h3>
    &emsp;&emsp;{4}\n
    """.format(SCORE_ANALYSIS, SLEEP, EAT, MOOD, SUMMARY)
    
    return (
        gr.Column(visible=True),
        gr.Markdown(visible=True),
        final_score,
        gr.HTML(
            value=FINAL_ADVICE,
            visible=True,
        ),
        gr.Button(visible=True),
    )


# def final_advice(
#     radio1, radio2, radio3, radio4, radio5, radio6, text3_1, radio8, radio9, radio10
# ):
#     return gr.Textbox(
#         visible=True,
#         value=advice(
#             radio1,
#             radio2,
#             radio3,
#             radio4,
#             radio5,
#             radio6,
#             text3_1,
#             radio8,
#             radio9,
#             radio10,
#         ),
#     )


def visibility():  # 让下一部分出现
    return gr.Column(visible=True)


def visibility2():  # 让下一道选择题出现
    return gr.Radio(visible=True)


def visibility3():  # 针对有标题切换的情况
    return (
        gr.Markdown(visible=True),
        gr.Radio(visible=True),
    )


def visibility4():
    return gr.Markdown(visible=True)


def visibility_choice(choice):  # 根据选择选项的不同决定下一道题是哪个
    if choice == 0:
        return gr.Column(visible=True), gr.Column(visible=False)
    else:
        return gr.Column(visible=False), gr.Column(visible=True)


def visibility_choice2(choice):  # 选择视频，语音还是文本输入
    if choice == 0:
        return (
            gr.Column(visible=True),
            gr.Column(visible=False),
            gr.Column(visible=False),
        )
    if choice == 1:
        return (
            gr.Column(visible=False),
            gr.Column(visible=True),
            gr.Column(visible=False),
        )
    else:
        return (
            gr.Column(visible=False),
            gr.Column(visible=False),
            gr.Column(visible=True),
        )


def visibility_choice3(choice):  # 根据选择选项的不同决定下一道题是哪个
    if choice == "不好":
        return (
            gr.Radio(visible=True),
            gr.Column(visible=False),
            gr.Column(visible=False),
        )
    else:
        return (
            gr.Radio(visible=False),
            gr.Column(visible=False),
            gr.Column(visible=True),
        )


def visibility_choice4(choice):  # 根据选择选项的不同决定下一道题是哪个
    if choice == 0:
        return gr.Radio(visible=True), gr.Radio(visible=False)
    else:
        return gr.Radio(visible=False), gr.Radio(visible=True)



def visibility_choice5(text):  # 关于自杀倾向问题是否触发
    if keyword(text) is True:
        return gr.Radio(visible=True), gr.Column(visible=False)
    else:
        return gr.Radio(visible=False), gr.Column(visible=True)


##########################################################
# 获取next数组
def get_next(T):
    i = 0
    j = -1
    next_val = [-1] * len(T)
    while i < len(T) - 1:
        if j == -1 or T[i] == T[j]:
            i += 1
            j += 1
            # next_val[i] = j
            if i < len(T) and T[i] != T[j]:
                next_val[i] = j
            else:
                next_val[i] = next_val[j]
        else:
            j = next_val[j]
    return next_val


# KMP算法
def kmp(S, T):
    i = 0
    j = 0
    next = get_next(T)
    while i < len(S) and j < len(T):
        if j == -1 or S[i] == T[j]:
            i += 1
            j += 1
        else:
            j = next[j]
    if j == len(T):
        return i - j
    else:
        return -1

#识别负面词的函数
def keyword(
    text
):      
    negative_keywords = ["轻生", "自杀", "死", "活着", "意义", "意思", "干劲","自残","孤单","结束",
                         "救","血","割腕","歇斯底里","抑郁","创伤","遗书","遗嘱","痛苦","跳楼","双向",
                         "障碍","精神病","变态","一无是处","疯",]
    text,score=text_score(text)
    for word in negative_keywords:
        if kmp(text,word)!=-1 and score>=0:
            return True
    return False


#保存测试数据
def save2(username,password,radio1,radio2,radio3,radio4,radio5,radio6,result1,text1,radio8,radio9,radio10,result2,text2,result3,text3,adv):
    new_data2=get_info(radio1,radio2,radio3,radio4,radio5,radio6,result1,text1,radio8,radio9,radio10,result2,text2,result3,text3,adv,)
    if (username=='' or password==''):
        return '请填写完整信息'

    user_login_df=pd.read_csv('./user_login/login.csv',encoding='gbk',converters = {'password':str})
    user_login=user_login_df.set_index('username')['password'].T.to_dict()
    user_data2_df=pd.read_csv('./user_data/data_2.csv',encoding='gbk',converters ={'senti_flt':float,'hobby_flt':float,'all_flt':float})

    results=''
    is_usn=(username in user_login)
    if(is_usn):
        pswd_crct=(password==user_login[username])
    if(is_usn and pswd_crct):
        results='登录成功，存储报告成功。'
        user_data2_df.loc[len(user_data2_df)]=[username,datetime.date.today(),
                                             datetime.datetime.now().strftime('%H:%M:%S')]+new_data2
        user_data2_df.to_csv('./user_data/data_2.csv',encoding='gbk',index=False)
    elif(is_usn):
        results='密码错误！'
    else:
        user_login_df.loc[len(user_login_df)]=[username,password]
        user_data2_df.loc[len(user_data2_df)]=[username,datetime.date.today(),
                                             datetime.datetime.now().strftime('%H:%M:%S')]+new_data2
        user_login_df.to_csv('./user_login/login.csv',encoding='gbk',index=False)
        user_data2_df.to_csv('./user_data/data_2.csv',encoding='gbk',index=False)
        results='账户不存在，已创建新的账户并保存数据。'

        
    return results

#从作答项目获取存储内容
def get_info(radio1,radio2,radio3,radio4,radio5,radio6,result1,text1,radio8,radio9,radio10,result2,text2,result3,text3,adv,):
    #radio1,radio2,radio3睡眠情况
    if radio1==0:
        if radio2=="存在":
            sleep="睡眠充足，存在嗜睡情况"
        else:
            sleep="睡眠充足，不存在嗜睡情况"
    else:
        if radio3=="不存在":
            sleep="睡眠不足，不存在失眠或早醒情况"
        elif radio3=="失眠":
            sleep="睡眠不足，存在失眠情况"
        else:
            sleep="睡眠不足，存在早醒情况"
    #radio4食欲情况
    if radio4==0:
        eat="食欲正常，体重无明显变化"
    elif radio4==1:
        eat="食欲亢进，体重增加"
    else:
        eat="食欲不振，体重减轻"
    #radio5,radio6心情情况
    if radio5=="好":
        mood="心情好"
    else:
        if radio6=="一周以内":
            mood="心情不好，持续一周以内"
        elif radio6=="一周至两周":
            mood="心情不好，持续一到两周"
        else:
            mood="心情不好，持续两周以上"
        
    #回答的分数与内容
    ans_score=result1
    ans_text=text1
    #radio8,radio9,radio10自杀情况
    if radio8==1 or radio5=="好":
        suicide="无自杀倾向"
    else:
        if radio9==1:
            suicide="想过死，但没想过怎么死"
        else:
            if radio10=="没想过":
                suicide="想过死，也想过怎么死，但没有具体想过"
            else:
                if radio10=="想过，没想过具体时间和地点":
                    suicide="想过死，也想过具体的做法，但没想过具体时间和地点"
                else:
                    if radio10=="想过具体做法，时间和地点，没实践过":
                        suicide="想过死的具体做法、时间和地点，但是没实践过"
                    else:
                        suicide="尝试自杀过"
    #兴趣分数与内容
    hobby_score=result2
    hobby_text=text2
    #近期分数与内容
    recent_score=result3
    recent_text=text3
    #adv总结建议
    advice="can be generated from the data above"

    
    data=[sleep,eat,mood,ans_score,ans_text,suicide,hobby_score,hobby_text,recent_score,recent_text,advice]
    # data=[2,3,4,5.0,'该回答的分数',6,7.0,'该回答的文字',8.0,'该回答的文字','最终建议']
    return data