# Horizon art masters

Editable sources for Horizon's original 16x16 textures. `scripts/gen_assets.py` renders every `*.txt` here into
`kubejs/assets/horizon/textures/...` (deterministically, no third-party art). Each file is:

    @ target: item|block
    <char> <rrggbb>[aa]        palette lines (char `.` is always transparent)
    ---
    16 rows of 16 characters

Shared palette (Horizon art direction, docs/ART_DIRECTION.md): timber `5a3b22/7a5230/9c6b3e`, stone `5b5763/8a8592`,
weathered copper `8c4a2f/b86b3e/d9925a`, verdigris `3f8f80/5fb8a4`, brass `a9822f/d9b24a/f2d27a`,
survey turquoise `2aa9a0/6ee6d8`, parchment `d9c79e/efe2c0`, ink `2b1d12`.
All files authored for Project Horizon (MIT, see repository licence).
