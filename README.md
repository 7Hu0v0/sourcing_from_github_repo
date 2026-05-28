# 从 GitHub 仓库挖掘候选人

这是一个 Codex skill，用来从指定 GitHub 仓库的贡献者和提交历史里整理候选人信息。

默认输出字段：

`Github ID | Commit | Institution | LinkedIn | personal home page | commit email`

这个 skill 会以目标仓库的 Git 历史为主要依据，提取贡献者姓名、commit 数和该仓库内出现的 commit 邮箱；同时可以辅助补充 GitHub 主页、LinkedIn、个人主页和机构信息。

## 使用方式

先 clone 或更新目标仓库，然后运行：

```bash
python3 scripts/extract_contributors.py /path/to/repo --rev origin/main --format markdown
```

如果需要 CSV：

```bash
python3 scripts/extract_contributors.py /path/to/repo --rev origin/main --format csv
```

## 说明

- `SKILL.md`：Codex skill 的完整工作流和边界说明。
- `scripts/extract_contributors.py`：可复用的贡献者提取脚本。
- `agents/openai.yaml`：skill 元数据。

## 注意

- 不根据姓名、头像、语言或位置推断族裔身份。
- 姓氏筛选只做字符串匹配，不代表身份判断。
- 只整理目标仓库中出现的 commit 邮箱，不跨仓库批量搜集个人邮箱。
