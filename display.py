import rich.rule
import rich.panel
from rich.console import Console

console = Console(record=True)

def print_tool_result(name, result):
    console.print(rich.panel.Panel(result[:500], title=name,
                                   border_style="green"))

def print_recall(hits):
    lines = []
    for score, record in hits:
        lines.append(f"[bold]{score:.3f}[/bold]  {record['file_name']}")
        lines.append(f"         [dim]{record['docstring']}[/dim]")
        for fn in record['functions']:
            sig = f"{fn['name']}({', '.join(fn['args'])}) -> {fn['returns']}"
            lines.append(f"         [cyan]{sig}[/cyan] [dim]{fn['doc']}[/dim]")
    console.print(rich.panel.Panel("\n".join(lines), title="recall",
                                   border_style="magenta"))

def call_name(call):
    """Get the tool name from either an ollama ToolCall or a plain dict."""
    try:
        return call.function.name
    except AttributeError:
        return call['function']['name']

def call_args(call):
    """Get the arguments dict from either an ollama ToolCall or a plain dict."""
    try:
        return call.function.arguments
    except AttributeError:
        return call['function']['arguments']

def render_messages(agent):
    """Turn the current message list into a list of printable panels."""
    out = []
    for msg in agent.messages:
        role = msg.get('role')

        if role == 'system':
            out.append(rich.panel.Panel(msg['content'], title="system",
                                        border_style="yellow"))

        elif role == 'user':
            out.append(rich.panel.Panel(msg['content'], title="user",
                                        border_style="blue"))

        elif role == 'assistant':
            body = ""
            if msg.get('thinking'):
                body += f"[dim]{msg['thinking']}[/dim]\n\n"
            if msg.get('content'):
                body += msg['content']
            for call in msg.get('tool_calls', []):
                args = ", ".join(f"{k}={v!r}" for k, v in call_args(call).items())
                body += f"\n[cyan]{call_name(call)}([/cyan]{args}[cyan])[/cyan]"
            out.append(rich.panel.Panel(body.strip() or "[dim](empty)[/dim]",
                                        title="assistant", border_style="white"))

        elif role == 'tool':
            out.append(rich.panel.Panel(msg['content'],
                                        title=msg.get('tool_name', 'tool'),
                                        border_style="green"))
    return out

def stream_response(stream) -> dict:
    is_thinking = False
    new_message = {'thinking': '', 'content': '', 'tool_calls': []}
    for chunk in stream:
        if chunk.message.thinking:
            if not is_thinking:
                console.print(rich.rule.Rule("[dim]thinking[/dim]", style="dim"))
                is_thinking = True
            new_message['thinking'] += chunk.message.thinking
            console.print(chunk.message.thinking, end='', style="dim",
                          highlight=False, soft_wrap=True)
        if chunk.message.content:
            if is_thinking:
                console.print(rich.rule.Rule("[bold]answer[/bold]"))
                is_thinking = False
            new_message['content'] += chunk.message.content
            console.print(chunk.message.content, end='', highlight=False,
                          soft_wrap=True)
        if chunk.message.tool_calls:
            new_message['tool_calls'].extend(chunk.message.tool_calls)
    if new_message['tool_calls']:
        console.print(rich.rule.Rule("[cyan]tool calls[/cyan]", style="cyan"))
        console.print(new_message['tool_calls'])
    return new_message
