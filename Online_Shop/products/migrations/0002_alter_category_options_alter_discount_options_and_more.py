# Generated by Django 4.1.5 on 2023-03-02 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'دسته', 'verbose_name_plural': 'دسته ها'},
        ),
        migrations.AlterModelOptions(
            name='discount',
            options={'verbose_name': 'تخفیف', 'verbose_name_plural': 'Discounts'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',), 'verbose_name': 'محصول', 'verbose_name_plural': 'محصولات'},
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/categories/img/%Y/%m', verbose_name='عکس'),
        ),
        migrations.AlterField(
            model_name='category',
            name='is_sub',
            field=models.BooleanField(default=False, verbose_name='زیر دسته'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='category',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scategory', to='products.category', verbose_name='زیر دسته از'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='end_date',
            field=models.DateTimeField(verbose_name='معتبر تا'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='start_date',
            field=models.DateTimeField(verbose_name='معتبر از'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='type',
            field=models.CharField(choices=[('val', 'value'), ('per', 'percent')], max_length=3, verbose_name='نوع'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='value',
            field=models.IntegerField(verbose_name='مقدار'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='products', to='products.category', verbose_name='دسته'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_obj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.discount', verbose_name='تخفیف'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='products/products/img/%Y/%m', verbose_name='عکس'),
        ),
        migrations.AlterField(
            model_name='product',
            name='initial_price',
            field=models.IntegerField(verbose_name='قیمت اولیه'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(verbose_name='تعداد'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='به روز رسانی شده در'),
        ),
    ]
