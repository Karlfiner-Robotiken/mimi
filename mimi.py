import json
import os
import random
import shutil
import signal
import subprocess
import time
from pathlib import Path

from pyfiglet import Figlet
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()
BASE_DIR = Path.home() / ".mimi"
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_FILE = MEMORY_DIR / "history.txt"
SETTINGS_FILE = BASE_DIR / "settings.json"
DEFAULT_SETTINGS = {
    "theme": "neon",
    "voice": True,
    "memory": True,
    "animations": True,
    "auto_update": True,
}


def ensure_files():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS.copy())


def load_settings():
    ensure_files()
    try:
        data = json.loads(SETTINGS_FILE.read_text())
        settings = DEFAULT_SETTINGS.copy()
        settings.update({k: v for k, v in data.items() if k in settings})
        return settings
    except (OSError, json.JSONDecodeError) as error:
        console.print(f"[yellow]Settings reset: {error}[/yellow]")
        save_settings(DEFAULT_SETTINGS.copy())
        return DEFAULT_SETTINGS.copy()


def save_settings(data):
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(data, indent=4) + "\n")


settings = load_settings()


def clear():
    console.clear()


def run_command(args, *, check=False, capture=False):
    command = shutil.which(args[0])
    if not command:
        console.print(f"[yellow]Optional command not found: {args[0]}[/yellow]")
        return None
    try:
        return subprocess.run([command, *args[1:]], check=check, text=True,
                              capture_output=capture)
    except (OSError, subprocess.SubprocessError) as error:
        console.print(f"[red]Command failed: {error}[/red]")
        return None


def ask_tgpt(prompt):
    result = run_command(["tgpt", prompt])
    if result is None:
        console.print("[yellow]Install tgpt with: npm install -g tgpt[/yellow]")


def boot_animation():
    frames = ["[" + "■" * i + "□" * (10 - i) + "]" for i in range(1, 11)]
    for frame in frames:
        clear()
        console.print("\n[bold magenta]Initializing MIMI AI[/bold magenta]")
        console.print(f"\n[cyan]{frame}[/cyan]")
        time.sleep(0.08)


def banner():
    clear()
    try:
        title = Figlet(font="slant").renderText("MIMI AI")
    except Exception:
        title = "MIMI AI"
    console.print(f"[bold magenta]{title}[/bold magenta]")
    console.print(Panel.fit(
        "[bold cyan]Termux AI command center[/bold cyan]\n"
        "[green]Powered by tgpt[/green]\n"
        "[yellow]Chat • Code • Search • Voice • Memory[/yellow]",
        border_style="magenta"))


def dashboard():
    table = Table(title="[bold cyan]MIMI COMMAND CENTER[/bold cyan]", box=box.DOUBLE_EDGE)
    table.add_column("OPTION", style="cyan", justify="center")
    table.add_column("FEATURE", style="green")
    for option, feature in [("1", "AI Chat"), ("2", "AI Coding Assistant"),
                            ("3", "Web Search"), ("4", "File Analyzer"),
                            ("5", "Voice Assistant"), ("6", "Autonomous AI Mode"),
                            ("7", "Memory Viewer"), ("8", "Plugin Manager"),
                            ("9", "Settings"), ("10", "System Information"),
                            ("11", "Update MIMI"), ("12", "Exit")]:
        table.add_row(option, feature)
    console.print(table)


def save_memory(text):
    if settings["memory"]:
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with MEMORY_FILE.open("a") as file:
            file.write(text + "\n")


def prompt_and_ask(label, prefix):
    prompt = Prompt.ask(label).strip()
    if prompt:
        save_memory(f"{prefix}: {prompt}")
        ask_tgpt(prompt)


def ai_chat():
    prompt_and_ask("[bold cyan]Ask MIMI[/bold cyan]", "CHAT")


def coding_assistant():
    prompt = Prompt.ask("[bold green]Describe code to generate[/bold green]").strip()
    if prompt:
        save_memory(f"CODE: {prompt}")
        ask_tgpt(f"Write production-ready code with comments and optimization for: {prompt}")


def web_search():
    query = Prompt.ask("[bold yellow]Search query[/bold yellow]").strip()
    if query:
        save_memory(f"SEARCH: {query}")
        ask_tgpt(f"Search and summarize with latest information: {query}")


def file_analyzer():
    path = Path(Prompt.ask("[bold magenta]Enter file path[/bold magenta]").expanduser())
    if not path.is_file():
        console.print("[red]File not found.[/red]")
        return
    try:
        content = path.read_text(errors="ignore")[:10000]
    except OSError as error:
        console.print(f"[red]Unable to read file: {error}[/red]")
        return
    save_memory(f"ANALYZE: {path}")
    ask_tgpt(f"Analyze this file content and explain it clearly:\n\n{content}")


def voice_mode():
    if not settings["voice"]:
        console.print("[yellow]Voice is disabled in Settings.[/yellow]")
        return
    text = Prompt.ask("[bold cyan]What should MIMI say?[/bold cyan]").strip()
    if text:
        run_command(["termux-tts-speak", text])


def autonomous_mode():
    topics = ["latest AI trends", "cybersecurity updates", "Linux optimization",
              "Termux automation", "future technology", "coding strategies"]
    console.print(Panel("[green]AUTONOMOUS MODE ACTIVE[/green]\nPress Ctrl+C to stop.", border_style="red"))
    try:
        while True:
            topic = random.choice(topics)
            console.print(f"\n[cyan]Thinking about:[/cyan] {topic}")
            ask_tgpt(f"Give futuristic insights on {topic}")
            time.sleep(10)
    except KeyboardInterrupt:
        console.print("\n[yellow]Autonomous mode stopped.[/yellow]")


def memory_viewer():
    memory = MEMORY_FILE.read_text(errors="ignore") if MEMORY_FILE.exists() else ""
    console.print(Panel(memory or "Empty memory", title="MIMI Memory", border_style="green"))


def plugin_manager():
    plugins = "\n".join(f"[green]✓[/green] {name}" for name in
                      ["coder", "search", "voice", "automation", "scraper", "analyzer"])
    console.print(Panel(plugins, title="Installed Plugins", border_style="cyan"))


def settings_menu():
    global settings
    console.print(Panel("[1] Toggle Voice\n[2] Toggle Memory\n[3] Toggle Animations\n[4] Reset Settings",
                        title="Settings", border_style="magenta"))
    choice = Prompt.ask("[cyan]Select[/cyan]")
    keys = {"1": "voice", "2": "memory", "3": "animations"}
    if choice in keys:
        settings[keys[choice]] = not settings[keys[choice]]
    elif choice == "4":
        settings = DEFAULT_SETTINGS.copy()
    else:
        console.print("[yellow]Unknown setting.[/yellow]")
    save_settings(settings)


def system_info():
    run_command(["neofetch"] if shutil.which("neofetch") else ["uname", "-a"])


def update_mimi():
    console.print("[green]Updating packages...[/green]")
    run_command(["pkg", "update", "-y"])
    run_command(["pkg", "upgrade", "-y"])
    run_command(["npm", "update", "-g", "tgpt"])


def main():
    if settings["animations"]:
        boot_animation()
    while True:
        banner()
        dashboard()
        choice = Prompt.ask("[bold cyan]Select option[/bold cyan]").strip()
        actions = {"1": ai_chat, "2": coding_assistant, "3": web_search,
                   "4": file_analyzer, "5": voice_mode, "6": autonomous_mode,
                   "7": memory_viewer, "8": plugin_manager, "9": settings_menu,
                   "10": system_info, "11": update_mimi}
        if choice == "12":
            clear()
            return
        action = actions.get(choice)
        if action:
            action()
        else:
            console.print("[yellow]Choose an option from 1 to 12.[/yellow]")
        Prompt.ask("\n[dim]Press ENTER to continue[/dim]", default="")


if __name__ == "__main__":
    main()
