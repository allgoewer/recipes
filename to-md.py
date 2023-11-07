#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import sys
import yaml
import jinja2


TEMPLATE = jinja2.Template('''---
title: {{ recipe.name }}
...

{% if image %}
![](data:image/jpg;base64,{{ image }})
{% endif %}

Rezept für __{{ portions }} Portion(en)__


## Zutaten
{% for ingredient in recipe.ingredients %}
* {{ ingredient -}}
{% endfor %}


## Zubereitung
{% for step in recipe.steps %}
{{ step }}
{% endfor %}
''')


def terminate_sentence(sentence):
    if sentence.endswith("."):
        return sentence
    else:
        return sentence + "."


def scale_ingredient(ingredient, scale):
    try:
        amount, remainder = ingredient.split(maxsplit=1)
        amount = float(amount)
    except ValueError:
        return ingredient

    return f"{amount * scale} {remainder}"


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        recipe = yaml.safe_load(f)

    try:
        portions = int(sys.argv[2])
    except IndexError:
        portions = recipe["portions"]

    recipe["steps"] = [terminate_sentence(s) for s in recipe["steps"]]
    recipe["ingredients"] = [scale_ingredient(i, portions / recipe["portions"])
                             for i in recipe["ingredients"]]

    try:
        with open(recipe["image"], "rb") as f:
            image = f.read()
            image = base64.b64encode(image).decode("utf-8")
    except KeyError:
        image = None

    print(TEMPLATE.render(portions=portions, recipe=recipe, image=image))
