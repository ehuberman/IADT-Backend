import re
from typing import Dict, List

def extract_players_by_position(text: str) -> Dict[str, List[str]]:
    positions = {
        "Goalkeeper": [],
        "Defenders": [],
        "Midfielders": [],
        "Forwards": []
    }

    # Extract the full "Recommended Lineup" section
    match = re.search(r"Recommended Lineup:\n\n(.*?)\n\nTactical approach:", text, re.DOTALL)
    if not match:
        return positions  # return empty structure if not found

    lineup_text = match.group(1)

    # Split into lines and assign to categories
    current_section = None
    for line in lineup_text.splitlines():
        line = line.strip()
        if not line:
            continue

        if "Goalkeeper:" in line:
            current_section = "Goalkeeper"
            name = line.split(":")[1].strip()
            positions[current_section].append(name)
        elif "Defenders:" in line:
            current_section = "Defenders"
        elif "Midfielders:" in line:
            current_section = "Midfielders"
        elif "Forwards:" in line:
            current_section = "Forwards"
        elif current_section and "-" in line:
            # extract text after the last colon or dash
            parts = re.split(r":|-", line)
            if len(parts) > 1:
                name = parts[-1].strip()
                positions[current_section].append(name)

    return positions
