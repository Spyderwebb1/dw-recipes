from django.forms import ModelForm
from django import forms
from .models import User, GroceryList, Ingredient, MyListIngredient, Recipe, RecipeIngredient, RecipeInstruction
from django.core.validators import MinValueValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _

# Customize the UserCreationForm in order to add email field and bootstrap classes
class CustomUserCreationForm(UserCreationForm):
    # Override the inherited declared form fields with desired form classes
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    # Per Django docs, subclass Meta data from UserCreationForm and override attributes as needed.
    class Meta(UserCreationForm.Meta):
        model = User
        # Note: These are the auto-generated form fields that you can modify their attributes (non-declared fields)
        fields = UserCreationForm.Meta.fields + ('email',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# Customize the AuthForm in order to override the fields with bootstrap classes
class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}),
    )


class CreateGroceryListForm(ModelForm):
    class Meta:
        model = GroceryList
        fields = ['nickname',]
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter list name..."}),
        }


class CreateIngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name',]


class CreateRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'serves', 'category', 'photo']
        labels = {
            'photo': _('Photo (optional)'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'serves': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CreateRecipeInstructionForm(forms.Form):
    instruction = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows':'3',}))


class IngredientInstanceForm(forms.Form):
    ingredient = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ingredient"}))
    quantity = forms.IntegerField(validators=[MinValueValidator(1)], widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Quantity"}))

    
class AddIngredientsForm(forms.Form):
    ingredients = forms.ModelMultipleChoiceField(error_messages={'required': 'Please select ingredient(s).'},
        queryset = RecipeIngredient.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),) 

    grocery_lists = forms.ModelChoiceField(
        queryset=None,
        empty_label="Choose from your lists...",
        widget= forms.Select(attrs={'class': 'form-select form-select-sm',}),
    )

    def __init__(self, recipe, user, *args, **kwargs):
        super(AddIngredientsForm, self).__init__(*args, **kwargs)
        
        ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        self.fields['ingredients'].queryset = ingredients

        grocery_lists = GroceryList.objects.filter(user=user)
        self.fields['grocery_lists'].queryset = grocery_lists


