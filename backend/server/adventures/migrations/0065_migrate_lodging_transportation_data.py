# Generated manually for data migration: Lodging → Location, Transportation → Note

from django.db import migrations


def migrate_lodging_to_locations(apps, schema_editor):
    """
    Migrate existing Lodging entries to Location entries with point_type='refuge'
    """
    Lodging = apps.get_model('adventures', 'Lodging')
    Location = apps.get_model('adventures', 'Location')
    Visit = apps.get_model('adventures', 'Visit')
    Category = apps.get_model('adventures', 'Category')

    for lodging in Lodging.objects.all():
        # Get or create "Refuge" category for this user
        refuge_category, _ = Category.objects.get_or_create(
            user=lodging.user,
            name='refuge',
            defaults={'display_name': 'Refuge/Accommodation', 'icon': '🏠'}
        )

        # Create a new Location from the Lodging
        location = Location.objects.create(
            user=lodging.user,
            name=lodging.name,
            category=refuge_category,
            description=lodging.description or '',
            rating=lodging.rating,
            link=lodging.link,
            latitude=lodging.latitude,
            longitude=lodging.longitude,
            location=lodging.location,
            is_public=lodging.is_public,
            point_type='refuge',
            created_at=lodging.created_at,
            updated_at=lodging.updated_at
        )

        # Add location to the collection if it exists
        if lodging.collection:
            location.collections.add(lodging.collection)

        # Create a Visit if check_in exists
        if lodging.check_in:
            visit_notes = f"Lodging: {lodging.type if hasattr(lodging, 'type') else 'N/A'}\n"
            if lodging.price:
                visit_notes += f"Price: {lodging.price}\n"
            if lodging.reservation_number:
                visit_notes += f"Reservation: {lodging.reservation_number}"

            Visit.objects.create(
                location=location,
                start_date=lodging.check_in,
                end_date=lodging.check_out or lodging.check_in,
                timezone=lodging.timezone,
                notes=visit_notes.strip()
            )

        # Migrate images (ContentImage with GenericForeignKey)
        ContentImage = apps.get_model('adventures', 'ContentImage')
        ContentType = apps.get_model('contenttypes', 'ContentType')

        lodging_content_type = ContentType.objects.get_for_model(Lodging)
        location_content_type = ContentType.objects.get_for_model(Location)

        for image in ContentImage.objects.filter(
            content_type=lodging_content_type,
            object_id=str(lodging.id)
        ):
            image.content_type = location_content_type
            image.object_id = str(location.id)
            image.save()

        # Migrate attachments
        ContentAttachment = apps.get_model('adventures', 'ContentAttachment')
        for attachment in ContentAttachment.objects.filter(
            content_type=lodging_content_type,
            object_id=str(lodging.id)
        ):
            attachment.content_type = location_content_type
            attachment.object_id = str(location.id)
            attachment.save()


def migrate_transportation_to_notes(apps, schema_editor):
    """
    Migrate existing Transportation entries to Note entries within Collections
    """
    Transportation = apps.get_model('adventures', 'Transportation')
    Note = apps.get_model('adventures', 'Note')

    for transportation in Transportation.objects.all():
        # Create note content from transportation data
        note_content = f"**Transportation: {transportation.type}**\n\n"

        if transportation.from_location and transportation.to_location:
            note_content += f"Route: {transportation.from_location} → {transportation.to_location}\n"
        elif transportation.from_location:
            note_content += f"From: {transportation.from_location}\n"
        elif transportation.to_location:
            note_content += f"To: {transportation.to_location}\n"

        if transportation.flight_number:
            note_content += f"Flight Number: {transportation.flight_number}\n"

        if transportation.date:
            note_content += f"Departure: {transportation.date}\n"

        if transportation.end_date:
            note_content += f"Arrival: {transportation.end_date}\n"

        if transportation.description:
            note_content += f"\n{transportation.description}"

        # Create Note
        note = Note.objects.create(
            user=transportation.user,
            name=f"Transportation: {transportation.name}",
            content=note_content.strip(),
            date=transportation.date.date() if transportation.date else None,
            collection=transportation.collection,
            is_public=transportation.is_public,
            created_at=transportation.created_at,
            updated_at=transportation.updated_at
        )

        # Migrate images
        ContentImage = apps.get_model('adventures', 'ContentImage')
        ContentType = apps.get_model('contenttypes', 'ContentType')

        transportation_content_type = ContentType.objects.get_for_model(Transportation)
        note_content_type = ContentType.objects.get_for_model(Note)

        for image in ContentImage.objects.filter(
            content_type=transportation_content_type,
            object_id=str(transportation.id)
        ):
            image.content_type = note_content_type
            image.object_id = str(note.id)
            image.save()

        # Migrate attachments
        ContentAttachment = apps.get_model('adventures', 'ContentAttachment')
        for attachment in ContentAttachment.objects.filter(
            content_type=transportation_content_type,
            object_id=str(transportation.id)
        ):
            attachment.content_type = note_content_type
            attachment.object_id = str(note.id)
            attachment.save()


def reverse_lodging_migration(apps, schema_editor):
    """
    Reverse migration - not implemented as this is a one-way transformation
    """
    # This is a one-way migration. Reverting would require complex logic
    # and potential data loss. Manual intervention recommended if reversal needed.
    pass


def reverse_transportation_migration(apps, schema_editor):
    """
    Reverse migration - not implemented as this is a one-way transformation
    """
    # This is a one-way migration. Reverting would require complex logic
    # and potential data loss. Manual intervention recommended if reversal needed.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0064_add_trekking_fields'),
    ]

    operations = [
        migrations.RunPython(
            migrate_lodging_to_locations,
            reverse_lodging_migration
        ),
        migrations.RunPython(
            migrate_transportation_to_notes,
            reverse_transportation_migration
        ),
    ]
