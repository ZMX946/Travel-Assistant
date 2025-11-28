import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def test_langchain_openai_compatibility(api_base_url, api_key, model_name):
    try:
        # 初始化ChatOpenAI实例
        llm = ChatOpenAI(
            base_url=api_base_url,
            api_key=api_key,
            model=model_name,
            temperature=0.7,
            max_tokens=100
        )

        # 发送测试消息
        messages = [HumanMessage(content="Hello, world!")]
        response = llm.invoke(messages)

        # 验证响应格式
        if hasattr(response, 'content') and response.content:
            return True, "兼容LangChain OpenAI接口"
        else:
            return False, "无效的响应格式"

    except Exception as e:
        return False, f"兼容性测试失败: {str(e)}"


def test_langchain_streaming(api_base_url, api_key, model_name):
    try:
        llm = ChatOpenAI(
            base_url=api_base_url,
            api_key=api_key,
            model=model_name,
            streaming=True
        )

        messages = [HumanMessage(content="Count from 1 to 5")]

        # 测试流式响应
        chunks = []
        for chunk in llm.stream(messages):
            chunks.append(chunk.content)

        if len(chunks) > 0:
            return True, "流式输出工作正常"
        else:
            return False, "没有接收到流式内容"

    except Exception as e:
        return False, f"流式输出兼容性测试失败: {str(e)}"


def comprehensive_langchain_test(api_base_url, api_key, model_name):
    """
    使用LangChain进行完整的OpenAI兼容性测试
    """
    print(f"测试LangChain OpenAI的兼容性： {model_name}")

    # 测试基本调用
    is_compatible, message = test_langchain_openai_compatibility(
        api_base_url, api_key, model_name
    )

    if not is_compatible:
        return False

    print("✓ 普通输出正常")

    # 测试流式响应
    stream_compatible, stream_message = test_langchain_streaming(
        api_base_url, api_key, model_name
    )

    if stream_compatible:
        print("✓ 流式输出正常")
        return True
    else:
        print(f"⚠ 非流式输出：{stream_message}")
        return False


# 使用示例
if __name__ == "__main__":
    load_dotenv()
    # 测试阿里云
    result = comprehensive_langchain_test(
        api_base_url=os.getenv("API_BASE_URL"),
        api_key=os.getenv("LLM_API_KEY"),
        model_name="qwen-max"
    )
    print(f"Result: {result}")

