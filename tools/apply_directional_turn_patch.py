from pathlib import Path
import json

window = Path('pet/window.py')
text = window.read_text(encoding='utf-8')
old = """        skip_facing = getattr(self, '_effects_skip_turn_facing', None)\n        if name in self.turns and not (callable(skip_facing) and skip_facing()):\n            self.facing = 'right' if self.facing == 'left' else 'left'\n"""
new = """        skip_facing = getattr(self, '_effects_skip_turn_facing', None)\n        if name in self.turns and not (callable(skip_facing) and skip_facing()):\n            # Directional turn assets own their visual direction and must not be\n            # followed by the legacy blind facing toggle.  Keep the old toggle\n            # as a fallback for existing character packs.\n            if name == 'turn_left':\n                self.facing = 'left'\n            elif name == 'turn_right':\n                self.facing = 'right'\n            else:\n                self.facing = 'right' if self.facing == 'left' else 'left'\n"""
assert old in text, 'turn facing block not found'
window.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')

no_mirror = Path('characters/cc_chibi/videos/text_clips.json')
no_mirror.parent.mkdir(parents=True, exist_ok=True)
no_mirror.write_text(json.dumps({'no_mirror': ['turn_left', 'turn_right']}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
