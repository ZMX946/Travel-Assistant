from langchain_core.tools import tool
from typing import Annotated, Tuple

@tool(response_format="content_and_artifact")
def save_info_and_clear_history(
    infomation_to_save: Annotated[str, "需要保存的有用信息。主要是你调用的工具返回给你的信息中有用的部分。尽量详细。"],
) -> Tuple[str, str]:
    """信息保存工具。保存当前已获取的有用信息。"""
    # 事实上，由于LangGraph工具没有更新图形状态的能力，我们只将工具消息返回给主代理。
    # 图形状态的更新将在主代理逻辑中处理。
    content = "信息已保存。"
    # LLM仅获取内容，要保存的信息将保存在工具消息的 'artifact' 字段中.
    return content, infomation_to_save

# test the tool
if __name__ == "__main__":
    print(save_info_and_clear_history.args_schema.model_json_schema())
    tool_call =     {
        "name": "save_info_and_clear_history",
        "args": {"infomation_to_save": "2025年3月14日"},
        "id": "123",  # required
        "type": "tool_call",  # required
    }
    a=save_info_and_clear_history.invoke(tool_call)
    print(a)