"""Build a deterministic Markdown overview from per-video JSON review results."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DECISION_LABELS = {
    "ready": "可直接发布",
    "post_fix": "后期处理后发布",
    "regenerate_segment": "需要局部重生成",
    "reject": "建议淘汰或整体重做",
    "insufficient_evidence": "证据不足",
}
DECISION_ORDER = {
    "ready": 0,
    "post_fix": 1,
    "regenerate_segment": 2,
    "reject": 3,
    "insufficient_evidence": 4,
}


def load_results(input_dir: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for path in sorted(input_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("item_id", path.stem)
        data.setdefault("source_file", path.name)
        results.append(data)
    if not results:
        raise ValueError(f"No JSON review files found in {input_dir}")
    return results


def normalized_summary(item: dict[str, Any]) -> dict[str, Any]:
    summary = dict(item.get("summary", {}))
    if "release_decision" not in summary:
        legacy = summary.get("verdict")
        summary["release_decision"] = {
            "pass": "ready",
            "conditional_pass": "post_fix",
            "revise": "regenerate_segment",
        }.get(legacy, legacy or "insufficient_evidence")
    if "technical_quality" not in summary:
        summary["technical_quality"] = summary.get("score")
    return summary


def common_issue_categories(results: list[dict[str, Any]]) -> list[tuple[str, int]]:
    counts = Counter(
        issue.get("category", "unknown")
        for item in results
        for issue in item.get("issues", [])
        if issue.get("severity") in {"critical", "major", "minor"}
    )
    return counts.most_common(5)


def render_markdown(results: list[dict[str, Any]], title: str) -> str:
    rows = []
    decision_counts: Counter[str] = Counter()
    for item in results:
        summary = normalized_summary(item)
        decision = summary["release_decision"]
        decision_counts[decision] += 1
        rows.append(
            {
                "id": str(item["item_id"]),
                "source": str(item.get("source_file", "")),
                "decision": decision,
                "quality": summary.get("technical_quality"),
                "fit": summary.get("goal_fit"),
                "priority": str(summary.get("top_priority", "")),
            }
        )

    rows.sort(
        key=lambda row: (
            DECISION_ORDER.get(row["decision"], 9),
            -(row["quality"] if isinstance(row["quality"], (int, float)) else -1),
            row["id"],
        )
    )

    lines = [f"# {title}", "", "## 总览", ""]
    lines.append(f"- 素材总数：{len(rows)}")
    for decision in DECISION_ORDER:
        lines.append(f"- {DECISION_LABELS[decision]}：{decision_counts[decision]}")

    lines.extend(
        [
            "",
            "## 素材结果",
            "",
            "| 排序 | 原文件 | 发布结论 | 技术质量 | 目标适配 | 最高优先级 |",
            "|---:|---|---|---:|---:|---|",
        ]
    )
    for rank, row in enumerate(rows, start=1):
        quality = "—" if row["quality"] is None else str(row["quality"])
        fit = "—" if row["fit"] is None else str(row["fit"])
        lines.append(
            f"| {rank} | {row['source']} | "
            f"{DECISION_LABELS.get(row['decision'], row['decision'])} | "
            f"{quality} | {fit} | {row['priority']} |"
        )

    lines.extend(["", "## 共性问题", ""])
    common = common_issue_categories(results)
    if common:
        lines.extend(f"- `{category}`：{count} 条问题" for category, count in common)
    else:
        lines.append("- 未记录可汇总的问题。")

    lines.extend(["", "## 建议处理顺序", ""])
    repair_rows = [row for row in rows if row["decision"] not in {"ready", "insufficient_evidence"}]
    if repair_rows:
        lines.extend(
            f"{index}. {row['source']}：{row['priority'] or DECISION_LABELS.get(row['decision'], row['decision'])}"
            for index, row in enumerate(repair_rows, start=1)
        )
    else:
        lines.append("全部已检查素材均可直接发布。")

    lines.extend(
        [
            "",
            "> 本表按发布结论优先、技术质量次优排序。候选版本的最终选择还应结合创作目标和返修成本。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path, help="Directory containing per-video JSON reports")
    parser.add_argument("--output", type=Path, required=True, help="Markdown output path")
    parser.add_argument("--title", default="AI 视频批量审片汇总")
    args = parser.parse_args()

    markdown = render_markdown(load_results(args.input_dir), args.title)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
