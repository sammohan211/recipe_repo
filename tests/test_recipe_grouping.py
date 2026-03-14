from app.models.recipes import RecipeCandidate
from app.services.recipe_suggester import group_recipes


def test_groups_recipe_can_make_now_when_only_staples_are_missing() -> None:
    candidates = [
        RecipeCandidate(
            title="Tomato Pasta",
            url="https://example.com/tomato-pasta",
            ingredients=["pasta", "tomato", "salt", "oil"],
        )
    ]

    response = group_recipes(
        candidates=candidates,
        inventory=["pasta", "tomato"],
        pantry_staples=["salt", "oil"],
        max_missing=3,
    )

    assert len(response.can_make_now) == 1
    assert response.can_make_now[0].missing_ingredients == []
    assert response.missing_a_few == []


def test_groups_recipe_as_missing_a_few_when_under_limit() -> None:
    candidates = [
        RecipeCandidate(
            title="Veggie Stir Fry",
            url="https://example.com/stir-fry",
            ingredients=["broccoli", "carrot", "soy sauce", "garlic"],
        )
    ]

    response = group_recipes(
        candidates=candidates,
        inventory=["carrot", "garlic"],
        pantry_staples=["salt", "oil"],
        max_missing=3,
    )

    assert response.can_make_now == []
    assert len(response.missing_a_few) == 1
    assert response.missing_a_few[0].missing_ingredients == ["broccoli", "soy sauce"]


def test_excludes_recipe_when_missing_more_than_limit() -> None:
    candidates = [
        RecipeCandidate(
            title="Big Shopping Meal",
            url="https://example.com/big-meal",
            ingredients=["a", "b", "c", "d"],
        )
    ]

    response = group_recipes(
        candidates=candidates,
        inventory=["a"],
        pantry_staples=[],
        max_missing=2,
    )

    assert response.can_make_now == []
    assert response.missing_a_few == []
