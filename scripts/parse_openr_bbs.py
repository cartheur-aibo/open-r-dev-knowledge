#!/usr/bin/env python3

from __future__ import annotations

import csv
import html
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SRC_FILES = [
    ROOT / "src" / "Msgs_1_to_726.html",
    ROOT / "src" / "Msgs_727_to_1955.html",
]
DATA_DIR = ROOT / "data"
CONTEXT_DIR = ROOT / "context"

ROW_RE = re.compile(r"<tr><td[^>]*>(.*?)</td></tr>", re.S)
ID_RE = re.compile(r'<a name="(?P<id>\d+)">(?P=id)</a>')
LINK_TEXT_RE = re.compile(r"<a [^>]*>(.*?)</a>", re.S)
TAG_RE = re.compile(r"<[^>]+>")
BR_RE = re.compile(r"<br\s*/?>", re.I)
WS_RE = re.compile(r"[ \t\r\f\v]+")
RE_PREFIX_RE = re.compile(r"^(?:(?:re|fw|fwd)\s*:\s*)+", re.I)
MODEL_PATTERNS = {
    "ERS-7M3": re.compile(r"\bers[- ]?7m3\b", re.I),
    "ERS-7": re.compile(r"\bers[- ]?7\b", re.I),
    "ERS-220": re.compile(r"\bers[- ]?220\b", re.I),
    "ERS-210A": re.compile(r"\bers[- ]?210a\b", re.I),
    "ERS-210": re.compile(r"\bers[- ]?210\b", re.I),
}
TOPIC_RULES = {
    "boot_setup": [
        re.compile(r"\bmemory stick\b", re.I),
        re.compile(r"\bboot(?:ing|ed)?\b", re.I),
        re.compile(r"\bflash updater\b", re.I),
        re.compile(r"\bflash rom\b", re.I),
        re.compile(r"\bfirmware\b", re.I),
        re.compile(r"\bwconsole\b", re.I),
        re.compile(r"\bclinic mode\b", re.I),
        re.compile(r"\bshutdown\b", re.I),
        re.compile(r"\bsupercore\b", re.I),
    ],
    "build_toolchain": [
        re.compile(r"\bcompil(?:e|er|ing|ation)\b", re.I),
        re.compile(r"\bmake(?:file)?\b", re.I),
        re.compile(r"\bstubgen2?\b", re.I),
        re.compile(r"\bstub\.cfg\b", re.I),
        re.compile(r"\bmkbin\b", re.I),
        re.compile(r"\bgzcp\b", re.I),
        re.compile(r"\bmipsel\b", re.I),
        re.compile(r"\bgcc\b", re.I),
        re.compile(r"\bheader files?\b", re.I),
        re.compile(r"\bremote processing\b", re.I),
        re.compile(r"\bpermissions?\b", re.I),
    ],
    "networking": [
        re.compile(r"\bwlan\b", re.I),
        re.compile(r"\bwireless\b", re.I),
        re.compile(r"\btcp(?:/ip)?\b", re.I),
        re.compile(r"\budp\b", re.I),
        re.compile(r"\bdhcp\b", re.I),
        re.compile(r"\bipstack\b", re.I),
        re.compile(r"\btelnet\b", re.I),
        re.compile(r"\bping\b", re.I),
        re.compile(r"\baccess ?point\b", re.I),
        re.compile(r"\bwlanconf(?:\.txt)?\b", re.I),
        re.compile(r"\bether_ip\b", re.I),
        re.compile(r"\bwep(?:enable|key)?\b", re.I),
    ],
    "motion": [
        re.compile(r"\bjoints?\b", re.I),
        re.compile(r"\bmotion\b", re.I),
        re.compile(r"\bwalk(?:ing)?\b", re.I),
        re.compile(r"\bturn\b", re.I),
        re.compile(r"\bisready\b", re.I),
        re.compile(r"\bframes?\b", re.I),
        re.compile(r"\bmotor\b", re.I),
        re.compile(r"\bmouth\b", re.I),
        re.compile(r"\bhead\b", re.I),
        re.compile(r"\bcommand vector\b", re.I),
    ],
    "vision": [
        re.compile(r"\bcamera\b", re.I),
        re.compile(r"\bvision\b", re.I),
        re.compile(r"\byuv\b", re.I),
        re.compile(r"\bycbcr\b", re.I),
        re.compile(r"\bcmvision\b", re.I),
        re.compile(r"\bpictures?\b", re.I),
        re.compile(r"\bimages?\b", re.I),
        re.compile(r"\bball\b", re.I),
        re.compile(r"\bcolo[u]?r calibration\b", re.I),
        re.compile(r"\bcolo[u]?r\b", re.I),
    ],
    "debugging": [
        re.compile(r"\berror\b", re.I),
        re.compile(r"\bexception\b", re.I),
        re.compile(r"\bdebug\b", re.I),
        re.compile(r"\bemon\.log\b", re.I),
        re.compile(r"\btimeout\b", re.I),
        re.compile(r"\bselector\b", re.I),
        re.compile(r"\bqueue\b", re.I),
        re.compile(r"\boverflow\b", re.I),
        re.compile(r"\bnot found\b", re.I),
        re.compile(r"\bsendready\b", re.I),
        re.compile(r"\bunimailer\b", re.I),
        re.compile(r"\btlb\b", re.I),
    ],
    "rcode": [
        re.compile(r"\br-?code\b", re.I),
        re.compile(r"\bdistance sensor\b", re.I),
        re.compile(r"\bdistance variable\b", re.I),
    ],
    "aperios": [
        re.compile(r"\baperios\b", re.I),
        re.compile(r"\bmcoop\b", re.I),
        re.compile(r"\bintradeliver\b", re.I),
        re.compile(r"\bselector out of range\b", re.I),
    ],
}
ERROR_PATTERNS = {
    "sTIMEOUT_error_28": re.compile(r"\berror\s+28\b|\bstimeout\b", re.I),
    "selector_out_of_range": re.compile(r"selector (?:is )?out of range", re.I),
    "service_not_found": re.compile(r"\b[A-Za-z0-9_.-]+(?:\.[A-Za-z0-9_.-]+)*\s+NOT FOUND\b"),
    "queue_overflow": re.compile(r"exceed max size of queue|maxqueuesize", re.I),
    "udp_connection_busy": re.compile(r"udp_connection_busy", re.I),
    "tlb_exception": re.compile(r"\btlb exception\b", re.I),
    "command_not_found": re.compile(r"command not found", re.I),
    "sendready_failed": re.compile(r"sendready\(\).*failed|sending ready failed", re.I),
}


@dataclass
class Message:
    id: int
    title: str
    normalized_title: str
    author: str
    date: str
    iso_date: str
    file: str
    depth: int
    is_reply: bool
    parent_id: int | None
    thread_root_id: int
    models: list[str]
    topics: list[str]
    error_signatures: list[str]
    body: str


def clean_html_fragment(fragment: str) -> str:
    clean = BR_RE.sub("\n", fragment)
    clean = html.unescape(clean.replace("&nbsp;", " "))
    clean = TAG_RE.sub("", clean)
    clean = "\n".join(WS_RE.sub(" ", line).strip() for line in clean.splitlines())
    return "\n".join(line for line in clean.splitlines() if line)


def normalize_title(title: str) -> str:
    title = RE_PREFIX_RE.sub("", title).strip()
    title = WS_RE.sub(" ", title)
    return title


def parse_date(raw: str) -> str:
    return datetime.strptime(raw, "%Y/%m/%d-%H:%M").isoformat()


def infer_depth(row: str) -> int:
    prefix = row.split('<a name="', 1)[0]
    depth = prefix.count("|") + prefix.count("+-")
    return depth


def extract_models(text: str) -> list[str]:
    found = [name for name, pattern in MODEL_PATTERNS.items() if pattern.search(text)]
    return sorted(found)


def extract_topics(text: str) -> list[str]:
    topics = []
    for topic, patterns in TOPIC_RULES.items():
        if any(pattern.search(text) for pattern in patterns):
            topics.append(topic)
    return sorted(topics)


def extract_errors(text: str) -> list[str]:
    return sorted(name for name, pattern in ERROR_PATTERNS.items() if pattern.search(text))


def parse_messages(paths: Iterable[Path]) -> list[Message]:
    parsed: list[Message] = []
    previous_by_title: dict[str, list[tuple[int, int, int]]] = defaultdict(list)

    for path in paths:
        rows = ROW_RE.findall(path.read_text(encoding="latin-1"))
        idx = 0
        while idx < len(rows) - 2:
            header = rows[idx]
            id_match = ID_RE.search(header)
            if not id_match:
                idx += 1
                continue

            message_id = int(id_match.group("id"))
            title_links = LINK_TEXT_RE.findall(header)
            title = clean_html_fragment(title_links[-1]) if title_links else ""
            after_last_link = header.split("</a>")[-1]
            author_match = re.search(r"\s*([^<]+?)\s*<small>\[(.*?)\]</small>", after_last_link, re.S)
            author, raw_date = ("", "")
            if author_match:
                author = author_match.group(1).strip()
                raw_date = author_match.group(2).strip()

            body = clean_html_fragment(rows[idx + 2])
            depth = infer_depth(header)
            normalized = normalize_title(title)
            is_reply = normalized != title
            parent_id = None
            thread_root_id = message_id

            history = previous_by_title[normalized]
            if history:
                thread_root_id = history[0][0]
                candidates = [item for item in reversed(history) if item[1] < depth]
                if candidates:
                    parent_id = candidates[0][0]
                else:
                    parent_id = history[-1][0]

            full_text = f"{title}\n{body}"
            message = Message(
                id=message_id,
                title=title,
                normalized_title=normalized,
                author=author,
                date=raw_date,
                iso_date=parse_date(raw_date),
                file=path.name,
                depth=depth,
                is_reply=is_reply,
                parent_id=parent_id,
                thread_root_id=thread_root_id,
                models=extract_models(full_text),
                topics=extract_topics(full_text),
                error_signatures=extract_errors(full_text),
                body=body,
            )
            parsed.append(message)
            history.append((message_id, depth, len(parsed) - 1))
            idx += 3

    return parsed


def write_json(messages: list[Message]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    all_path = DATA_DIR / "openr_bbs_messages.json"
    jsonl_path = DATA_DIR / "openr_bbs_messages.jsonl"
    records = [asdict(msg) for msg in sorted(messages, key=lambda m: m.id)]
    all_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_csv(messages: list[Message]) -> None:
    path = DATA_DIR / "openr_bbs_messages.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "id",
                "title",
                "normalized_title",
                "author",
                "date",
                "iso_date",
                "file",
                "depth",
                "is_reply",
                "parent_id",
                "thread_root_id",
                "models",
                "topics",
                "error_signatures",
                "body",
            ]
        )
        for msg in sorted(messages, key=lambda m: m.id):
            writer.writerow(
                [
                    msg.id,
                    msg.title,
                    msg.normalized_title,
                    msg.author,
                    msg.date,
                    msg.iso_date,
                    msg.file,
                    msg.depth,
                    str(msg.is_reply).lower(),
                    msg.parent_id or "",
                    msg.thread_root_id,
                    "|".join(msg.models),
                    "|".join(msg.topics),
                    "|".join(msg.error_signatures),
                    msg.body,
                ]
            )


def top_examples(messages: list[Message], predicate, limit: int = 8) -> list[Message]:
    return sorted([msg for msg in messages if predicate(msg)], key=lambda m: m.id)[:limit]


def write_manifest(messages: list[Message]) -> None:
    topic_counts = Counter(topic for msg in messages for topic in msg.topics)
    model_counts = Counter(model for msg in messages for model in msg.models)
    error_counts = Counter(err for msg in messages for err in msg.error_signatures)
    thread_roots = {msg.thread_root_id for msg in messages}

    manifest = {
        "source_files": [str(path.relative_to(ROOT)) for path in SRC_FILES],
        "message_count": len(messages),
        "thread_count": len(thread_roots),
        "date_range": {
            "start": min(msg.date for msg in messages),
            "end": max(msg.date for msg in messages),
        },
        "topic_counts": dict(sorted(topic_counts.items())),
        "model_counts": dict(sorted(model_counts.items())),
        "error_signature_counts": dict(sorted(error_counts.items())),
    }
    (DATA_DIR / "openr_bbs_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def write_threads(messages: list[Message]) -> None:
    by_root: dict[int, list[Message]] = defaultdict(list)
    for msg in messages:
        by_root[msg.thread_root_id].append(msg)

    threads = []
    for root_id, members in sorted(by_root.items()):
        members = sorted(members, key=lambda msg: msg.id)
        root = next(msg for msg in members if msg.id == root_id)
        threads.append(
            {
                "thread_root_id": root_id,
                "thread_title": root.normalized_title,
                "message_ids": [msg.id for msg in members],
                "message_count": len(members),
                "authors": sorted({msg.author for msg in members if msg.author}),
                "models": sorted({model for msg in members for model in msg.models}),
                "topics": sorted({topic for msg in members for topic in msg.topics}),
                "error_signatures": sorted({err for msg in members for err in msg.error_signatures}),
                "date_start": members[0].date,
                "date_end": members[-1].date,
            }
        )

    (DATA_DIR / "openr_bbs_threads.json").write_text(json.dumps(threads, indent=2), encoding="utf-8")


def write_topic_index(messages: list[Message]) -> None:
    counts = Counter(topic for msg in messages for topic in msg.topics)
    lines = [
        "# OPEN-R BBS Topic Index",
        "",
        "Retrieval-oriented topic index generated from the two archived Sony BBS exports.",
        "",
    ]
    for topic, count in sorted(counts.items()):
        lines.append(f"## {topic}")
        lines.append("")
        lines.append(f"- Messages tagged: {count}")
        examples = top_examples(messages, lambda msg, topic=topic: topic in msg.topics)
        for msg in examples:
            lines.append(f"- Msg {msg.id}: {msg.title}")
        lines.append("")
    (CONTEXT_DIR / "openr_bbs_topic_index.md").write_text("\n".join(lines), encoding="utf-8")


def write_model_index(messages: list[Message]) -> None:
    counts = Counter(model for msg in messages for model in msg.models)
    lines = [
        "# OPEN-R BBS Model Index",
        "",
        "Model-centric pointers for troubleshooting compatibility, firmware, WLAN, and R-CODE behavior.",
        "",
    ]
    for model, count in sorted(counts.items()):
        lines.append(f"## {model}")
        lines.append("")
        lines.append(f"- Messages tagged: {count}")
        examples = top_examples(messages, lambda msg, model=model: model in msg.models)
        for msg in examples:
            lines.append(f"- Msg {msg.id}: {msg.title}")
        lines.append("")
    (CONTEXT_DIR / "openr_bbs_model_index.md").write_text("\n".join(lines), encoding="utf-8")


def write_error_index(messages: list[Message]) -> None:
    counts = Counter(err for msg in messages for err in msg.error_signatures)
    explanations = {
        "command_not_found": "Missing or non-executable SDK tools such as the cross compiler or stub generator.",
        "queue_overflow": "Producer/consumer imbalance, observer readiness issues, or message floods.",
        "sTIMEOUT_error_28": "Lifecycle callback did not return, or another operation timed out.",
        "selector_out_of_range": "Bad selector wiring, incomplete registration, or entry mismatch.",
        "sendready_failed": "Observer/send readiness path is broken or overloaded.",
        "service_not_found": "Object or service registration mismatch, often in generated glue or config.",
        "tlb_exception": "Likely memory corruption or invalid access in user code.",
        "udp_connection_busy": "UDP send path still busy when another packet is submitted.",
    }
    lines = [
        "# OPEN-R BBS Error Signature Index",
        "",
        "Fast lookup for common runtime and build signatures discussed in the archive.",
        "",
    ]
    for signature, count in sorted(counts.items()):
        lines.append(f"## {signature}")
        lines.append("")
        lines.append(f"- Messages tagged: {count}")
        lines.append(f"- Typical meaning: {explanations.get(signature, 'See source messages for details.')}")
        examples = top_examples(messages, lambda msg, signature=signature: signature in msg.error_signatures)
        for msg in examples:
            lines.append(f"- Msg {msg.id}: {msg.title}")
        lines.append("")
    (CONTEXT_DIR / "openr_bbs_error_index.md").write_text("\n".join(lines), encoding="utf-8")


def write_rules(messages: list[Message]) -> None:
    rules = [
        {
            "name": "SDK stick fails to boot",
            "if_seen": "AIBO powers off, hangs, or seems dead when booting an SDK Memory Stick.",
            "check": [
                "Verify flash ROM / firmware level.",
                "Verify the Memory Stick has the full expected file layout.",
                "Check whether the base image is WCONSOLE instead of WLAN or BASIC.",
                "Check battery level and try a known-good stick.",
                "Suspect hardware only after the above pass.",
            ],
            "messages": [714, 716, 722],
        },
        {
            "name": "Service or subject NOT FOUND",
            "if_seen": "Runtime reports `... NOT FOUND` while connecting objects or services.",
            "check": [
                "Inspect `OBJECTS.CFG` and `CONNECT.CFG`.",
                "Confirm generated stubs and names match exactly.",
                "Verify `REGISTER_ALL_ENTRY` runs in `DoInit()`.",
            ],
            "messages": [683, 686, 690],
        },
        {
            "name": "selector out of range",
            "if_seen": "Aperios reports `selector out of range` or `intraDeliver selector is out of range`.",
            "check": [
                "Inspect selector counts and generated entries.",
                "Check `stub.cfg` and object registration.",
                "Treat it as wiring/glue failure before suspecting application logic.",
            ],
            "messages": [336],
        },
        {
            "name": "sTIMEOUT / error 28",
            "if_seen": "Logs mention `error 28` or `sTIMEOUT` during object lifecycle.",
            "check": [
                "Check whether `DoStart()` or `DoStop()` blocks or never returns.",
                "Move long-running work out of lifecycle callbacks.",
            ],
            "messages": [671, 704],
        },
        {
            "name": "All joints move wildly when commanding one joint",
            "if_seen": "Setting one joint causes unrelated joints to move to extreme positions.",
            "check": [
                "Verify the joint command vector length.",
                "If the vector declares all joints, populate all joint values before sending it.",
            ],
            "messages": [719, 723],
        },
        {
            "name": "WLAN config accepted in peer-to-peer but hangs via access point",
            "if_seen": "AIBO boots in ad-hoc mode but hangs or fails with AP mode.",
            "check": [
                "Inspect `WLANCONF.TXT` formatting carefully.",
                "Do not include spaces around `KEY=VALUE` assignments.",
            ],
            "messages": [543, 552],
        },
        {
            "name": "Current OPEN-R stack needs static IP",
            "if_seen": "User wants DHCP or dynamic assignment on older OPEN-R LAN support.",
            "check": [
                "Assume a known static IP is required unless using a different software stack.",
                "Do not infer DHCP support from newer commercial AIBO products.",
            ],
            "messages": [693, 700, 701],
        },
        {
            "name": "UDP send path stalls or reports busy",
            "if_seen": "First UDP packet never completes or next packet reports `UDP_CONNECTION_BUSY`.",
            "check": [
                "Treat send as asynchronous and verify completion before the next packet.",
                "Check callback flow and pacing.",
            ],
            "messages": [402],
        },
        {
            "name": "Image transfer or large payload misbehaves",
            "if_seen": "Passing camera/image arrays between objects leads to failures or unexpected copies.",
            "check": [
                "Remember `SetData(ptr, size)` copies to shared memory.",
                "Check `OStatus` return codes.",
                "Use explicit shared-memory handling if zero-copy semantics are required.",
            ],
            "messages": [696, 697],
        },
        {
            "name": "R-CODE feature seems missing on ERS-7M3",
            "if_seen": "R-CODE WLAN or support assumptions fail on ERS-7M3.",
            "check": [
                "Verify the exact R-CODE version and model support window.",
                "Older R-CODE Ver2 did not support ERS-7M3 WLAN at first.",
            ],
            "messages": [1944, 1945, 1954, 1955],
        },
    ]
    (DATA_DIR / "openr_bbs_rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")

    lines = [
        "# OPEN-R Troubleshooting Rules",
        "",
        "Compact rules for retrieval and expert-system prompting. Each rule is backed by specific BBS message IDs.",
        "",
    ]
    for rule in rules:
        lines.append(f"## {rule['name']}")
        lines.append("")
        lines.append(f"- Symptom: {rule['if_seen']}")
        lines.append("- Checks:")
        for item in rule["check"]:
            lines.append(f"  - {item}")
        lines.append("- Source messages: " + ", ".join(f"Msg {msg_id}" for msg_id in rule["messages"]))
        lines.append("")
    (CONTEXT_DIR / "openr_bbs_troubleshooting_rules.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    CONTEXT_DIR.mkdir(exist_ok=True)
    messages = parse_messages(SRC_FILES)
    write_json(messages)
    write_csv(messages)
    write_manifest(messages)
    write_threads(messages)
    write_topic_index(messages)
    write_model_index(messages)
    write_error_index(messages)
    write_rules(messages)
    print(f"Generated corpus for {len(messages)} messages.")


if __name__ == "__main__":
    main()
