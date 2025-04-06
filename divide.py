import sys
import random
import json


def split_code(file_path=None):
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    num_lines = len(lines)
    dataset = []
    num_samples = min(50, max(20, num_lines // 4))

    for _ in range(num_samples):
        line_idx = random.randint(3, num_lines - 3)
        while not lines[line_idx].strip() or lines[line_idx].startswith(("import", "from")):
            line_idx = random.randint(3, num_lines - 3)

        prefix = "".join(lines[:line_idx])
        middle = lines[line_idx].strip()
        middle_hint = middle[:random.randint(1, 4)]

        extra_lines = random.randint(1, 2)
        middle_extended = "\n".join(lines[line_idx : min(num_lines, line_idx + 1 + extra_lines)]).strip()

        suffix_start = line_idx + 1 + extra_lines
        suffix = "".join(lines[suffix_start : min(num_lines, suffix_start + 3)])

        dataset.append({"prefix": prefix + middle_hint, "middle": middle_extended, "suffix": suffix})

    return dataset


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    dataset = split_code(file_path)
    with open("samples.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
