# Generated by Django 5.1.4 on 2025-01-10 03:43

from django.db import migrations

# Migrate data from ChallengeInteraction and GridInteraction to TileInteraction.


def combine_grid_challenge_interaction(apps, schema_editor):
    """
    For each GridInteraction object that contains ChallengeInteraction objects,
    combine these objects into the new TileInteraction Object.
    ChallengeInteraction objects that have no corresponding GridInteraction object will be
    deleted in the next migration, as they have no data for the grid field.
    """
    GridInteraction = apps.get_model("bingo", "GridInteraction")
    TileInteraction = apps.get_model("bingo", "TileInteraction")
    for gi in GridInteraction.objects.all():
        cis = gi.challenge_interactions.all()
        position = 0
        if cis:
            for ci in cis:
                TileInteraction.objects.create(user=ci.user, position=position, grid=gi.grid,
                                               image=ci.image, completed=ci.completed, consent=ci.consent,
                                               date_started=ci.date_started, date_completed=ci.date_completed)
                position += 1


class Migration(migrations.Migration):

    dependencies = [
        ("bingo", "0010_tileinteraction"),
    ]

    operations = [
        migrations.RunPython(combine_grid_challenge_interaction),
    ]
