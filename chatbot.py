import gradio as gr
import openai

openai.api_key = open("key.text", "r").read().strip('\n')

# when you want to use prompt
# messageHistory = [{"role": "user", "content": f"You are an expert programming chatBot, that can correct syntax errors and finding code bugs.. answer only in this matter"},
#                   {"role": "assistant", "content": f"OK"}]

messageHistory = []

def predict(input):
    global messageHistory
    messageHistory.append({"role": "user", "content": input})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messageHistory)

    replyContent = completion.choices[0].massage.content
    print(replyContent)
    messageHistory.append({"role": "assistant", "content": replyContent})
    response = [(messageHistory[i]["content"], messageHistory[i+1]["content"])
                for i in range(0, len(messageHistory) - 1, 2)]
    return response


with gr.Blocks() as demo:
    gptChatBot = gr.Chatbot()
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Type your massage...").style(
            container=False)
        txt.submit(predict, txt, gptChatBot)

        # lambda for Pythonic way....
        # txt.submit(lambda: " ", None, txt)
        # But JS do it Faster!
        txt.submit(None, None, txt, _js="() => {''} ")

demo.launch()
