import os
from openai import OpenAI
import gradio as gr

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)



def predict(message, history):
    history_openai_format = []
    history_openai_format.append({"role": "assistant", "content":"你是一个专业的中国心理咨询师与心理陪伴师，你的所有内容都需要用【中文】回答，你必须对你的患者耐心，你需要以【朋友】的身份和患者交流，这意味着你需要用更加【口语化】的文字回答，并且【不要长篇大论】，更【不要分点作答】。可以偶尔针对用户的回答进行【提问】，并给予必要的【建议和引导】。"})
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message})
  
    response = client.chat.completions.create(model='gpt-3.5-turbo',
       messages= history_openai_format,
        temperature=1.0,
        stream=True)

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
              partial_message = partial_message + chunk.choices[0].delta.content
              yield partial_message

chat=gr.ChatInterface(
    predict,
    chatbot=gr.Chatbot(
        height=400,
        bubble_full_width=False,
        avatar_images=(os.path.join(os.path.dirname(__file__), "patient_ava.png"), os.path.join(os.path.dirname(__file__), "docter_ava.png")),
        likeable=True,
    ),
    # textbox=gr.Textbox(placeholder="在此书输入消息...",),
    retry_btn="🔄重新生成",
    undo_btn="↩️撤回信息",
    clear_btn="🗑️清空信息",
    stop_btn="停止生成",
    submit_btn="发送",
    
)