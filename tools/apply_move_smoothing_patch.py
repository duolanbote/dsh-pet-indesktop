from pathlib import Path

path = Path('pet/window.py')
text = path.read_text(encoding='utf-8')

old = '''        # ---- 移动驱动 ----\n        self._move_plan: dict | None = None\n        self._move_timer = QTimer(self)\n        self._move_timer.setInterval(33)         # ~30fps 位置插值\n        self._move_timer.timeout.connect(self._on_move_tick)\n\n        # ---- 交互节拍跟随屏幕刷新率 ----\n'''
new = '''        # ---- 移动驱动 ----\n        self._move_plan: dict | None = None\n        self._move_timer = QTimer(self)\n        self._move_timer.timeout.connect(self._on_move_tick)\n\n        # ---- 交互节拍跟随屏幕刷新率 ----\n'''
assert old in text, 'move timer block not found'
text = text.replace(old, new, 1)

old = '''        _tick_ms = max(4, round(1000.0 / _refresh)) if _refresh > 90.0 else 16\n\n        # ---- 点击 Q 弹效果 ----\n'''
new = '''        _tick_ms = max(4, round(1000.0 / _refresh)) if _refresh > 90.0 else 16\n\n        # 移动窗口与屏幕刷新节拍对齐；固定 33ms (~30fps) 在 60/120/165Hz\n        # 显示器上都会产生可见的步进抖动。与物理/Q 弹路径统一使用精确定时器。\n        self._move_timer.setInterval(_tick_ms)\n        self._move_timer.setTimerType(Qt.TimerType.PreciseTimer)\n\n        # ---- 点击 Q 弹效果 ----\n'''
assert old in text, 'refresh tick block not found'
text = text.replace(old, new, 1)

old = '''        t = self.movie.currentTimeSeconds()\n        lead, tail = catalog.MOVE_LEAD_SEC, catalog.MOVE_TAIL_SEC\n        dur = plan['duration']\n        if t <= lead:\n'''
new = '''        t = self.movie.currentTimeSeconds()\n        dur = plan['duration']\n        lead, tail = catalog.MOVE_LEAD_SEC, catalog.MOVE_TAIL_SEC\n        # 短移动素材（例如 5s 的「站姿→走路→站姿」）若仍固定前后各 2s，\n        # 实际位移会被压缩到约 1s，窗口看起来像突然冲过去。仅当默认前后缓冲\n        # 已占到素材一半以上时，把两侧缓冲各限制到素材时长的 10%；长素材\n        # 继续保留历史的 2s/2s 行为。\n        if dur > 0 and lead + tail >= dur * 0.5:\n            lead = min(lead, dur * 0.10)\n            tail = min(tail, dur * 0.10)\n        if t <= lead:\n'''
assert old in text, 'move timing block not found'
text = text.replace(old, new, 1)

old = '''  - 移动：动画只提供"走路姿态"（3 选 1），位置由 QTimer 驱动，\n    开头/结尾各 2s 不动，中间按播放进度插值；\n'''
new = '''  - 移动：动画提供起步/走路/收步姿态，位置由 QTimer 驱动；\n    长素材保留前后各 2s 缓冲，短素材自动缩短缓冲，中间按播放进度插值；\n'''
assert old in text, 'module move comment not found'
text = text.replace(old, new, 1)

path.write_text(text, encoding='utf-8', newline='\n')
