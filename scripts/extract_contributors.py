#!/usr/bin/env python3
"""Extract contributor sourcing rows from a local git repository.

This script intentionally reads only the target repository's git history. It
does not search other repositories for personal emails.
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_SURNAMES = {
    "zhao", "qian", "sun", "li", "zhou", "wu", "zheng", "wang", "feng",
    "chen", "zhu", "wei", "shen", "han", "qin", "you", "xu", "he", "lv",
    "shi", "zhang", "kong", "cao", "yan", "hua", "jin", "tao", "jiang",
    "xie", "zou", "yu", "bo", "shui", "dou", "yun", "su", "pan", "ge",
    "fan", "peng", "lang", "lu", "chang", "ma", "miao", "fang", "ren",
    "yuan", "liu", "bao", "tang", "fei", "lian", "xue", "lei", "ni",
    "teng", "yin", "luo", "bi", "hao", "an", "ying", "le", "fu", "pi",
    "qi", "kang", "bu", "gu", "meng", "ping", "huang", "mu", "xiao",
    "yao", "shao", "mao", "di", "mi", "bei", "ming", "zang", "ji",
    "cheng", "dai", "song", "shu", "qu", "dong", "liang", "du", "lan",
    "min", "jia", "lou", "tong", "guo", "lin", "diao", "zhong",
    "zhongli", "qiu", "gao", "xia", "cai", "tian", "hu", "huo", "ling",
    "wan", "zhi", "ke", "kuan", "mo", "zong", "ding", "deng", "shan",
    "hang", "zuo", "cui", "niu", "weng", "xun", "yang", "hui", "gong",
    "pei", "rong", "jiao", "che", "hou", "quan", "ban", "ning", "chou",
    "luan", "zu", "long", "ye", "si", "bai", "huai", "cong", "lai",
    "zhuo", "qiao", "shuang", "dang", "tan", "ran", "bian", "chai",
    "liao", "jian", "sha", "hai", "wen", "zhai", "kou", "rao", "pu",
    "ou", "she", "nian", "ai", "ha", "zhan", "ruan", "bing", "tu",
    "zhuang", "geng", "guang", "chao", "ouyang", "shangguan", "duanmu",
    "kuang", "shang", "pang", "nie", "gou", "ju",
}


@dataclass(frozen=True)
class Contributor:
    commits: int
    name: str
    email: str

    @property
    def github_id_guess(self) -> str:
        return self.email.split("@", 1)[0]

    @property
    def institution_guess(self) -> str:
        domain = self.email.split("@", 1)[-1].lower()
        if domain == "google.com":
            return "Google (commit email)"
        if domain == "nvidia.com":
            return "NVIDIA (commit email)"
        if domain == "gmail.com":
            return "Gmail / unknown"
        return domain or "-"


def run_git(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def parse_shortlog(output: str) -> list[Contributor]:
    rows: list[Contributor] = []
    pattern = re.compile(r"^\s*(\d+)\s+(.+?)\s+<([^>]+)>$")
    for line in output.splitlines():
        match = pattern.match(line)
        if not match:
            continue
        rows.append(
            Contributor(
                commits=int(match.group(1)),
                name=match.group(2),
                email=match.group(3),
            )
        )
    return rows


def load_surnames(path: Path | None) -> set[str]:
    if not path:
        return set(DEFAULT_SURNAMES)
    text = path.read_text(encoding="utf-8")
    return {token.lower() for token in re.findall(r"[A-Za-z]+", text)}


def matches_surname(name: str, surnames: set[str]) -> bool:
    tokens = [token.lower() for token in re.findall(r"[A-Za-z]+", name)]
    return any(token in surnames for token in tokens)


def markdown(rows: list[Contributor]) -> str:
    lines = [
        "| Github ID | Commit | Institution | LinkedIn | personal home page | commit email |",
        "|---|---:|---|---|---|---|",
    ]
    for row in rows:
        github_id = row.github_id_guess
        lines.append(
            f"| [{github_id}](https://github.com/{github_id}) | {row.commits} | "
            f"{row.institution_guess} | - | - | {row.email} |"
        )
    return "\n".join(lines)


def write_csv(rows: list[Contributor]) -> None:
    writer = csv.writer(sys.stdout)
    writer.writerow(
        ["Github ID", "Commit", "Institution", "LinkedIn", "personal home page", "commit email"]
    )
    for row in rows:
        writer.writerow([row.github_id_guess, row.commits, row.institution_guess, "", "", row.email])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", type=Path)
    parser.add_argument("--rev", default="HEAD")
    parser.add_argument("--surname-filter", type=Path)
    parser.add_argument("--format", choices=["markdown", "csv"], default="markdown")
    args = parser.parse_args()

    shortlog = run_git(args.repo, ["shortlog", "-sne", args.rev])
    rows = parse_shortlog(shortlog)
    surnames = load_surnames(args.surname_filter)
    rows = [row for row in rows if matches_surname(row.name, surnames)]

    if args.format == "csv":
        write_csv(rows)
    else:
        print(markdown(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
