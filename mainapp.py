import os

from test import test_mode

import gradio as gr

# from acknowledge import acknowledge
# from announce import announce
# from details import details
from user_center import user_center
from introduce import INTRODUCE
from chat import chat

os.environ["no_proxy"] = "localhost,127.0.0.1,::1"


help_message="""
## 校医院
保健科/体检中心<br>
心理咨询、学生体检<br>
62797647

## 学生部-（学生处）
学生心理发展指导中心<br>
办公室<br>
62782007<br>


## 北京安定医院
https://www.bjad.com.cn/<br>
健康服务热线(010)86430066<br>
预约挂号(010)114<br>
市卫生热线：(010)12320<br>

## EE心语预约
http://service.ee.tsinghua.edu.cn/pages/counselor/appointment/appointment<br>
"""


with gr.Blocks() as demo:
    # theme='gstaff/xkcd'
    with gr.Column():
        with gr.Row():
            gr.HTML(
                "<h1 style='text-align:center;'>📈基于多模态融合的抑郁症检测系统📋</h1>"
            )
        # with gr.Row():
        #     gr.HTML("<h5 style='text-align:center;'>[SATLab小分队_入围决赛版]</h5>")
        # with gr.Row():
        #     gr.HTML("<br>")
        #     gr.HTML("<br>")   
        # with gr.Row():
        #     gr.Video(value="demo.mp4",width=300)
        # with gr.Row():
        #     with gr.Column():
        #         gr.Image(value="local_data/QR.svg",width=10,visible=False)
        #     with gr.Column():
        #         gr.Image(value="local_data/QR.png",)
        #     with gr.Column():
        #         gr.Image(value="local_data/QR.svg",width=10,visible=False)
        with gr.Row():
            gr.HTML("<br>")
            gr.HTML("<br>")    
        with gr.Row():
            gr.HTML(INTRODUCE)
        # with gr.Row():
        #     gr.HTML("<br>")
        #     gr.HTML("<br>")

        # with gr.Row():
        #     gr.Markdown(
        #         """
        #         ## 下面的功能面板有五个功能，您可以自由选择。\n
        #         1️⃣知情同意说明\t   2️⃣用法功能详细介绍\t   3️⃣开始自测\t    4️⃣查看个人历史数据\t    5️⃣引用与致谢\n
        #         """
        #     )

        # with gr.Row():
        #     gr.HTML("<br>")
        #     gr.HTML("<br>")
        #     gr.HTML("<br>")

        # with gr.Row():
        #     gr.Markdown("## 功能面板\n")

    # with gr.Tab("🔈️知情同意说明"):
    #     announce.render()
    # with gr.Tab("📜介绍"):
    #     details.render()
    with gr.Tab("📋自我测试"):
        test_mode.render()
    with gr.Tab("💬日常聊天"):
        chat.render()
    with gr.Tab("🗃️个人中心"):
        user_center.render()
    with gr.Tab("📞求助热线"):
        gr.Markdown(help_message)
    # with gr.Tab("💐引用与致谢"):
    #     acknowledge.render()

        
    # gr.HTML("<br><br><br>")
    # gr.HTML("<h1>了解更多</h1>")
    # with gr.Accordion("点击这里",open=False):
    #     with gr.Tab("系统介绍"):
    #         gr.Markdown("系统介绍")
    #     with gr.Tab("关于我们"):
    #         gr.Markdown("关于我们")
    #     with gr.Tab("引用致谢"):
    #         gr.Markdown("引用致谢")
    #     with gr.Tab("免责声明"):
    #         gr.Markdown("免责声明")


demo.launch()
