import os

import gradio as gr

from consult import consult
from scale import scale
from scale_n_consult import SCALE_AND_CONSULT

os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

with gr.Blocks() as test_mode:
    # 量表得分

    with gr.Tab("量表"):
        scale.render()
    with gr.Tab("咨询"):
        consult.render()
    with gr.Tab("量表咨询🆕"):
        SCALE_AND_CONSULT.render()
    # with gr.Tab("咨询(新)"):
    #     gr.Markdown("开发中，敬请期待...")
    # with gr.Tab("综合评估与建议"):
    #     gr.Markdown("结论页面")
