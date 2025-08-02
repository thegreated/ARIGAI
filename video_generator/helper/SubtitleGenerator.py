import re

class SubtitleGenerator:

    def __init__(self, segments, max_chars=70):
        self.segments = segments
        self.max_chars = max_chars

    def split_text(self, text):
        # Smart split at sentence or length
        parts = re.split(r'(?<=[.?!])\s+', text.strip())
        if len(parts) > 1:
            return [p for p in parts if p]
        words = text.split()
        if len(text) <= self.max_chars or len(words) <= 1:
            return [text]
        mid = len(words) // 2
        return [" ".join(words[:mid]), " ".join(words[mid:])]

    def generate(self):
        subtitle_list = []
        for seg in self.segments:
            start, end = seg["start"], seg["end"]
            text = seg["text"].strip()
            parts = self.split_text(text)
            if len(parts) == 1:
                subtitle_list.append(((start, end), text))
            else:
                total = end - start
                part_dur = total / len(parts)
                for i, part in enumerate(parts):
                    s = start + i * part_dur
                    e = start + (i + 1) * part_dur
                    subtitle_list.append(((s, e), part.strip()))
        return subtitle_list