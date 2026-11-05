import logging
import json
import sys
import os
from dataclasses import asdict, is_dataclass

from ..main import RUN_ID, ROOT_DIR
from ..models.outputs import Envelope

OUTPUT_DIR = os.path.join(ROOT_DIR, "output")

logger = logging.getLogger(__name__)

initialized = False
stream = sys.stdout
json_output = None


def init(args):
    global stream, json_output, initialized

    json_output = args.json_output
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if json_output is None or json_output == 'stdout':
        pass
    elif json_output == 'file':
        output_path = os.path.join(OUTPUT_DIR, f"{RUN_ID}.out.jsonl")
        stream = open(output_path, "a", encoding="utf-8")
    else:
        raise ValueError(f"Unknown json output: {json_output}")
    
    initialized = True


def close():
    global stream

    if stream is not None and stream is not sys.stdout:
        try:
            stream.flush()
            stream.close()
        except Exception as e:
            logger.exception("Failed to close output stream")
            raise Exception(f"Failed to close output stream: {e}") from e
        finally:
            stream = None
    else:
        stream = None


def write(data, flush=False):
    """
    Write data to the configured output stream.

    In non-JSON output mode, data is written as-is. For dataclass instances, define
    `__str__` to provide a more suitable human-readable representation.

    In JSON output mode, data is wrapped as `{"type": TYPE, "data": DATA}`. 
    For strings, the type is `"text"`.
    For dataclass instances, the type is the class name and the data is the
    serialized dataclass fields. Other data types are rejected.

    Args:
        data: A string or dataclass instance.
        flush: Whether to forcibly flush the output stream after writing.

    Raises:
        TypeError: If JSON output is enabled and data is neither a string
            nor a dataclass instance.
    """
    out = data

    if json_output:
        if isinstance(data, str):
            envelope = Envelope(data=data, type="text")
        elif is_dataclass(data):
            envelope = Envelope(data=data, type=data.__class__.__name__)
        else:
            raise TypeError(f"Unsupported output data type: {data.__class__.__name__}")
        
        out = json.dumps(asdict(envelope), ensure_ascii=False, separators=(",", ":"),)

    print(out, file=stream, flush=flush)


def emergency(message, flush=False):
    """Write an emergency message to stderr and a fallback output file."""
    if initialized:
        write(message, flush=True)
    else:
        try:
            print(message, file=sys.stderr, flush=True)
        except Exception:
            pass

        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            path = os.path.join(OUTPUT_DIR, f"{RUN_ID}.out.err")

            with open(path, "a", encoding="utf-8") as f:
                print(message, file=f, flush=True)
        except Exception:
            pass