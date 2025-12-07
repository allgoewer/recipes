#let recipe(portions: [], ingredients: (), img: "", lang: "de", doc) = {
  set page(
    width: 80mm,
    height: auto,
    margin: (top: 4mm, bottom: 4mm, right: 8mm, left: 1mm)
  )
  set text(font: "Cascadia Code", size: 10pt, lang: lang)
  set par(justify: true)
  set table(
    columns: (auto, 1fr),
    align: (right, left),
    stroke: none,
  )

  show table: set par(justify: false)
  show title: set par(justify: false)
  show title: set align(left)
  show title: set block(below: 1.2em)
  show title: set text(fill: white, size: 16pt, hyphenate: auto)
  show title: it => rect(radius: 1mm, fill: black)[#it]
  show heading: set block(below: 1.2em)
  show heading: set text(fill: white)
  show heading: it => rect(radius: 1mm, fill: black)[#it]

  title()

  if img.len() > 0 {
    image(img)
  }

  if lang == "de" {
    [Rezept für #portions #if portions > 1 [Portionen] else [Portion]]
  } else {
    [Recipe for #portions  #if portions > 1 [portions] else [portion]]
  }

  table(..ingredients)

  if lang == "de" {
    [= Zubereitung]
  } else {
    [= Steps]
  }

  show regex("\d+ (.?C|Grad)"): it => {box()[#emoji.fire *#it* #emoji.fire]}
  
  doc
}
