# project-path: kanda_reasoner_app/reasoner_engine/ai_bridge_help/prompt_extraction.py
"""Prompt parsing helpers for Project Reasoner AI bridge."""

from __future__ import annotations
import re
from typing import Any
__all__ = ['extract_runtime_anchors_from_detail', 'extract_snippet_text_blob', 'extract_snippet_blocks', 'extract_file_evidence_blocks', 'extract_symbol_evidence_blocks', 'extract_user_question', 'extract_allowed_ids', 'extract_cited_ids', 'extract_allowed_symbols', 'extract_allowed_file_paths', 'extract_path_like_mentions', 'extract_symbol_like_mentions', 'extract_symbol_id_map', 'extract_file_id_map', 'extract_symbol_score_map', 'extract_file_score_map', 'extract_locator_target', 'extract_one_line_triplet']

def extract_runtime_anchors_from_detail(detail_text: str) -> list[str]:
        """Extract the runtime anchors from detail.
        
        Parameters
        ----------
        detail_text : str
            The detail text value.
        
        Returns
        -------
        list[str]
            The list of values.
        """
        
        anchors: list[str] = []

        for line in detail_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("Runtime anchors: "):
                raw = stripped[len("Runtime anchors: "):]
                anchors.extend([part.strip() for part in raw.split("|") if part.strip()])

        return anchors

def extract_snippet_text_blob(prompt: str) -> str:
        """Return concatenated snippet text, including live-source snippets."""
        blocks = extract_snippet_blocks(prompt)
        return "\n".join(str(block.get("text", "")) for block in blocks)

def extract_snippet_blocks(prompt: str) -> list[dict[str, Any]]:
        """Extract SOURCE SNIPPETS and LIVE SOURCE EVIDENCE snippet blocks."""
        blocks: list[dict[str, Any]] = []
        lines = prompt.splitlines()

        in_snippet_section = False
        current: dict[str, Any] | None = None

        section_starters = {
            "SOURCE SNIPPETS",
            "LIVE SOURCE EVIDENCE",
        }
        hard_section_enders = {
            "STRICT GROUNDING RULE",
            "CITATION RULE",
            "PREFERENCE MODE",
            "FINAL TASK REMINDER",
            "INSTRUCTIONS",
        }

        for line in lines:
            stripped = line.strip()

            if stripped in section_starters:
                if current is not None:
                    current["text"] = "\n".join(current["text_lines"]).rstrip()
                    blocks.append(current)
                in_snippet_section = True
                current = None
                continue

            if stripped in hard_section_enders:
                if current is not None:
                    current["text"] = "\n".join(current["text_lines"]).rstrip()
                    blocks.append(current)
                    current = None
                if stripped == "STRICT GROUNDING RULE":
                    break
                in_snippet_section = False
                continue

            if not in_snippet_section:
                continue

            match = re.match(r"^\[(SN\d{2})\]\s+(.+?):(\d+)\s+anchor=(.+)$", stripped)
            if match:
                if current is not None:
                    current["text"] = "\n".join(current["text_lines"]).rstrip()
                    blocks.append(current)

                current = {
                    "snippet_id": match.group(1),
                    "path": match.group(2).strip(),
                    "line": int(match.group(3)),
                    "anchor": match.group(4).strip(),
                    "text_lines": [],
                }
                continue

            if current is None:
                continue

            current["text_lines"].append(line)

        if current is not None:
            current["text"] = "\n".join(current["text_lines"]).rstrip()
            blocks.append(current)

        return blocks

def extract_file_evidence_blocks(prompt: str) -> list[dict[str, Any]]:
        """Extract the file evidence blocks.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        list[dict[str, Any]]
            The list of values.
        """
        
        blocks: list[dict[str, Any]] = []
        lines = prompt.splitlines()

        in_file_section = False
        current: dict[str, Any] | None = None

        for line in lines:
            stripped = line.strip()

            if stripped == "FILE EVIDENCE":
                in_file_section = True
                current = None
                continue

            if stripped == "SYMBOL EVIDENCE":
                if current is not None:
                    current["detail"] = "\n".join(current["detail_lines"]).strip()
                    blocks.append(current)
                break

            if not in_file_section:
                continue

            match = re.match(r"^\[(F\d{2})\]\s+score=(\d+)\s*$", stripped)
            if match:
                if current is not None:
                    current["detail"] = "\n".join(current["detail_lines"]).strip()
                    blocks.append(current)

                current = {
                    "file_id": match.group(1),
                    "score": int(match.group(2)),
                    "path": "",
                    "detail_lines": [],
                }
                continue

            if current is None:
                continue

            if stripped.startswith("Path: "):
                current["path"] = stripped[len("Path: "):].strip()

            current["detail_lines"].append(line)

        return blocks

def extract_symbol_evidence_blocks(prompt: str) -> list[dict[str, Any]]:
        """Extract the symbol evidence blocks.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        list[dict[str, Any]]
            The list of values.
        """
        
        blocks: list[dict[str, Any]] = []
        lines = prompt.splitlines()

        in_symbol_section = False
        current: dict[str, Any] | None = None

        for line in lines:
            stripped = line.strip()

            if stripped == "SYMBOL EVIDENCE":
                in_symbol_section = True
                current = None
                continue

            if stripped in {"SOURCE SNIPPETS", "LIVE SOURCE EVIDENCE"}:
                if current is not None:
                    current["detail"] = "\n".join(current["detail_lines"]).strip()
                    blocks.append(current)
                break

            if not in_symbol_section:
                continue

            match = re.match(r"^\[(S\d{2})\]\s+score=(\d+)\s*$", stripped)
            if match:
                if current is not None:
                    current["detail"] = "\n".join(current["detail_lines"]).strip()
                    blocks.append(current)

                current = {
                    "symbol_id": match.group(1),
                    "score": int(match.group(2)),
                    "symbol_name": "",
                    "path": "",
                    "line": 0,
                    "detail_lines": [],
                }
                continue

            if current is None:
                continue

            if stripped.startswith("Symbol: "):
                current["symbol_name"] = stripped[len("Symbol: "):].strip()

            location_match = re.match(r"^Location:\s+(.+?):(\d+)\s*$", stripped)
            if location_match:
                current["path"] = location_match.group(1).strip()
                current["line"] = int(location_match.group(2))

            current["detail_lines"].append(line)

        return blocks

def extract_user_question(prompt: str) -> str:
        """Extract the user question.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        str
            The string result.
        """
        
        match = re.search(
            r"USER QUESTION\s*\n(.+?)(?:\n\s*\nPROJECT SUMMARY|\n\s*\nCONVERSATION MEMORY|\Z)",
            prompt,
            flags=re.DOTALL,
        )
        if not match:
            return prompt.strip().lower()
        return match.group(1).strip().lower()

def extract_allowed_ids(prompt: str) -> set[str]:
        """Extract the allowed ids.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        set[str]
            The set result.
        """
        
        return set(re.findall(r"\[(?:F|S|SN)\d{2}\]", prompt))

def extract_cited_ids(text: str) -> set[str]:
        """Extract the cited ids.
        
        Parameters
        ----------
        text : str
            The text value.
        
        Returns
        -------
        set[str]
            The set result.
        """
        
        return set(re.findall(r"\[(?:F|S|SN)\d{2}\]", text))

def extract_allowed_symbols(prompt: str) -> set[str]:
        """Extract the allowed symbols.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        set[str]
            The set result.
        """
        
        allowed: set[str] = set()

        symbol_pattern = re.compile(r"^Symbol:\s+(.+?)\s*$", flags=re.MULTILINE)
        for match in symbol_pattern.findall(prompt):
            symbol = match.strip()
            if symbol:
                allowed.add(symbol)

        snippet_anchor_pattern = re.compile(
            r"^\[(SN\d{2})\]\s+.+?:\d+\s+anchor=(.+)$",
            flags=re.MULTILINE,
        )

        for _snippet_id, anchor in snippet_anchor_pattern.findall(prompt):
            anchor = anchor.strip()
            if anchor:
                allowed.add(anchor)
                if anchor.startswith("LIVE_SOURCE:"):
                    allowed.add(anchor[len("LIVE_SOURCE:"):].strip())

            # Also extract dotted names from FILE EVIDENCE detail lines
            # (Functions:, Classes:, Calls out: entries) so the LLM can
            # cite any symbol mentioned in the compact file evidence without rejection.
        file_detail_pattern = re.compile(
            r"^(?:Functions|Classes|Calls out):\s+(.+)$",
            flags=re.MULTILINE,
        )
        for detail_match in file_detail_pattern.findall(prompt):
            for token in re.findall(
                    r"\b[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+\b",
                    detail_match,
            ):
                allowed.add(token)

        return allowed

def extract_allowed_file_paths(prompt: str) -> set[str]:
        """Extract the allowed file paths.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        set[str]
            The set result.
        """
        
        allowed: set[str] = set()
        current_file_id = None

        for line in prompt.splitlines():
            stripped = line.strip()

            file_match = re.match(r"^\[(F\d{2})\]\s+score=", stripped)
            if file_match:
                current_file_id = file_match.group(1)
                continue

            if stripped.startswith("Path: ") and current_file_id is not None:
                allowed.add(stripped[len("Path: "):].strip())
                current_file_id = None
                continue

            location_match = re.match(r"^Location:\s+(.+?):(\d+)\s*$", stripped)
            if location_match:
                allowed.add(location_match.group(1).strip())
                continue

            snippet_match = re.match(r"^\[(SN\d{2})\]\s+(.+?):(\d+)\s+anchor=(.+)$", stripped)
            if snippet_match:
                allowed.add(snippet_match.group(2).strip())
                continue

        return allowed

def extract_path_like_mentions(text: str) -> set[str]:
        """Extract slash or backslash path-like mentions from answer text."""
        return set(
            re.findall(
                r"\b[A-Za-z0-9_\-\\/]+(?:[\\/][A-Za-z0-9_\-\.]+)+\b",
                text,
            )
        )

def extract_symbol_like_mentions(text: str) -> set[str]:
        """Extract the symbol like mentions.
        
        Parameters
        ----------
        text : str
            The text value.
        
        Returns
        -------
        set[str]
            The set result.
        """
        
        candidates = set(
            re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+\b", text)
        )

        excluded_prefixes = {
            "f01",
            "f02",
            "f03",
            "f04",
            "f05",
            "f06",
            "f07",
            "f08",
            "f09",
            "f10",
            "f11",
            "f12",
            "f13",
            "f14",
            "s01",
            "s02",
            "s03",
            "s04",
            "s05",
            "s06",
            "s07",
            "s08",
            "s09",
            "s10",
            "s11",
            "s12",
            "s13",
            "s14",
            "sn01",
            "sn02",
            "sn03",
            "sn04",
            "sn05",
            "sn06",
            "sn07",
            "sn08",
            "sn09",
            "sn10",
        }

        filtered: set[str] = set()
        for candidate in candidates:
            low = candidate.lower()
            if low.split(".")[0] in excluded_prefixes:
                continue
            filtered.add(candidate)

        return filtered

def extract_symbol_id_map(prompt: str) -> dict[str, str]:
        """Extract the symbol id map.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        dict[str, str]
            The mapped values.
        """
        
        out: dict[str, str] = {}
        current_symbol_id = None

        for line in prompt.splitlines():
            stripped = line.strip()

            m_score = re.match(r"^\[(S\d{2})\]\s+score=(\d+)\s*$", stripped)
            if m_score:
                current_symbol_id = m_score.group(1)
                continue

            m_symbol = re.match(r"^Symbol:\s+(.+?)\s*$", stripped)
            if m_symbol and current_symbol_id is not None:
                out[m_symbol.group(1).strip()] = current_symbol_id
                current_symbol_id = None

        return out

def extract_file_id_map(prompt: str) -> dict[str, str]:
        """Extract the file id map.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        dict[str, str]
            The mapped values.
        """
        
        out: dict[str, str] = {}
        current_file_id = None

        for line in prompt.splitlines():
            stripped = line.strip()

            m_score = re.match(r"^\[(F\d{2})\]\s+score=(\d+)\s*$", stripped)
            if m_score:
                current_file_id = m_score.group(1)
                continue

            m_path = re.match(r"^Path:\s+(.+?)\s*$", stripped)
            if m_path and current_file_id is not None:
                out[m_path.group(1).strip()] = current_file_id
                current_file_id = None

        return out

def extract_symbol_score_map(prompt: str) -> list[tuple[str, str, str, int]]:
        """Extract the symbol score map.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        list[tuple[str, str, str, int]]
            The list of values.
        """
        
        items: list[tuple[str, str, str, int]] = []

        current_symbol_id = None
        current_score = None
        current_symbol_name = None

        for line in prompt.splitlines():
            stripped = line.strip()

            m_score = re.match(r"^\[(S\d{2})\]\s+score=(\d+)\s*$", stripped)
            if m_score:
                current_symbol_id = m_score.group(1)
                current_score = int(m_score.group(2))
                current_symbol_name = None
                continue

            m_symbol = re.match(r"^Symbol:\s+(.+?)\s*$", stripped)
            if m_symbol and current_symbol_id is not None:
                current_symbol_name = m_symbol.group(1).strip()
                continue

            m_location = re.match(r"^Location:\s+(.+?):(\d+)\s*$", stripped)
            if (
                m_location
                and current_symbol_id is not None
                and current_score is not None
                and current_symbol_name is not None
            ):
                symbol_path = m_location.group(1).strip()
                items.append(
                    (current_symbol_id, current_symbol_name, symbol_path, current_score)
                )
                current_symbol_id = None
                current_score = None
                current_symbol_name = None

        return items

def extract_file_score_map(prompt: str) -> list[tuple[str, str, int]]:
        """Extract the file score map.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        list[tuple[str, str, int]]
            The list of values.
        """
        
        items: list[tuple[str, str, int]] = []
        current_file_id = None
        current_score = None

        for line in prompt.splitlines():
            stripped = line.strip()

            m_score = re.match(r"^\[(F\d{2})\]\s+score=(\d+)\s*$", stripped)
            if m_score:
                current_file_id = m_score.group(1)
                current_score = int(m_score.group(2))
                continue

            m_path = re.match(r"^Path:\s+(.+?)\s*$", stripped)
            if m_path and current_file_id is not None and current_score is not None:
                items.append((current_file_id, m_path.group(1).strip(), current_score))
                current_file_id = None
                current_score = None

        return items

def extract_locator_target(question: str) -> str:
        """Extract the locator target.
        
        Parameters
        ----------
        question : str
            The question value.
        
        Returns
        -------
        str
            The string result.
        """
        
        q = question.strip().lower()

        prefixes = [
            "which file contains",
            "what file contains",
            "which file records",
            "what file records",
            "which file has",
            "what file has",
            "which file includes",
            "what file includes",
            "which file is the source of",
            "what file is the source of",
            "which file defines",
            "what file defines",
            "in which file is",
            "where is",
            "where is the",
            "where is this",
            "which symbol owns",
            "what symbol owns",
            "which symbol handles",
            "what symbol handles",
            "which method owns",
            "what method owns",
            "which function owns",
            "what function owns",
            "which symbol directly calls",
        ]

        for prefix in prefixes:
            if q.startswith(prefix):
                target = q[len(prefix):].strip()
                target = target.rstrip(" ?.")
                if target.startswith("the "):
                    target = target[4:]
                return target

        return ""

def extract_one_line_triplet(text: str) -> str:
        """Extract the one line triplet.
        
        Parameters
        ----------
        text : str
            The text value.
        
        Returns
        -------
        str
            The string result.
        """
        
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.count("|") == 2:
                return stripped
        return text.strip()



