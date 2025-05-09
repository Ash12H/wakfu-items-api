from enum import StrEnum


class Categories(StrEnum):
    actions = "actions"
    "Contient les descriptions des types d'effets (perte de PdV, boost de PA, etc)."

    blueprints = "blueprints"
    "Contient la liste des plans débloquant des recettes."

    collectibleResources = "collectibleResources"
    "Contient les actions de récolte."

    equipmentItemTypes = "equipmentItemTypes"
    "Contient les définitions des types d'équipements et des emplacements associés."

    harvestLoots = "harvestLoots"
    "Contient les objets récupérés via la récolte."

    itemTypes = "itemTypes"
    "Contient les définitions des types d'objets."

    itemProperties = "itemProperties"
    "Contient les propriétés qui peuvent être appliquées à des objets."

    items = "items"
    "Contient les données relatives aux items, leurs effets, nom, description, etc. À croiser avec les données actions, equipmentItemTypes et itemProperties."

    jobsItems = "jobsItems"
    "Contient les données relatives aux items récoltés, craftés et utilisés par les recettes de craft (version light du items.json)."

    recipeCategories = "recipeCategories"
    "Contient la liste des métiers."

    recipeIngredients = "recipeIngredients"
    "Contient les ingrédients des crafts."

    recipeResults = "recipeResults"
    "Contient les objets produits par les crafts."

    recipes = "recipes"
    "Contient la liste des recettes."

    resourceTypes = "resourceTypes"
    "Contient les types de ressources."

    resources = "resources"
    "Contient les ressources."

    states = "states"
    "Contient les traductions des états utilisés par les équipements."


if __name__ == "__main__":
    # Test the Categories enum
    print(f"All categories : {[category.value for category in Categories]}")
