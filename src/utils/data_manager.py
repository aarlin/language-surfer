import json
import os
from datetime import datetime, timedelta
from typing import Dict, List

class DataManager:
    def __init__(self):
        self.data_file = "game_data.json"
        self.load_data()
        
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "characters": {},
                "scores": [],
                "srs_data": {}
            }
            self.save_data()
            
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
            
    def add_character(self, character: str, meaning: str, lane: int):
        if character not in self.data["characters"]:
            self.data["characters"][character] = {
                "meaning": meaning,
                "correct_lane": lane,
                "times_seen": 0,
                "times_correct": 0,
                "last_seen": None,
                "next_review": None
            }
            self.save_data()
            
    def update_srs(self, character: str, was_correct: bool):
        if character in self.data["characters"]:
            char_data = self.data["characters"][character]
            char_data["times_seen"] += 1
            if was_correct:
                char_data["times_correct"] += 1
                
            # Simple SRS algorithm
            if was_correct:
                # Increase interval by 1.5x each time
                current_interval = char_data.get("interval", 1)
                new_interval = int(current_interval * 1.5)
            else:
                # Reset interval if wrong
                new_interval = 1
                
            char_data["interval"] = new_interval
            char_data["last_seen"] = datetime.now().isoformat()
            char_data["next_review"] = (datetime.now() + timedelta(days=new_interval)).isoformat()
            
            self.save_data()
            
    def add_score(self, score: int, level: int, characters_seen: int):
        self.data["scores"].append({
            "score": score,
            "level": level,
            "characters_seen": characters_seen,
            "timestamp": datetime.now().isoformat()
        })
        self.save_data()
        
    def get_next_review_characters(self) -> List[str]:
        now = datetime.now()
        return [
            char for char, data in self.data["characters"].items()
            if data["next_review"] and datetime.fromisoformat(data["next_review"]) <= now
        ]
        
    def get_character_stats(self, character: str) -> Dict:
        return self.data["characters"].get(character, {}) 