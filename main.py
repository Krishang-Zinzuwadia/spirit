"""
Spirit – Windows Voice Assistant
Main entry point.  Launches UI, voice-processing thread, and global hotkey.
"""

import sys
import os
import traceback
import keyboard
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QAction, QFont
from PyQt6.QtCore import Qt, QObject, pyqtSignal

# Prevent crashes when running as a background process (no console)
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    try:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
    except Exception:
        pass


class HotkeyBridge(QObject):
    """Thread-safe bridge between `keyboard` lib and Qt main thread."""
    triggered = pyqtSignal()


def create_tray_icon(app, overlay):
    px = QPixmap(64, 64)
    px.fill(QColor(0, 0, 0, 0))
    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(80, 140, 255))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(4, 4, 56, 56)
    p.setPen(QColor(255, 255, 255))
    font = QFont("Segoe UI", 22, QFont.Weight.Bold)
    p.setFont(font)
    p.drawText(px.rect(), Qt.AlignmentFlag.AlignCenter, "S")
    p.end()

    tray = QSystemTrayIcon(QIcon(px), app)
    menu = QMenu()
    show_action = QAction("Show Spirit", menu)
    show_action.triggered.connect(overlay.show_overlay)
    menu.addAction(show_action)
    quit_action = QAction("Quit", menu)
    quit_action.triggered.connect(app.quit)
    menu.addAction(quit_action)
    tray.setContextMenu(menu)
    tray.setToolTip("Spirit Voice Assistant")
    tray.activated.connect(
        lambda reason: overlay.show_overlay()
        if reason == QSystemTrayIcon.ActivationReason.Trigger
        else None
    )
    tray.show()
    return tray


def main():
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Spirit")
        app.setQuitOnLastWindowClosed(False)

        from gui.overlay import OverlayWindow
        from core.assistant import AssistantThread

        overlay = OverlayWindow()
        assistant = AssistantThread()

        # ── Signal Wiring ─────────────────────────────────────
        # State changes only update the sphere visuals (no show/hide)
        assistant.state_changed.connect(overlay.set_state)
        assistant.response_ready.connect(overlay.set_response)

        # Explicit overlay control from assistant
        assistant.overlay_show.connect(overlay.show_overlay)
        assistant.overlay_hide.connect(overlay.hide_overlay)
        assistant.overlay_pause.connect(overlay.pause_overlay)
        assistant.overlay_resume.connect(overlay.resume_overlay)

        assistant.error_occurred.connect(lambda err: print(f"[Spirit Error] {err}"))

        # ── Global Hotkey: Ctrl+Space ─────────────────────────
        hotkey_bridge = HotkeyBridge()

        def on_hotkey_activated():
            try:
                if not overlay.isVisible():
                    overlay.show_overlay()
                assistant.push_to_talk.emit()
            except Exception as e:
                print(f"[Spirit] Hotkey error: {e}")

        hotkey_bridge.triggered.connect(on_hotkey_activated)

        try:
            keyboard.add_hotkey("ctrl+space", lambda: hotkey_bridge.triggered.emit(), suppress=False)
            print("[Spirit] Hotkey 'Ctrl+Space' registered.")
        except Exception as e:
            print(f"[Spirit] Could not register hotkey (try running as admin): {e}")

        # ── Start ─────────────────────────────────────────────
        assistant.start()
        tray = create_tray_icon(app, overlay)

        def cleanup():
            try:
                keyboard.unhook_all()
            except Exception:
                pass
            assistant.stop()

        app.aboutToQuit.connect(cleanup)

        print("[Spirit] Running — say 'Spirit' or press Ctrl+Space to activate.")
        sys.exit(app.exec())

    except Exception:
        traceback.print_exc()
        print("\n[Spirit] Fatal error — see traceback above.")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
