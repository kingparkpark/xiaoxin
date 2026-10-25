"""Provider-neutral skeleton for the future automated review pipeline."""

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Sequence


@dataclass(frozen=True)
class TimedFrame:
    path: Path
    timestamp_seconds: float


class FrameExtractor(Protocol):
    def extract(self, video: Path) -> Sequence[TimedFrame]: ...


class VisionAnalyzer(Protocol):
    def observe(self, frames: Sequence[TimedFrame], context: dict) -> list[dict]: ...


class RuleEngine(Protocol):
    def evaluate(self, observations: list[dict], context: dict) -> list[dict]: ...


class ReportRenderer(Protocol):
    def render(self, issues: list[dict], context: dict) -> str: ...


def run_review(
    video: Path,
    context: dict,
    extractor: FrameExtractor,
    analyzer: VisionAnalyzer,
    rules: RuleEngine,
    renderer: ReportRenderer,
) -> str:
    """Run extraction, observation, rule evaluation, and report rendering."""
    frames = extractor.extract(video)
    observations = analyzer.observe(frames, context)
    issues = rules.evaluate(observations, context)
    return renderer.render(issues, context)
