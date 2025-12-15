import re
import OpenAIClient
import Config
import tools

if __name__ == "__main__":
    client = OpenAIClient.OpenAICompatibleClient(model=Config.model, api_key=Config.api_key, base_url=Config.base_url)
    user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
    prompt_history = [f"用户请求：{user_prompt}"]

    print(f"用户输入：{user_prompt}\n" + "="*50)

    for i in range(3):
        print(f"--- 循环 {i+1} ---\n")
        full_prompt = "\n".join(prompt_history)
        llm_output = client.generate(full_prompt, Config.AGENT_SYSTEM_PROMPT)
        # 模型可能会输出多余的Thought-Action，需要截断
        match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
        if match:
            truncated = match.group(1).strip()
            if truncated != llm_output.strip():
                llm_output = truncated
                print("已截断多余的 Thought-Action 对")
        print(f"模型输出:\n{llm_output}\n")
        prompt_history.append(llm_output)

        # 解析 Action（捕获整段以便后续提取函数与参数）
        action_match = re.search(r'Action:\s*(.+)', llm_output, re.DOTALL)
        if not action_match:
            print("未检测到 Action，结束循环。\n")
            break
        action_str = action_match.group(1).strip()

        # 处理任务完成
        if action_str.lower().startswith("finish"):
            m_finish = re.search(r'finish\(answer="(.*)"\)', action_str, re.DOTALL)
            if m_finish:
                final_answer = m_finish.group(1)
            else:
                final_answer = action_str
            print(f"任务完成，最终答案: {final_answer}")
            break

        # 提取工具名与参数，增加健壮性判断
        m_tool = re.search(r"(\w+)\(", action_str)
        m_args = re.search(r"\((.*)\)", action_str, re.DOTALL)
        if not m_tool or not m_args:
            print(f"无法解析 Action 内容：{action_str}\n")
            break
        tool_name = m_tool.group(1)
        args_str = m_args.group(1)
        kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

        # 使用 tools.available_tools 调用
        if tool_name in tools.available_tools:
            observation = tools.available_tools[tool_name](**kwargs)
        else:
            observation = f"错误:未定义的工具 '{tool_name}'"
        # 3.4. 记录观察结果
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)

