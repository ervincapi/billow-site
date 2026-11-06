"""Rewrites `@media (prefers-color-scheme: dark)` blocks so a manual choice can override the system setting.

Each dark rule is emitted twice: inside the media query, scoped to `:root:not([data-theme="light"])`,
and outside it, scoped to `:root[data-theme="dark"]`."""
import re

MEDIA = "@media (prefers-color-scheme: dark)"


def _split_rules(block):
    rules, depth, start = [], 0, 0
    for i, ch in enumerate(block):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                rules.append(block[start:i + 1].strip())
                start = i + 1
    return [r for r in rules if r]


def _scope(rule, prefix):
    sel, body = rule.split("{", 1)
    parts = []
    for s in sel.split(","):
        s = s.strip()
        if s == ":root":
            parts.append(prefix)
        elif s.startswith(":root"):
            parts.append(prefix + s[5:])
        else:
            parts.append(prefix + " " + s)
    return ", ".join(parts) + " {" + body


def theme_aware(css):
    out, pos = [], 0
    while True:
        i = css.find(MEDIA, pos)
        if i < 0:
            out.append(css[pos:])
            break
        out.append(css[pos:i])
        j = css.index("{", i)
        depth, k = 0, j
        while True:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        inner = css[j + 1:k]
        rules = _split_rules(inner)
        system = " ".join(_scope(r, ':root:not([data-theme="light"])') for r in rules)
        manual = " ".join(_scope(r, ':root[data-theme="dark"]') for r in rules)
        out.append(MEDIA + " { " + system + " }\n" + manual)
        pos = k + 1
    return "".join(out)


if __name__ == "__main__":
    import sys
    p = sys.argv[1]
    open(p, "w").write(theme_aware(open(p).read()))
