# import datetime
import os

import gradio as gr
import numpy as np
import pandas as pd

os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
#######################################################################################
def read_ui(username,password):
    if (username=='' or password==''):
        return '请填写完整信息'
    user_login_df=pd.read_csv('./user_login/login.csv',encoding='gbk',converters = {'password':str})
    user_login=user_login_df.set_index('username')['password'].T.to_dict()
    user_data1_df=pd.read_csv('./user_data/data_1.csv',encoding='gbk')
    user_data2_df=pd.read_csv('./user_data/data_2.csv',encoding='gbk',converters ={'senti_flt':float,'hobby_flt':float,'all_flt':float})

    results=''
    is_usn=(username in user_login)
    if(is_usn):
        pswd_crct=(password==user_login[username])
    if(is_usn and pswd_crct):
        report1=user_data1_df[user_data1_df['username'] == username]
        report1=np.array(report1).tolist()
        report2=user_data2_df[user_data2_df['username'] == username]
        report2=np.array(report2).tolist()

        results='用户名：'+username+'\n'
        for i in range(len(report1)):
            line1=report1[i]
            results=results+'第'+str(i+1)+'次量表测试  '+'日期：'+str(line1[1])+' 时间：'+str(line1[2])+'\n'
            results=results+'量表分数：'+str(line1[3])+'\n结果解释：'+str(line1[4])+'\n建议：'+str(line1[5])+'\n'
        results+='\n'


        for i in range (len(report2)):
            line2=report2[i]
            results=results+'第'+str(i+1)+'次咨询  '+'日期：'+str(line2[1])+' 时间：'+str(line2[2])+'\n'
            results=results+'睡眠情况：'+str(line2[3])+'\n食欲情况：'+str(line2[4])+'\n情绪情况：'+str(line2[5])+'\n情绪分数：'+str(line2[6])+'\n情绪回答：'+str(line2[7])+'\n轻生倾向：'+str(line2[8])+'\n'
            results=results+'兴趣爱好分数：'+str(line2[9])+'\n兴趣爱好回答：'+str(line2[10])+'\n近期总体分数：'+str(line2[11])+'\n近期总体回答：'+str(line2[12])+'\n'+'最终建议：'+line2[13]+'\n\n'

    elif(is_usn):
        results='密码错误，无法读取报告数据。'
    else:
        results='账户不存在，无法读取报告数据。'

        
    return results


def delete_ui(username,password):
    if (username=='' or password==''):
        return '请填写完整信息'
    user_login_df=pd.read_csv('./user_login/login.csv',encoding='gbk',converters = {'password':str})
    user_login=user_login_df.set_index('username')['password'].T.to_dict()
    user_data1_df=pd.read_csv('./user_data/data_1.csv',encoding='gbk')
    user_data2_df=pd.read_csv('./user_data/data_2.csv',encoding='gbk',converters ={'senti_flt':float,'hobby_flt':float,'all_flt':float})

    results=''
    is_usn=(username in user_login)
    if(is_usn):
        pswd_crct=(password==user_login[username])
    if(is_usn and pswd_crct):
        user_data1_df.drop(user_data1_df[user_data1_df['username'] == username].index,inplace=True)
        user_data2_df.drop(user_data2_df[user_data2_df['username'] == username].index,inplace=True)
        user_login_df.drop(user_login_df[user_login_df['username'] == username].index,inplace=True)
        user_login_df.to_csv('./user_login/login.csv',encoding='gbk',index=False)
        user_data1_df.to_csv('./user_data/data_1.csv',encoding='gbk',index=False)
        user_data2_df.to_csv('./user_data/data_2.csv',encoding='gbk',index=False)
        results='已删除对应账户所有数据'
        
    elif(is_usn):
        results='密码错误，无法删除报告数据。'
    else:
        results='账户不存在，无法删除报告数据。'
    return results

###########################################################################################
def clear_info():
    return (
        gr.Textbox(""),
        gr.Textbox(""),
        gr.Textbox(""),
    )


with gr.Blocks() as user_center:
    with gr.Tab("查询历史"):   
        with gr.Row():
            gr.HTML("<h3 style='text-align:center;'>输入账号密码查看个人历史记录</h3>")
        with gr.Row():
            with gr.Column(scale=1):
                input_name1 = gr.Textbox(label="用户名",interactive=True)
                input_pwd1 = gr.Textbox(label="密码",interactive=True)
                with gr.Row():
                    clear_button1 = gr.Button("清除")
                    login_button1 = gr.Button("登录")
            with gr.Column(scale=1):
                output_info1 = gr.Textbox(label="输出", lines=5,interactive=False)
    with gr.Tab("清空数据"):
        with gr.Row():
            gr.HTML("<h3 style='text-align:center;'>输入账号密码清空个人历史记录与账号</h3>")
        with gr.Row():
            with gr.Column(scale=1):
                input_name2 = gr.Textbox(label="用户名",interactive=True)
                input_pwd2 = gr.Textbox(label="密码",interactive=True)
                with gr.Row():
                    clear_button2 = gr.Button("清除")
                    delete_button2 = gr.Button("登录")
            with gr.Column(scale=1):
                output_info2 = gr.Textbox(label="输出", lines=5,interactive=False)


    clear_button1.click(
        fn=clear_info,
        inputs=[],
        outputs=[input_name1, input_pwd1, output_info1],
    )
    login_button1.click(
        fn=read_ui,
        inputs=[input_name1, input_pwd1],
        outputs=output_info1,
    )
    clear_button2.click(
            fn=clear_info,
            inputs=[],
            outputs=[input_name2, input_pwd2, output_info2],
        )
    delete_button2.click(
        fn=delete_ui,
        inputs=[input_name2,input_pwd2],
        outputs=[output_info2],
    )