import json
import os

transcript_path = "/Users/mutahanaka/.gemini/antigravity/brain/225021a5-8b93-43d7-a567-ccac2f001804/.system_generated/logs/transcript_full.jsonl"

def extract_old_index():
    if not os.path.exists(transcript_path):
        print("Transcript not found.")
        return
        
    # We want to find a state of index.html from roughly "2 hours ago".
    # Or just the first state we ever saw index.html in this session.
    # We will look through the transcript for tool calls to view_file or read_file on index.html
    # and print their timestamp and length.
    
    with open(transcript_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        data = json.loads(line)
        content = data.get("content", "")
        # Look for the output of read_file or view_file or a python script that printed it
        # Actually, let's look for "Created At:" and "File Path: .*index.html"
        if "File Path:" in content and "index.html" in content and "Showing lines" in content:
            # This is a view_file output. It might not have the full file.
            pass
        
        # Did I do a read_file on index.html?
        tool_calls = data.get("tool_calls", [])
        for call in tool_calls:
            # check if there's a write_to_file for index.html?
            if call.get("name") == "write_to_file":
                args = call.get("arguments", {})
                if "index.html" in args.get("TargetFile", ""):
                    print(f"Step {data.get('step_index')}: Wrote to index.html")
                    
        # Let's check for any mention of the full index.html content
        # For example, if a python script printed it, or if it was in the initial prompt?
        
    print("Done scanning.")

extract_old_index()
