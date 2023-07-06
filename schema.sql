# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountInterest(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    interest = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_interest'


class AccountUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    id = models.CharField(primary_key=True, max_length=32)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=254)
    image = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10)
    is_admin = models.BooleanField()
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'account_user'


class AccountUserFavorite(models.Model):
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)
    recipe = models.ForeignKey('RecipeRecipe', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_user_favorite'
        unique_together = (('user', 'recipe'),)


class AccountUserGroups(models.Model):
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_user_groups'
        unique_together = (('user', 'group'),)


class AccountUserInterest(models.Model):
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)
    interest = models.ForeignKey(AccountInterest, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_user_interest'
        unique_together = (('user', 'interest'),)


class AccountUserLastView(models.Model):
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)
    recipe = models.ForeignKey('RecipeRecipe', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_user_last_view'
        unique_together = (('user', 'recipe'),)


class AccountUserUserPermissions(models.Model):
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class RecipeCategoryingredient(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'recipe_categoryingredient'


class RecipeCoreingredient(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=50)
    categoryingredient = models.ForeignKey(RecipeCategoryingredient, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'recipe_coreingredient'


class RecipeIngredient(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    number = models.IntegerField()
    unit = models.CharField(max_length=10)
    quantity = models.IntegerField()
    recipe_fk = models.ForeignKey('RecipeRecipe', models.DO_NOTHING)
    coreingredient = models.ForeignKey(RecipeCoreingredient, models.DO_NOTHING, blank=True, null=True)
    note = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'recipe_ingredient'


class RecipeMethod(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    number = models.IntegerField()
    method_text = models.TextField()
    recipe_fk = models.ForeignKey('RecipeRecipe', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipe_method'


class RecipeRecipe(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.CharField(max_length=100)
    duration = models.IntegerField()
    portion = models.IntegerField()
    calories = models.IntegerField()
    difficulty = models.CharField(max_length=10)
    view = models.IntegerField()
    fav = models.IntegerField()
    updated_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'recipe_recipe'


class RecipeRecipeGuest(models.Model):
    recipe = models.ForeignKey(RecipeRecipe, models.DO_NOTHING)
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipe_recipe_guest'
        unique_together = (('recipe', 'user'),)


class RecipeRecipeIngredient(models.Model):
    recipe = models.ForeignKey(RecipeRecipe, models.DO_NOTHING)
    ingredient = models.ForeignKey(RecipeIngredient, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipe_recipe_ingredient'
        unique_together = (('recipe', 'ingredient'),)


class RecipeRecipeMethod(models.Model):
    recipe = models.ForeignKey(RecipeRecipe, models.DO_NOTHING)
    method = models.ForeignKey(RecipeMethod, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipe_recipe_method'
        unique_together = (('recipe', 'method'),)
