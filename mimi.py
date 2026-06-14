import os
import json
import time
import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box
from pyfiglet import Figlet

console = Console()

MEMORY_FILE = os.path.expanduser("~/.mimi/memory/history.txt")
SETTINGS_FILE = os.path.expanduser("~/.mimi/settings.json")

DEFAULT_SETTINGS = {
    "theme": "neon",
    "voice": True,
    "memory": True,
    "animations": True,
    "auto_update": True
}

if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(DEFAULT_SETTINGS, f, indent=4)

with open(SETTINGS_FILE) as f:
    settings = json.load(f)

def clear():
    os.system("clear")

def boot_animation():
    frames = [
        "[■□□□□□□□□□]",
        "[■■□□□□□□□□]",
        "[■■■□□□□□□□]",
        "[■■■■□□□□□□]",
        "[■■■■■□□□□□]",
        "[■■■■■■□□□□]",
        "[■■■■■■■□□□]",
        "[■■■■■■■■□□]",
        "[■■■■■■■■■□]",
        "[■■■■■■■■■■]"
    ]

    for frame in frames:
        clear()
        console.print(f"\n\n[bold magenta]Initializing MIMI AI[/bold magenta]")
        console.print(f"\n[cyan]{frame}[/cyan]")
        time.sleep(0.15)

def banner():
    clear()

    fig = Figlet(font="slant")
    title = fig.renderText("MIMI AI")

    console.print(f"[bold magenta]{title}[/bold magenta]")

    console.print(
        Panel.fit(
            "[bold cyan]Ultimate Futuristic AI Agent[/bold cyan]\n"
            "[green]Powered by tgpt + Termux[/green]\n"
            "[yellow]Autonomous • Coding • Search • Voice • Memory[/yellow]",
            border_style="magenta"
        )
    )

def dashboard():
    table = Table(
        title="[bold cyan]MIMI COMMAND CENTER[/bold cyan]",
        box=box.DOUBLE_EDGE
    )

    table.add_column("OPTION", style="cyan", justify="center")
    table.add_column("FEATURE", style="green")

    features = [
        ("1", "AI Chat"),
        ("2", "AI Coding Assistant"),
        ("3", "Web Search"),
        ("4", "File Analyzer"),
        ("5", "Voice Assistant"),
        ("6", "Autonomous AI Mode"),
        ("7", "Memory Viewer"),
        ("8", "Plugin Manager"),
        ("9", "Settings"),
        ("10", "System Information"),
        ("11", "Update MIMI"),
        ("12", "Exit")
    ]

    for opt, feat in features:
        table.add_row(opt, feat)

    console.print(table)

def save_memory(text):
    with open(MEMORY_FILE, "a") as f:
        f.write(text + "\n")

def ai_chat():
    prompt = Prompt.ask("[bold cyan]Ask MIMI[/bold cyan]")

    if settings["memory"]:
        save_memory(f"CHAT: {prompt}")

    os.system(f'tgpt "{prompt}"')

def coding_assistant():
    prompt = Prompt.ask("[bold green]Describe code to generate[/bold green]")

    full = f"Write production-ready code with comments and optimization for: {prompt}"

    if settings["memory"]:
        save_memory(f"CODE: {prompt}")

    os.system(f'tgpt "{full}"')

def web_search():
    query = Prompt.ask("[bold yellow]Search Query[/bold yellow]")

    full = f"Search and summarize with latest information: {query}"

    if settings["memory"]:
        save_memory(f"SEARCH: {query}")

    os.system(f'tgpt "{full}"')

def file_analyzer():
    path = Prompt.ask("[bold magenta]Enter file path[/bold magenta]")

    if not os.path.exists(path):
        console.print("[red]File not found.[/red]")
        return

    with open(path, "r", errors="ignore") as f:
        content = f.read()[:5000]

    with open("/tmp/mimi_analysis.txt", "w") as temp:
        temp.write(content)

    os.system(
        'tgpt "Analyze this file content and explain everything:\n$(cat /tmp/mimi_analysis.txt)"'
    )

def voice_mode():
    text = Prompt.ask("[bold cyan]What should MIMI say?[/bold cyan]")
    os.system(f'termux-tts-speak "{text}"')

def autonomous_mode():
    console.print(
        Panel(
            "[green]AUTONOMOUS MODE ACTIVE[/green]\n"
            "MIMI will continuously generate insights.",
            border_style="red"
        )
    )

    while True:
        try:
            topic = random.choice([
                "latest AI trends",
                "cybersecurity updates",
                "Linux optimization",
                "Termux automation",
                "future technology",
                "coding strategies"
            ])

            console.print(f"\n[cyan]Thinking about:[/cyan] {topic}")

            os.system(f'tgpt "Give futuristic insights on {topic}"')

            time.sleep(10)

        except KeyboardInterrupt:
            break

def memory_viewer():
    if not os.path.exists(MEMORY_FILE):
        console.print("[yellow]No memory yet.[/yellow]")
        return

    with open(MEMORY_FILE) as f:
        memory = f.read()

    console.print(
        Panel(
            memory if memory else "Empty memory",
            title="MIMI Memory",
            border_style="green"
        )
    )

def plugin_manager():
    plugins = [
        "coder",
        "search",
        "voice",
        "automation",
        "scraper",
        "analyzer"
    ]

    txt = "\n".join([f"[green]✔[/green] {p}" for p in plugins])

    console.print(
        Panel(
            txt,
            title="Installed Plugins",
            border_style="cyan"
        )
    )

def settings_menu():
    global settings

    console.print(
        Panel(
            "[1] Toggle Voice\n"
            "[2] Toggle Memory\n"
            "[3] Toggle Animations\n"
            "[4] Reset Settings",
            title="Settings",
            border_style="magenta"
        )
    )

    choice = Prompt.ask("[cyan]Select[/cyan]")

    if choice == "1":
        settings["voice"] = not settings["voice"]

    elif choice == "2":
        settings["memory"] = not settings["memory"]

    elif choice == "3":
        settings["animations"] = not settings["animations"]

    elif choice == "4":
        settings = DEFAULT_SETTINGS

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def system_info():
    os.system("neofetch || uname -a")

def update_mimi():
    console.print("[green]Updating packages...[/green]")

    os.system("pkg update -y && pkg upgrade -y")
    os.system("npm update -g tgpt")

def main():
    if settings["animations"]:
        boot_animation()

    while True:
        banner()
        dashboard()

        choice = Prompt.ask("[bold cyan]Select Option[/bold cyan]")

        if choice == "1":
            ai_chat()

        elif choice == "2":
            coding_assistant()

        elif choice == "3":
            web_search()

        elif choice == "4":
            file_analyzer()

        elif choice == "5":
            voice_mode()

        elif choice == "6":
            autonomous_mode()

        elif choice == "7":
            memory_viewer()

        elif choice == "8":
            plugin_manager()

        elif choice == "9":
            settings_menu()

        elif choice == "10":
            system_info()

        elif choice == "11":
            update_mimi()

        elif choice == "12":
            clear()
            break

        input("\nPress ENTER to continue...")

if __name__ == "__main__":
    main()
