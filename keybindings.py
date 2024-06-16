from PyQt6.QtGui import QShortcut, QKeySequence
from config import TIMER_INTERVALS

def setup_shortcuts(widget):
    """
    为指定的 widget 设置快捷键
    """
    QShortcut(QKeySequence("Space"), widget, widget.toggle_timer)
    QShortcut(QKeySequence("1"), widget, lambda: widget.set_timer_interval(TIMER_INTERVALS['1']))
    QShortcut(QKeySequence("2"), widget, lambda: widget.set_timer_interval(TIMER_INTERVALS['2']))
    QShortcut(QKeySequence("3"), widget, lambda: widget.set_timer_interval(TIMER_INTERVALS['3']))
    QShortcut(QKeySequence("4"), widget, lambda: widget.set_timer_interval(TIMER_INTERVALS['4']))
