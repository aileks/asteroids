import inspect
import json
import math
import types
from datetime import datetime
from typing import Any

__all__ = ["log_state", "log_event"]

_FPS: int = 60
_MAX_SECONDS: int = 16
_SPRITE_SAMPLE_LIMIT: int = 10  # Maximum number of sprites to log per group

_frame_count: int = 0
_state_log_initialized: bool = False
_event_log_initialized: bool = False
_start_time: datetime = datetime.now()


def log_state() -> None:
    global _frame_count, _state_log_initialized

    # Stop logging after `_MAX_SECONDS` seconds
    if _frame_count > _FPS * _MAX_SECONDS:
        return

    # Take a snapshot approx. once per second
    _frame_count += 1
    if _frame_count % _FPS != 0:
        return

    now: datetime = datetime.now()

    frame: types.FrameType | None = inspect.currentframe()
    if frame is None:
        return

    frame_back: types.FrameType | None = frame.f_back
    if frame_back is None:
        return

    local_vars: dict[str, Any] = frame_back.f_locals.copy()

    screen_size: tuple[int, int] | list[int] = []
    game_state: dict[str, Any] = {}

    for key, value in local_vars.items():
        if "pygame" in str(type(value)) and hasattr(value, "get_size"):
            screen_size = value.get_size()

        if hasattr(value, "__class__") and "Group" in value.__class__.__name__:
            sprites_data: list[dict[str, Any]] = []

            for i, sprite in enumerate(value):
                if i >= _SPRITE_SAMPLE_LIMIT:
                    break

                sprite_info: dict[str, Any] = {"type": sprite.__class__.__name__}

                if hasattr(sprite, "position"):
                    sprite_info["pos"] = [
                        round(sprite.position.x, 2),
                        round(sprite.position.y, 2),
                    ]

                if hasattr(sprite, "velocity"):
                    sprite_info["vel"] = [
                        round(sprite.velocity.x, 2),
                        round(sprite.velocity.y, 2),
                    ]

                if hasattr(sprite, "radius"):
                    sprite_info["rad"] = sprite.radius

                if hasattr(sprite, "rotation"):
                    sprite_info["rot"] = round(sprite.rotation, 2)

                sprites_data.append(sprite_info)

            game_state[key] = {"count": len(value), "sprites": sprites_data}

        if len(game_state) == 0 and hasattr(value, "position"):
            sprite_info: dict[str, Any] = {"type": value.__class__.__name__}

            sprite_info["pos"] = [
                round(value.position.x, 2),
                round(value.position.y, 2),
            ]

            if hasattr(value, "velocity"):
                sprite_info["vel"] = [
                    round(value.velocity.x, 2),
                    round(value.velocity.y, 2),
                ]

            if hasattr(value, "radius"):
                sprite_info["rad"] = value.radius

            if hasattr(value, "rotation"):
                sprite_info["rot"] = round(value.rotation, 2)

            game_state[key] = sprite_info

    entry: dict[str, Any] = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "screen_size": screen_size,
        **game_state,
    }

    # New log file on each run
    mode: str = "w" if not _state_log_initialized else "a"
    with open("game_state.jsonl", mode) as f:
        f.write(json.dumps(entry) + "\n")

    _state_log_initialized = True


def log_event(event_type: str, **details: Any) -> None:
    global _event_log_initialized

    now: datetime = datetime.now()

    event: dict[str, Any] = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "type": event_type,
        **details,
    }

    mode: str = "w" if not _event_log_initialized else "a"
    with open("game_events.jsonl", mode) as f:
        f.write(json.dumps(event) + "\n")

    _event_log_initialized = True
