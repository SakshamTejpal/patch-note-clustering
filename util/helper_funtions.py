import json
import re
from typing import Generator, List
from util.file_handler import FileHandler
from util.game_data import GameData
from util.cluster import SingleNote

class HelperFunctions:
    
    @staticmethod
    def extract_json(raw_text: str):
        if not isinstance(raw_text, str):
            raise ValueError("LLM response is not a string.")

        cleaned = raw_text.strip()

        # Remove markdown code fences 
        if cleaned.startswith("```"):
            cleaned = HelperFunctions._strip_fences(cleaned)

        json_ready = HelperFunctions._remove_invalid_escapes(cleaned)
        return json.loads(json_ready)

    @staticmethod
    def _strip_fences(text: str) -> str:
        text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE).strip()
        if text.endswith("```"):
            text = text[:-3].strip()
        return text

    @staticmethod
    def _remove_invalid_escapes(text: str) -> str:
        return re.sub(
            r'\\(?!["\\/bfnrtu])',   # match \ NOT followed by valid escapes
            lambda m: '\\' + m.group(0),
            text
        )

    @staticmethod
    def seprating_notes(game: GameData) -> list[SingleNote]:
        separated_notes = []
        for note in game.notes:
            single_note = SingleNote(
                app_id=game.app_id,
                title=note.title,
                content=note.content
            )
            # separated_notes.append(single_note.to_dict())
            separated_notes.append(single_note)
        return separated_notes

    @staticmethod
    def generate_batches(file_handler: FileHandler) -> Generator[List[SingleNote], None, None]:
        BATCH_SIZE = 30
        buffer: List[SingleNote] = []

        for game in file_handler.import_games():
            notes = HelperFunctions.seprating_notes(game)
            buffer.extend(notes)

            # Yield batches of 30 notes
            while len(buffer) >= BATCH_SIZE:
                batch = buffer[:BATCH_SIZE]
                buffer = buffer[BATCH_SIZE:]
                yield batch

        # Leftover batch
        if buffer:
            yield buffer

    @staticmethod
    def contains_injection(text):
        bad_phrases = [
            "ignore previous instructions",
        ]
        text_lower = text.lower()
        if any(phrase in text_lower for phrase in bad_phrases):
            return True
        return False