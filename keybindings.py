from PyQt6.QtGui import QKeySequence, QShortcut

def setup_shortcuts(widget):
    """
    设置快捷键
    """
    QShortcut(QKeySequence("Space"), widget, widget.toggle_timer)
    QShortcut(QKeySequence("1"), widget, lambda: widget.set_timer_interval(1000))
    QShortcut(QKeySequence("2"), widget, lambda: widget.set_timer_interval(500))
    QShortcut(QKeySequence("3"), widget, lambda: widget.set_timer_interval(100))
    QShortcut(QKeySequence("4"), widget, lambda: widget.set_timer_interval(10))
