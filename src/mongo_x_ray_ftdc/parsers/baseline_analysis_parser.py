"""
Copyright (c) 2026 MongoDB Inc.

DISCLAIMER: THESE CODE SAMPLES ARE PROVIDED FOR EDUCATIONAL AND ILLUSTRATIVE PURPOSES ONLY,
TO DEMONSTRATE THE FUNCTIONALITY OF SPECIFIC MONGODB FEATURES.
THEY ARE NOT PRODUCTION-READY AND MAY LACK THE SECURITY HARDENING, ERROR HANDLING, AND TESTING REQUIRED FOR A LIVE ENVIRONMENT.
YOU ARE RESPONSIBLE FOR TESTING, VALIDATING, AND SECURING THIS CODE WITHIN YOUR OWN ENVIRONMENT BEFORE IMPLEMENTATION.
THIS MATERIAL IS PROVIDED "AS IS" WITHOUT WARRANTY OR LIABILITY.

Parser for FTDC baseline analysis results.
"""

import base64
import re
from html import escape
from pathlib import Path
from typing import Any, Optional

import markdown

from mongo_x_ray_ftdc.charts import DEFAULT_CHART_HEIGHT, DEFAULT_CHART_WIDTH
from mongo_x_ray_ftdc.parsers.base_parser import BaseParser


def _chart_img(
    chart_path: str,
    alt: str,
    output_folder: Optional[str] = None,
    width: int = DEFAULT_CHART_WIDTH,
    height: int = DEFAULT_CHART_HEIGHT,
) -> str:
    if chart_path.endswith(".png"):
        src = chart_path
        if output_folder is not None:
            resolved = Path(output_folder) / chart_path
            if resolved.is_file():
                data = resolved.read_bytes()
                b64 = base64.b64encode(data).decode("ascii")
                src = f"data:image/png;base64,{b64}"
        return f'<img src="{src}" width="{width}" height="{height}" alt="{escape(alt)}">'
    return f"![{alt}]({chart_path})"


def _thresholds(item: dict) -> str:
    warning = item.get("warning_threshold")
    critical = item.get("critical_threshold")
    if warning is None and critical is None:
        return "\u2014"
    if critical is None:
        return str(round(warning or 0, 2))
    return f"{round(warning or 0, 2)} / {round(critical or 0, 2)}"


_MD_IMAGE_RE = re.compile(r"^!\[(.*)\]\((.*)\)$", re.DOTALL)


def _html_cell(value: Any) -> str:
    """Render a table cell as HTML: images pass through, other text is escaped."""
    text = str(value)
    if text.startswith("<img"):
        return text
    match = _MD_IMAGE_RE.match(text)
    if match:
        return f'<img src="{escape(match.group(2), quote=True)}" alt="{escape(match.group(1), quote=True)}">'
    return escape(text)


def _comment_html(text: str) -> str:
    """Render the comment text (markdown) to HTML without blank lines.

    Blank lines would end the raw HTML block when the report is rendered, so
    they are removed from the generated markup.
    """
    html = markdown.markdown(text.strip(), extensions=["fenced_code"])
    return "\n".join(line for line in html.splitlines() if line.strip())


class BaselineAnalysisParser(BaseParser):
    """Convert baseline analysis metric summaries to a report table."""

    def format_table(self, item, i) -> str:
        """Format a table; a ``comments`` entry becomes a final merged row.

        Markdown pipe tables cannot merge cells, so a table with comments is
        written as an HTML table whose last row has the label ``Comments`` in
        the first column and the comment text spanning the remaining columns.
        """
        comments = (item.get("comments") or "").strip()
        rows = item.get("rows")
        if not comments:
            return super().format_table(item, i)
        if not rows:
            return super().format_table(item, i) + "\n" + _comment_html(comments) + "\n"

        header = item.get("header", [])
        caption = item.get("caption")
        output = f"#### {caption}\n\n" if caption else ""
        output += '<table style="width:100%">\n<colgroup>\n'
        for h in header:
            width = h.get("width", "") if isinstance(h, dict) else ""
            if width.endswith("px"):
                output += f'<col style="width:{width}" width="{width[:-2]}">\n'
            elif width and width != "*":
                output += f'<col style="width:{width}">\n'
            else:
                output += "<col>\n"
        output += "</colgroup>\n<thead>\n<tr>\n"
        for h in header:
            text = h["text"] if isinstance(h, dict) else h
            output += f'<th style="text-align: center;">{escape(str(text))}</th>\n'
        output += "</tr>\n</thead>\n<tbody>\n"
        for row in rows:
            output += "<tr>\n"
            for cell in row:
                output += f'<td style="text-align: center;">{_html_cell(cell)}</td>\n'
            output += "</tr>\n"
        span = max(len(header) - 1, 1)
        output += (
            "<tr>\n"
            '<td style="text-align: center;"><strong>Comments</strong></td>\n'
            f'<td colspan="{span}" style="text-align: left;">\n{_comment_html(comments)}\n</td>\n'
            "</tr>\n"
        )
        output += "</tbody>\n</table>\n"
        return output

    def parse(self, data: Any, **kwargs) -> list:
        output_folder = kwargs.get("output_folder")
        if kwargs.get("member_state"):
            return [
                {
                    "type": "table",
                    "caption": kwargs.get("caption", "Member State"),
                    "header": [
                        {"text": "Member", "align": "left", "sortable": False, "width": "100px"},
                        {"text": "Me", "sortable": False, "width": "100px"},
                        {"text": "State", "sortable": False, "width": "*"},
                    ],
                    "rows": [
                        [
                            item["member"],
                            item["myself"],
                            _chart_img(
                                item["chart"],
                                f"{item['metric']} {item.get('chart_type', 'bar')} chart",
                                output_folder,
                                item.get("chart_width", DEFAULT_CHART_WIDTH),
                                item.get("chart_height", DEFAULT_CHART_HEIGHT),
                            ),
                        ]
                        for item in data
                    ],
                }
            ]

        show_thresholds = kwargs.get("show_thresholds", True)
        rows = []
        for item in data:
            row = [
                f"{item['metric']} ({item['unit']})",
                f"{round(item['peak'], 2)} / {round(item['average'], 2)}",
            ]
            if show_thresholds:
                row.append(_thresholds(item))
            row.append(
                _chart_img(
                    item["chart"],
                    f"{item['metric']} {item.get('chart_type', 'bar')} chart",
                    output_folder,
                    item.get("chart_width", DEFAULT_CHART_WIDTH),
                    item.get("chart_height", DEFAULT_CHART_HEIGHT),
                )
            )
            rows.append(row)
        header = [
            {"text": "Metric", "sortable": False, "width": "*"},
            {"text": "Peak / Average", "sortable": False, "width": "150px"},
        ]
        if show_thresholds:
            header.append({"text": "Warning / Critical Threshold", "sortable": False, "width": "150px"})
        header.append({"text": "Chart", "sortable": False, "width": "500px"})
        table = {
            "type": "table",
            "caption": kwargs.get("caption", "Baseline Analysis"),
            "header": header,
            "rows": rows,
        }
        comments = (kwargs.get("comments") or "").strip()
        if comments:
            table["comments"] = comments
        return [table]
