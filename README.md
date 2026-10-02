# Writing

个人写作系统：让 AI 辅助写作时，既保留自己的观点和素材，又能稳定地使用自己喜欢的表达方式。

这个仓库不是“让 AI 模仿某篇文章”，而是把写作拆成可复用的几个部分：

- **Skill**：规定 AI 怎么工作（先问什么、不做什么、怎么审稿）
- **风格指南**：可执行地描述你想要的语言特征
- **参考文章库**：提供风格证据，只提炼规律，不复制句子
- **素材与观点**：这篇文章真正要表达的内容，来自你自己
- **草稿与成稿**：从 brief 到发布的工作区

## 目录结构

```text
Writing/
├── README.md                        # 本文件
├── .agents/
│   └── skills/
│       └── personal-writing/        # 核心 skill
│           ├── SKILL.md             # AI 工作流程
│           ├── references/
│           │   ├── style-guide.md   # 我的写作风格（需自己确认后填写）
│           │   ├── favorite-examples.md  # 参考文章索引与风格分析
│           │   └── avoid-list.md    # 禁止/警惕的表达
│           └── templates/
│               └── article-brief.md # 写前 brief 模板
├── corpus/
│   ├── README.md                    # 参考文章库说明
│   └── raw/                         # 原始收藏文章（txt / md）
├── notes/                           # 素材、观察、观点碎片
├── drafts/                          # 正在写的草稿
├── published/                       # 已发布成稿
└── docs/
    └── workflow.md                  # 完整写作流程说明
```

## 快速开始

1. 读 `docs/workflow.md` 了解整体流程。
2. 往 `corpus/raw/` 放 5–10 篇你最认可的文章。
3. 让 AI 分析这些文章，产出 `style-guide.md` 的初稿。
4. **人工确认并修改** `style-guide.md` —— 这一步不能省。
5. 之后用 `/skill:personal-writing` 开始写文章。

## 核心原则

- 内容来自你：经历、观察、观点、事实、判断。
- 表达可以借鉴：节奏、结构、语气、叙述方法、具体程度。
- 不复制原文中的独特句子、段落和比喻。
- 先提炼“风格特征”，再据此写新文章，而不是每次丢原文说“模仿这个”。
