# 输入输出契约 v1.3

## 输入

最低输入：

- `videos`：一条或多条可读取的视频，或按时间顺序排列且带时间码的关键帧。
- `review_goal`：如发布验收、人物一致性或电影感；缺失时默认做通用发布前质检。

推荐输入：

- `prompt_or_script`：生成提示词、脚本或分镜。
- `reference_assets`：角色、场景、风格参考。
- `target_platform`：用途、画幅和发布标准。
- `known_intentional_changes`：有意的变装、转场、时空切换等。
- `batch_mode`：`single`、`variants` 或 `sequence`；缺失时自动推断。
- `platform`：发布平台；缺失时不套用平台特定规则。
- `priority`：用户最在意的 1–3 项。
- `storyboard_requirements`：必须出现的主体、数量、动作、顺序、空间关系和情绪结果；候选筛选时拆成逐项可验证条件。

用户不需要提交结构化数据。自然语言先按 [极简使用入口](quick-start.md) 归一化为：

```yaml
shot_brief:
  visual_goal: string | null
  must_have: [string]
  priorities: [string]
  intentional_designs: [string]
  parsed_requirements:
    subjects: [string]
    setting: [string]
    quantities: [string]
    ordered_actions: [string]
    spatial_relations: [string]
    emotional_result: string | null
    final_state: string | null
```

只有 `visual_goal` 对分镜验收是必填；普通通用质检允许为 `null`。未提供的选填项使用空列表或 `null`，不得自行编造。

## 输出

```yaml
summary:
  release_decision: ready | post_fix | regenerate_segment | reject | insufficient_evidence
  technical_quality: 0-100 | null
  goal_fit: 0-100 | null
  evidence_confidence: high | medium | low
  top_priority: string
  detected_mode: single | variants | sequence
  detected_content_types: [string]
style_profile:
  intended_style: string | null
  perceived_style: string
  visual_traits: [string]
  style_gap: string | null
  confidence: high | medium | low
director_diagnosis:
  - time_range: string
    audience_impression: string
    observation: string
    professional_dimensions: [movement | shot_size | camera_position | camera_movement | blocking | lighting_color | focus_texture | editing_rhythm | performance | sound]
    professional_diagnosis: string
    mechanism: string
    improvement: string
    confidence: high | medium | low
issues:
  - id: Q-001
    time_range: "00:04.200-00:05.800"
    category: character | motion | scene | cinematography | ai_artifact
    severity: critical | major | minor | note
    confidence: high | medium | low
    observation: string
    impact: string
    evidence: string
    recommendation: string
    remediation_method: edit | post | local_regeneration | full_regeneration | manual_review
    acceptance_checks: [string]
module_scores:
  character: 0-20 | null
  motion: 0-20 | null
  scene: 0-20 | null
  cinematography: 0-20 | null
  ai_artifact: 0-20 | null
strengths:
  - string
assumptions_and_limits:
  - string
next_action: string
```

批量模式在逐条结果之外增加：

```yaml
batch_summary:
  uploaded_files: integer
  unique_items: integer
  duplicate_groups:
    - canonical_item: string
      source_files: [string]
  ready: integer
  post_fix: integer
  regenerate_segment: integer
  reject: integer
  recommended_items: [string]
  common_issues: [string]
  repair_queue: [string]
comparisons:
  - group: string
    preferred: string | null
    alternatives: [string]
    reason: string
cross_shot_issues:
  - from_item: string
    to_item: string
    observation: string
    recommendation: string
```

报告面向人阅读时可用中文标题呈现，但保留这些语义字段。问题按严重程度、时间顺序排序。同一根因造成的连续现象合并为一个时间段，避免逐帧重复。为了兼容旧报告，读取时可以接受 `verdict` 和 `score`，新报告统一写新字段。

`style_profile` 和 `director_diagnosis` 在纯技术检查中可以省略；当用户询问风格、电影感、画面为何显假或不好看时必须输出。没有明确目标风格时，`intended_style` 与 `style_gap` 为 `null`，不得替用户虚构创作意图。
