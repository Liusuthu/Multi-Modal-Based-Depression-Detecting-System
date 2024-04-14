# 📈Multi-Modal-Based-Depression-Dection-System📋
The 42nd THU Challenge Cup🏆 entry , built on the Gradio SDK framework and deployed on HuggingFace Space.


### 📚️Description
*Below are some description of this system, including the basic information and how to use it.*<br>
The purpose of this system is to provide an easy way to detect depression, provide timely primary diagnosis and alert treatment for users who may be at potential risk of depression. The system consists of a fusion of video, audio, and text modal models for Chinese language environments, it also accesses to a large language model API to achieve a more humanized consultation experience.
##### 📋Testing Mode
Including three sub-modes:<br>
1. Basic Scale Test: a scale test based on SDS(Self-rating depression scale), which is traditional and effective.<br>
2. Structured Consultancy: a consultancy test with a relatively fixed structure, including sleeping condition, dietary situation, mood condition, daily hobbies, recent affairs, etc.<br>
3. Scale and Consultancy: firstly complete a SDS scale, and the the LLM(GPT-4) will give an consultancy based on the content of the scale, the multi-modal information is collected during the consultancy.

##### 💬Chatting Mode
Users can share their daily things and get emotion needs with the chattin grobot.

##### 🗃️User Center
Users can manage their private data in this mode, including querying and deleting.

##### 📞Helpline Info
Offering some helpline in THU and Beijing.


### ⛓️Links
1. https://huggingface.co/spaces/Liusuthu/Portable-Depression-Detecting-System (the official page in HF)
2. https://hf-mirror.com/spaces/Liusuthu/Portable-Depression-Detecting-System (the mirror website of 1.)
3. https://liusuthu-portable-depression-detecting-system.hf.space (the pure version)

### 💐Acknowledges
◽ Special thanks to Dr.Wei-Qiang ZHANG, director of SATLAB for his vital help.<br>
◽ Many thanks to Yuhang Zhao in SATLAB for offering the audio model XLSR-Chinese.<br>
◽ Thanks to Elena Ryumina et al. for their Facial Expressions Recognition Model(EMO-AffectNetModel).<br>
◽ Thanks to all those friends who join the internal testing and give us feedbacks.<br>
◽ Thanks to all who offered help to this project.<br>

