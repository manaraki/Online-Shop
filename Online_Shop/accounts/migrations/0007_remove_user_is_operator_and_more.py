# Generated by Django 4.1.5 on 2023-03-02 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_onetimepassword_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_operator',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_product_manager',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_supervisor',
        ),
    ]
