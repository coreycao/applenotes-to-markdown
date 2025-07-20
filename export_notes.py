import subprocess
import os
import re
from markdownify import markdownify as md

def run_applescript(script: str) -> str:
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.stdout.strip()

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', name).strip()

def get_folders():
    script = '''
    tell application "Notes"
        set folderNames to name of every folder
        set AppleScript's text item delimiters to "|||"
        return folderNames as string
    end tell
    '''
    output = run_applescript(script)
    return [name.strip() for name in output.split("|||") if name.strip()]

def get_note_titles(folder_name: str):
    script = f'''
    tell application "Notes"
        set theFolder to folder "{folder_name}"
        set noteTitles to name of every note of theFolder
        set AppleScript's text item delimiters to "|||"
        return noteTitles as string
    end tell
    '''
    output = run_applescript(script)
    return [title.strip() for title in output.split("|||") if title.strip()]

def get_note_body(folder_name: str, note_index: int):
    script = f'''
    tell application "Notes"
        set theFolder to folder "{folder_name}"
        set theNotes to notes of theFolder
        set theNote to item {note_index} of theNotes
        set noteBody to the body of theNote
        return noteBody
    end tell
    '''
    return run_applescript(script)

def export_note(title: str, body: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    filename = sanitize_filename(title) + ".md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md(body))
    print(f"✅ Exported: {filepath}")

while True:
    print("📁 Folders in Apple Notes:")
    folder_names = get_folders()
    for idx, name in enumerate(folder_names):
        print(f"{idx}: {name}")
    choice = input("\nEnter the Folder Index to view (or type exit to quit): ").strip()
    if choice.lower() == "exit":
        print("👋 Goodbye!")
        break
    if not choice.isdigit() or int(choice) not in range(len(folder_names)):
        print("❌ Invalid index.")
        continue

    selected_folder = folder_names[int(choice)]
    print(f"\n📂 Selected folder: {selected_folder}")

    note_titles = get_note_titles(selected_folder)
    if not note_titles:
        print("(Empty Folder)")
        continue

    while True:
        print(f"\n📝 Note titles in folder \"{selected_folder}\":")
        for i, title in enumerate(note_titles):
            print(f"{i + 1}. {title}")
        user_input = input("\nEnter Note Index to export, 'all' to export all, or 'exit' to leave this folder: ").strip().lower()

        if user_input == "exit":
            break
        elif user_input == "all":
            print(f"\n🚀 Exporting all notes from \"{selected_folder}\"...")
            for i, title in enumerate(note_titles):
                body = get_note_body(selected_folder, i + 1)
                export_note(title, body, "note_output")
            print("🎉 All notes have been exported.")
        elif user_input.isdigit():
            idx = int(user_input)
            if 1 <= idx <= len(note_titles):
                title = note_titles[idx - 1]
                body = get_note_body(selected_folder, idx)
                export_note(title, body, "note_output")
            else:
                print("❌ Note index is out of range, please try again.")
        else:
            print("❌ Invalid input. Please enter a number, 'all', or 'exit'.")
