# Generated by Django 3.0.5 on 2020-05-31 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_userfollowing'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBlocking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('blocking_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_by', to='profile.Profile')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocking', to='profile.Profile')),
            ],
            options={
                'ordering': ['-created'],
                'unique_together': {('user_id', 'blocking_user_id')},
            },
        ),
    ]