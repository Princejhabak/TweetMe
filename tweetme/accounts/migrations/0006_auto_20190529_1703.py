# Generated by Django 2.0.5 on 2019-05-29 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0005_remove_tweetlike_likes'),
        ('admin', '0002_logentry_remove_auto_add'),
        ('accounts', '0005_user_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_ptr',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]