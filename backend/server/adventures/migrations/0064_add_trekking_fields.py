# Generated manually for trekking transformation

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0063_alter_activity_timezone_alter_lodging_timezone_and_more'),
    ]

    operations = [
        # Add trekking fields to Location model
        migrations.AddField(
            model_name='location',
            name='elevation',
            field=models.FloatField(blank=True, help_text='Elevation in meters', null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='difficulty_level',
            field=models.CharField(
                blank=True,
                choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard'), ('very_hard', 'Very Hard'), ('extreme', 'Extreme')],
                max_length=50,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='location',
            name='terrain_type',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=100),
                blank=True,
                help_text='Types of terrain: trail, scree, rock, snow, ice, etc.',
                null=True,
                size=None
            ),
        ),
        migrations.AddField(
            model_name='location',
            name='point_type',
            field=models.CharField(
                choices=[
                    ('summit', 'Summit/Peak'),
                    ('viewpoint', 'Viewpoint'),
                    ('refuge', 'Refuge/Hut'),
                    ('campsite', 'Campsite'),
                    ('water_source', 'Water Source'),
                    ('pass', 'Mountain Pass'),
                    ('trailhead', 'Trailhead'),
                    ('emergency_shelter', 'Emergency Shelter'),
                    ('waypoint', 'General Waypoint'),
                    ('other', 'Other')
                ],
                default='waypoint',
                max_length=50
            ),
        ),
        migrations.AddField(
            model_name='location',
            name='has_mobile_coverage',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='is_emergency_point',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='location',
            name='water_available',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='permits_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='location',
            name='permit_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='best_season_start',
            field=models.IntegerField(blank=True, help_text='Best season start month (1-12)', null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='best_season_end',
            field=models.IntegerField(blank=True, help_text='Best season end month (1-12)', null=True),
        ),

        # Add trek log fields to Visit model
        migrations.AddField(
            model_name='visit',
            name='weather_conditions',
            field=models.TextField(blank=True, help_text='Weather conditions during the trek', null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='trail_conditions',
            field=models.TextField(blank=True, help_text='Trail conditions (muddy, snow-covered, etc.)', null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='snow_level',
            field=models.FloatField(blank=True, help_text='Snow level in meters elevation', null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='companions',
            field=models.IntegerField(blank=True, help_text='Number of companions', null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='completed',
            field=models.BooleanField(default=True, help_text='Whether the trek was completed'),
        ),
        migrations.AddField(
            model_name='visit',
            name='abandoned_reason',
            field=models.TextField(blank=True, help_text='Reason if trek was abandoned', null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='public_report',
            field=models.BooleanField(default=False, help_text='Share as community trail report'),
        ),

        # Add route fields to Collection model
        migrations.AddField(
            model_name='collection',
            name='route_type',
            field=models.CharField(
                choices=[
                    ('circular', 'Circular Loop'),
                    ('linear', 'Linear/Out and Back'),
                    ('traverse', 'Traverse/Point to Point'),
                    ('multi_day', 'Multi-Day Trek')
                ],
                default='linear',
                max_length=50
            ),
        ),
        migrations.AddField(
            model_name='collection',
            name='total_distance',
            field=models.FloatField(blank=True, help_text='Total route distance in kilometers', null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='total_elevation_gain',
            field=models.FloatField(blank=True, help_text='Total elevation gain in meters', null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='total_elevation_loss',
            field=models.FloatField(blank=True, help_text='Total elevation loss in meters', null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='estimated_duration',
            field=models.DurationField(blank=True, help_text='Estimated duration for the route', null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='difficulty_level',
            field=models.CharField(
                blank=True,
                choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard'), ('very_hard', 'Very Hard'), ('extreme', 'Extreme')],
                max_length=50,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='collection',
            name='max_elevation',
            field=models.FloatField(blank=True, help_text='Maximum elevation in meters', null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='min_elevation',
            field=models.FloatField(blank=True, help_text='Minimum elevation in meters', null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='technical_grade',
            field=models.CharField(blank=True, help_text='Technical climbing grade if applicable', max_length=50, null=True),
        ),
    ]
