# Recipes

A collection of recipe `.yml` files, rendered to Typst and printed on a
receipt printer (`bin/precipe` → `bin/to-typ.py` → `typst compile` → `lp`).

## Adding/editing a recipe

Copy `template.yml` as a starting point. Fields:

```yaml
name: Display Name
image: img/slug.jpg      # optional; omit the key entirely if there's no photo
portions: 4               # integer, servings the ingredient list is written for
ingredients:
  - 200 g; Zutat
  - Zutat ohne Menge
steps:
  - Erster Schritt.
  - Zweiter Schritt.
```

- **File name**: kebab-case slug of the recipe name, German umlauts kept as-is
  (e.g. `gemüseauflauf-mit-filo-teig.yml`, not transliterated to `ue`/`oe`).
  Matches the image file base name when one exists.
- **Language**: everything (name, ingredients, steps) is in German.
- **Images**: live in `img/`, referenced as `img/<slug>.<ext>` (jpg/png).
  Not every recipe has one — many don't. Resize images to 400x300 with
  imagemagick if necessary.

### `ingredients`

Each entry is either `<amount>; <ingredient>` or just `<ingredient>` (no
amount, e.g. "Salz & Pfeffer", "Öl"). The part before `;` is parsed by
`scale_ingredient()` in `bin/to-typ.py` to scale quantities when printing a
different portion count, so keep it machine-parseable:

- `<number> <unit>; ...` — e.g. `150 g; Karotten`, `1 EL; Öl` — the number
  scales, the unit is copied as-is.
- `<number>; ...` — no unit, just a count — e.g. `4; Eier`.
- Non-numeric or ranged amounts (`2 - 3 EL`, `1 gr.`) are left untouched by
  scaling (only exact `float()`-parseable leading numbers scale). Prefer a
  single number when a range isn't essential.
- Decimals use a dot: `0.5 TL`, `0.33 l`.
- Multi-word units are fine (`1 geh. TL`, `1 kleine handvoll`, `2 Prise(n)`) —
  everything after the first space in the amount is treated as the unit.

### `steps`

- Plain imperative/infinitive German instructions, one per list item.
- No need to add a trailing period — `to-typ.py` appends one if missing.
- Long steps may be wrapped across multiple YAML lines (block scalar folding
  via plain multi-line list items); indentation just needs to line up under
  the `-`. This is only for readability of the source file, not required.

## Rendering / testing a change

```sh
bin/to-typ.py <file>.yml [portions] | typst compile --font-path typst/fonts - out.png
```

Omit `portions` to render at the recipe's native portion count.
