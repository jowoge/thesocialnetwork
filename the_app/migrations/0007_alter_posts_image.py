# Generated by Django 4.2.4 on 2023-09-16 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_app', '0006_alter_appuser_pfp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_image'),
        ),
    ]
