from django.shortcuts import render, get_object_or_404, redirect
from .models import Equipement, Animal
from .forms import MoveForm
from django.contrib import messages

def animal_list(request):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'animalerie/animal_list.html', {'animaux': animaux, 'equipements': equipements})

def post_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    lieu = animal.lieu
    form=MoveForm()
    if request.method == "POST":
        ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        form = MoveForm(request.POST, instance=animal)
        if form.is_valid():
            form.save(commit=False)
            nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
            if nouveau_lieu.disponibilite=="libre" and nouveau_lieu.id_equip=="mangeoire" and animal.etat=='affame':
                animal.etat="repus"
                animal.save()
                nouveau_lieu.disponibilite="occupe"
                nouveau_lieu.save()
                messages.add_message(request, messages.SUCCESS, 'Votre animal a bien été déplacé dans la mangeoire !')
            elif nouveau_lieu.disponibilite=="libre" and nouveau_lieu.id_equip=="roue" and animal.etat=='repus':
                ancien_lieu.disponibilite="libre"
                ancien_lieu.save()
                animal.etat="fatigue"
                animal.save()
                nouveau_lieu.disponibilite = "occupe"
                nouveau_lieu.save()
                messages.add_message(request, messages.SUCCESS, 'Votre animal a bien été déplacé dans la roue !')
            elif nouveau_lieu.disponibilite=="libre" and nouveau_lieu.id_equip=="nid" and animal.etat=='fatigue':
                ancien_lieu.disponibilite="libre"
                ancien_lieu.save()
                animal.etat="endormi"
                animal.save()
                nouveau_lieu.disponibilite = "occupe"
                nouveau_lieu.save()
                messages.add_message(request, messages.SUCCESS, 'Votre animal a bien été déplacé dans le nid !')
            elif nouveau_lieu.disponibilite=="libre" and nouveau_lieu.id_equip=="litiere" and animal.etat=='endormi':
                ancien_lieu.disponibilite="libre"
                ancien_lieu.save()
                animal.etat="affame"
                animal.save()
                nouveau_lieu.disponibilite = "libre"
                nouveau_lieu.save()
                messages.add_message(request, messages.SUCCESS, 'Votre animal a bien été déplacé dans la litière !')
            elif nouveau_lieu==ancien_lieu:
                messages.add_message(request, messages.WARNING, 'Votre animal est déjà à cet endroit.')
            else :
                print('message')
                messages.add_message(request, messages.ERROR, 'Désolé, vous ne pouvez pas déplacer cet animal à cet endroit.')
        return redirect('post_detail', id_animal=id_animal)
    else:
        form = MoveForm()
        return render(request,
                  'animalerie/post_detail.html',
                  {'animal': animal, 'lieu': lieu, 'form': form})