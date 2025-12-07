#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import sys
import yaml
import jinja2

TEMPLATE = jinja2.Template("""
#import "typst/bix.typ": recipe

#set document(title: [{{ recipe.name }}])

#show: recipe.with(
  portions: {{ portions }},
  {%- if image_path %}
  img: "/{{ image_path }}",
  {%- endif %}
  ingredients: (
    {%- for ingredient in recipe.ingredients %}
    [{{ ingredient[0] }}], [{{ ingredient[1] }}],
    {%- endfor %}
  )
)

{% for step in recipe.steps %}
+ {{ step }}
{% endfor %}
""")


def terminate_sentence(sentence: str) -> str:
    if sentence.endswith("."):
        return sentence
    else:
        return sentence + "."


def scaled(f: float) -> float | int:
    after_comma = f % 1.0
    return f if after_comma > 0.2 and after_comma < 0.8 else round(f)


def scale_ingredient(ingredient: str, scale: float = 1.0) -> tuple[str, str]:
    ingredients = ingredient.split(";", maxsplit=1)
    if len(ingredients) == 1:
        return "", ingredients[0].strip()

    amount, ingredient = ingredients
    amount = amount.strip()
    ingredient = ingredient.strip()

    amount = amount.split(maxsplit=1)
    if len(amount) == 1:
        try:
            amount = float(amount[0])
            return f"{scaled(amount * scale)}", ingredient
        except ValueError:
            return amount[0], ingredient
    else:
        try:
            count = float(amount[0])
            unit = amount[1]
            return f"{scaled(count * scale)} {unit}", ingredient
        except ValueError:
            return f"{amount[0]} {amount[1]}", ingredient

    return amount, ingredient


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
            _, image_extension = recipe["image"].rsplit(".", maxsplit=1)
            image = f.read()
            image = base64.b64encode(image).decode("utf-8")
    except KeyError:
        image = None
        image_extension = None

    print(TEMPLATE.render(portions=portions, recipe=recipe,
                          image=image, image_ext=image_extension,
                          image_path=recipe.get("image")))
