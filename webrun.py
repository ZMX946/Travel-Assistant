import gradio as gr
from graph.graph import init_app
from utils.helper import save_chat_history, get_thread_id
from langchain_core.messages import HumanMessage
import warnings
from langchain_core._api.beta_decorator import LangChainBetaWarning
from dotenv import load_dotenv, find_dotenv
warnings.filterwarnings("ignore", category=LangChainBetaWarning)


_ = load_dotenv(find_dotenv())

app = init_app(model_name="qwen-max")
thread_id = get_thread_id()
print('thread_id:',thread_id)
config = {"configurable": {"thread_id": thread_id}}

async def process_message(user_message, chatbot_history, debug_history):
    chatbot_history.append((user_message, None))  # 没有标签的用户消息
    formatted_user_message = HumanMessage(content=user_message)
    print('formatted_user_message:',formatted_user_message)

    async for event in app.astream_events({"messages": formatted_user_message}, config=config, version="v1"):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                # 增量更新AI的最后一条消息
                if chatbot_history and chatbot_history[-1][1] is not None:
                    chatbot_history[-1] = (chatbot_history[-1][0], chatbot_history[-1][1] + content)
                    print('chatbot_history1：',chatbot_history)
                else:
                    chatbot_history[-1] = (chatbot_history[-1][0], content)  # 添加第一个块
                yield chatbot_history, debug_history  # 确保流式更新
        elif kind == "on_tool_start":
            debug_history += f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}\n"
            print('debug_history2:',debug_history)
            yield chatbot_history, debug_history  # Stream 工具开始信息

        elif kind == "on_tool_end":
            debug_history += f"Done tool: {event['name']}\nTool output: {event['data'].get('output')}\n--\n"
            print('debug_history3:',debug_history)
            yield chatbot_history, debug_history  # Stream 工具结束信息


def clear_input():
    return ""


def start_gradio():
    with gr.Blocks() as demo:
        gr.Markdown("# 基于Langgraph的旅游规划助手")

        with gr.Row(equal_height=True) as chat_interface:
            chat_interface.elem_classes = ["full-height"]
            # 调试信息的左栏
            with gr.Column(scale=1):
                debug_info = gr.Textbox(
                    label="Debug Info",
                    lines=30,
                    interactive=False,
                    elem_id="debug-info"
                )

            # 聊天界面的右栏
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="User-AI Chat",
                    show_label=False,
                    elem_id="chatbot"
                )

                user_input = gr.Textbox(
                    label="Your message",
                    placeholder="Type your message here",
                    lines=3,
                    max_lines=5,
                    show_label=False,
                    elem_id="user-input"
                )

                submit_click = gr.Button("Send")  # 消息输入的提交功能

        def submit_action():
            return process_message, [user_input, chatbot, debug_info], [chatbot, debug_info]

        submit_click.click(*submit_action()).then(
            clear_input, None, user_input
        )

        user_input.submit(*submit_action()).then(
            clear_input, None, user_input
        )

    demo.launch()

# 程序主入口
if __name__ == "__main__":
    start_gradio()

