# Generated by Django 4.1.5 on 2023-03-02 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_category_options_alter_discount_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discount',
            options={'verbose_name': 'تخفیف', 'verbose_name_plural': 'تخفیف ها'},
        ),
    ]
