# Generated by Django 4.1.1 on 2022-09-20 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_options'),
        ('accounts', '0002_user_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='product_fav',
            field=models.ManyToManyField(to='products.product'),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='zip_number',
            field=models.CharField(max_length=5),
        ),
    ]
