from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from .models import Recipe, Category, GroceryList, Ingredient, MyListIngredient, RecipeIngredient, RecipeInstruction
from .forms import CustomUserCreationForm, CreateGroceryListForm, IngredientInstanceForm, CreateRecipeForm, AddIngredientsForm, CreateRecipeInstructionForm
from django.urls import reverse
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models.functions import Lower


class MyCustomError(Exception):     
    # Constructor
    def __init__(self, value):  
        self.value = value  
    
    def __str__(self):  
        return(repr(self.value)) 


def index(request):
    return render(request, "mymeals/index.html", context={
        'active_page': 'home',
    })


def register(request):
    if request.method == 'POST':
        # Bind POST data to custom form
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Creates user
            # Log the new user in after the user has been created
            username = form.cleaned_data['username']
            # Use the raw password to authenticate
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=username, password=raw_password)

            login(request, user)
            # Link messsage to request object to display success to user
            messages.success(request, 'You have registered successfully!') 
            return HttpResponseRedirect(reverse('recipes'))

    else:
        form = CustomUserCreationForm()
    return render(request, "mymeals/register.html", context = {
        'form': form,
    })


""" Recipes views section """
@login_required
def recipes(request):
    categories = Category.objects.all()
    print(categories)
    return render(request, "mymeals/recipes.html", context = {
        'categories': categories,
        'active_page': 'recipes',
    })

@login_required
def create_recipe(request):
    if request.method == 'POST':
        recipe_form = CreateRecipeForm(request.POST, request.FILES)
        recipe_ingredients = request.POST.getlist('ingredient')
        recipe_ingredients_quantities = request.POST.getlist('quantity')
        instructions = request.POST.getlist('instruction')
        print(recipe_ingredients)
        print(recipe_ingredients_quantities)
        print(instructions)

        instructions_form_list = [] # Initialize an empty list to keep track of the instructions forms
        ingredient_form_list = []  # Initialize an empty list to keep track of the ingredient forms in case we need to send back errors to user.

        # Do atomic save (make sure if there are any failures that all data is not saved and is rolled back, so user can resubmit the form)
        try:
            with transaction.atomic():
                has_errors = False  # Create a flag for errors in this transaction
                
                # Save the recipe
                if recipe_form.is_valid():
                    new_recipe = recipe_form.save()
                    new_recipe.author = request.user
                    new_recipe.save()
                else:
                    has_errors = True
                    new_recipe = None

                # Save the instructions list
                for i in range(len(instructions)):
                    form = CreateRecipeInstructionForm({'instruction':instructions[i]}, auto_id=False)
                    
                    if form.is_valid() and new_recipe:
                        instruction = form.cleaned_data['instruction']
                        new_instruction = RecipeInstruction.objects.create(recipe_instruction=instruction, recipe=new_recipe)
                        new_instruction.save()
                        
                    else:
                        has_errors = True
                    instructions_form_list.append(form)
                
                print(instructions_form_list)

                # Save the ingredients
                for i in range(len(recipe_ingredients)):
                    form = IngredientInstanceForm({'ingredient':recipe_ingredients[i], 'quantity':recipe_ingredients_quantities[i]}, auto_id=False)
                    
                    if form.is_valid() and new_recipe:
                        ingredient = form.cleaned_data['ingredient']
                        ingredient_name, created = Ingredient.objects.get_or_create(name=ingredient)
                        ingredient_name.save()
                        quantity = int(form.cleaned_data['quantity'])
                        new_ingredient = RecipeIngredient.objects.create(ingredient=ingredient_name, quantity=quantity, recipe=new_recipe)
                        new_ingredient.save()
                        
                    else:
                        has_errors = True
                    ingredient_form_list.append(form)
                print(ingredient_form_list)

                if not has_errors:
                    return HttpResponseRedirect(reverse('recipe-detail', args=[new_recipe.id]))
                else:
                    raise MyCustomError("Failed, there were form errors. db should be rolled back. And errors should be passed on to the template.")

        except MyCustomError as e:
            print(e)

    else:
        # Generate unbound forms to pass on to template
        recipe_form = CreateRecipeForm()   
        ingredient_form_list = [IngredientInstanceForm(auto_id=False),]
        instructions_form_list = [CreateRecipeInstructionForm(auto_id=False),]
    
    return render(request, "mymeals/create-recipe.html", context = {
        'recipe_form': recipe_form,
        'recipe_ingredient_form': ingredient_form_list,
        'instruction_form': instructions_form_list,
    })

@login_required
def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    instructions_form_list = [] # Initialize an empty list to keep track of the instructions forms
    ingredient_form_list = []  # Initialize an empty list to keep track of the ingredient forms in case we need to send back errors to user.

    if request.method == 'POST':   
        recipe_ingredients = request.POST.getlist('ingredient')
        recipe_ingredients_quantities = request.POST.getlist('quantity')
        instructions = request.POST.getlist('instruction')
        print(recipe_ingredients)
        print(recipe_ingredients_quantities)
        print(instructions)

        # Do atomic save (make sure if there are any failures that all data is not saved and is rolled back, so user can resubmit the form)
        try:
            with transaction.atomic():
                has_errors = False  # Create a flag for errors in this transaction
                
                # Save the recipe
                recipe_form = CreateRecipeForm(request.POST, request.FILES, instance=recipe)
                if recipe_form.is_valid():
                    recipe_form.save()
                else:
                    has_errors = True
                
                # clear the existing recipe instructions list
                recipe.recipe_instructions.all().delete()

                # Save the new instructions list to recipe
                for i in range(len(instructions)):
                    form = CreateRecipeInstructionForm({'instruction':instructions[i]}, auto_id=False)
                    # Execute is_valid method to get return value of errors if applicable.
                    # Only touch the database if there are no errors in the total transaction thus far,
                    # or else it is a waste of resource to execute the rest of if statement since we are only
                    # returning errors in the forms at this point.
                    if form.is_valid() and not has_errors:
                        instruction = form.cleaned_data['instruction']
                        new_instruction = RecipeInstruction.objects.create(recipe_instruction=instruction, recipe=recipe)
                        new_instruction.save()
                        
                    else:
                        has_errors = True
                    instructions_form_list.append(form)
                
                print(instructions_form_list)

                # clear the existing recipe instructions list
                recipe.my_recipe_ingredients.all().delete()
                
                # Save the ingredients
                for i in range(len(recipe_ingredients)):
                    form = IngredientInstanceForm({'ingredient':recipe_ingredients[i], 'quantity':recipe_ingredients_quantities[i]}, auto_id=False)
                    
                    if form.is_valid() and not has_errors:
                        ingredient = form.cleaned_data['ingredient']
                        ingredient_name, created = Ingredient.objects.get_or_create(name=ingredient)
                        ingredient_name.save()
                        quantity = int(form.cleaned_data['quantity'])
                        new_ingredient = RecipeIngredient.objects.create(ingredient=ingredient_name, quantity=quantity, recipe=recipe)
                        new_ingredient.save()
                        
                    else:
                        has_errors = True
                    ingredient_form_list.append(form)
                print(ingredient_form_list)

                if not has_errors:
                    return HttpResponseRedirect(reverse('recipe-detail', args=[recipe.id]))
                else:
                    raise MyCustomError("Failed, there were form errors. db should be rolled back. And errors should be passed on to the template.")

        except MyCustomError as e:
            print(e)

    else:
        # Generate forms with bound data form the recipe instance to pass to the template
        recipe_form = CreateRecipeForm(instance=recipe)

        # Bind existing recipe ingredient data to forms
        for item in recipe.my_recipe_ingredients.all():
            ingredient_form = IngredientInstanceForm({'ingredient':item.ingredient.name, 'quantity':item.quantity}, auto_id=False)
            ingredient_form_list.append(ingredient_form)


        # Bind existing recipe instruction data to forms
        for item in recipe.recipe_instructions.all():
            form = CreateRecipeInstructionForm({'instruction':item.recipe_instruction,}, auto_id=False)
            instructions_form_list.append(form)
    
    return render(request, "mymeals/update-recipe.html", context = {
        'recipe_form': recipe_form,
        'recipe_ingredient_form': ingredient_form_list,
        'instruction_form': instructions_form_list,
        'recipe': recipe,
    })

@login_required
def recipe_detail(request, recipe_id):
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")

    if request.method == "POST":
        form = AddIngredientsForm(recipe, request.user, request.POST)
        if form.is_valid():
            grocery_list = form.cleaned_data['grocery_lists'] # returns the grocerylist instance
            ingredients = form.cleaned_data['ingredients'] # returns the queryset
            for ingredient in ingredients:
                #Create a listingredient instance (note this is just copying the recipe ingredient into a list ingredient instance in case user wants to modify in list)
                new_list_ingredient = MyListIngredient.objects.create(ingredient=ingredient.ingredient, quantity=ingredient.quantity, grocery_list=grocery_list, recipe=recipe)
                new_list_ingredient.save()
            return HttpResponseRedirect(grocery_list.get_absolute_url())

    else:
        #Generate bound form with this recipes ingredient data
        form = AddIngredientsForm(recipe, request.user) 
        
    print(form.errors)

    return render(request, 'mymeals/recipe-detail.html', {
        'recipe': recipe,
        'form': form
        })


@login_required
@require_http_methods(["POST"])
def recipe_add_to_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    request.user.favorite_recipes.add(recipe)
    # Link messsage to request object to display success to user
    messages.success(request, 'You have successfully added to your favorites.') 
    return HttpResponseRedirect(reverse('recipe-detail', args=[recipe.id]))


@login_required
@require_http_methods(["POST"])
def recipe_remove_from_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    request.user.favorite_recipes.remove(recipe)
    # Link messsage to request object to display success to user
    messages.success(request, 'You have successfully removed from your favorites.') 
    return HttpResponseRedirect(reverse('recipe-detail', args=[recipe.id]))


@login_required
def my_favorite_recipes(request):
    recipes = request.user.favorite_recipes.all()
    return render(request, 'mymeals/favorite-recipes.html', {
        'recipes': recipes,
        })


""" Grocery list views section"""
@login_required
def create_list(request):
    my_lists = GroceryList.objects.filter(user=request.user)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreateGroceryListForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.user = request.user
            new_list.save()
            # redirect to a new URL:
            return HttpResponseRedirect(new_list.get_absolute_url())

    # If this is a GET (or any other method) create the default form.
    else:
        form = CreateGroceryListForm()

    context = {
        'form': form,
        'my_lists': my_lists,
        'active_page': 'lists',
    }

    return render(request, "mymeals/create-list.html", context)

@login_required
def my_list_detail(request, list_id, sort):
    try:
        my_list = GroceryList.objects.get(pk=list_id)

    except GroceryList.DoesNotExist:
        raise Http404("Grocery List does not exist")

    if request.method == 'POST':
        form = IngredientInstanceForm(request.POST)

        if form.is_valid():
            ingredient = form.cleaned_data['ingredient']
            quantity = int(form.cleaned_data['quantity'])
            
            # get or create an ingredient instance
            ingredient_instance = Ingredient.objects.get_or_create(name=ingredient)[0]
            print(ingredient_instance)
            my_list_ingredient = MyListIngredient.objects.get_or_create(ingredient=ingredient_instance, grocery_list=my_list)[0]
            my_list_ingredient.quantity += quantity
            my_list_ingredient.save()

            return HttpResponseRedirect(my_list.get_absolute_url())
    else:
        form = IngredientInstanceForm()
        if sort == 'az':
            ingredients = my_list.my_ingredients.order_by(Lower('ingredient__name'))
        elif sort == 'recipe':
            ingredients = my_list.my_ingredients.order_by(Lower('recipe__title'), Lower('ingredient__name'))
        else:
            raise Http404("Page does not exist")

    return render(request, 'mymeals/my-grocery-list.html', {
        'my_list': my_list,
        'form': form,
        'ingredients': ingredients,
        })


@login_required
def sort_my_list_detail(request, list_id, sort):
    grocery_list = get_object_or_404(GroceryList, pk=list_id)

    

    
@login_required
def delete_grocery_list_ingredient(request, pk):
    list_ingredient = get_object_or_404(MyListIngredient, pk=pk)
    grocery_list = list_ingredient.grocery_list

    if request.method == 'POST':
        list_ingredient.delete()
        return HttpResponseRedirect(grocery_list.get_absolute_url())

@login_required
def update_grocery_list_ingredient(request, pk):
    list_ingredient = get_object_or_404(MyListIngredient, pk=pk)
   
    grocery_list = list_ingredient.grocery_list

    if request.method == 'POST':
        form = IngredientInstanceForm(request.POST)

        if form.is_valid():
            print("valid")
            ingredient = form.cleaned_data['ingredient']
            quantity = int(form.cleaned_data['quantity'])

            ingredient_name, created = Ingredient.objects.get_or_create(name=ingredient)
            print(ingredient_name.pk)
            ingredient_name.save()
            list_ingredient.ingredient = ingredient_name            
            list_ingredient.quantity = quantity
            list_ingredient.save()
            return JsonResponse({"message": "You successfully updated server database"})

        else:
            # return Fail,
            # and the form errors to be displayed in html
            print("not valid")
            print(form.errors)
            return JsonResponse({'status':'false', 'errors': form.errors.as_json()}, status=400)
