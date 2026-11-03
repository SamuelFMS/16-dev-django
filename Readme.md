# Poll Forum

## 2.2.1

### 3. Visualisez le résultat de vos saisies dans l'interface d'admin.
- __Voyez-vous tous les attributs de vos classes ?__
Non Seulement la méthode `__str__` est affiché
- __Pouvez-vous filtrer vos données suivants tous les attributs ?__
Non imppossible de filtrer pour l'instant, cependant User oui
- __Pouvez-vous trier vos données suivants tous les attributs ?__
Non impossible pour l'instant, idem
- __Pouvez-vous chercher un contenu parmi tous les champs ?__
Non impossible pour l'instant, idem

### 5. Ajoutez un nouvel utilisateur via l'interface d'admin. Ne lui donnez pas le "Statut équipe" ni le "Statut super-utilisateur". Déconnectez-vous et essayer de vous reconnecter avec ce nouveau compte. Y parvenez-vous ?
Non je ne parviens pas a me connecter

## 2.2.2.2 Questions
- __1. Lister tous les objets de type Question : faites une boucle pour afficher les attributs de 
chaque question sur une ligne différente. Indice : remarquer que
Question.objects.all() est un itérable sur lequel vous pouvez boucler avec une 
simple boucle for__
```python
for e in Question.objects.all():
    print(e)
```

- __2. Ajoutez un filtre sur la date de publication – portant par ex. sur un de ses composants4
suivants : year, month, day – de vos questions et lister un sous-ensemble de vos 
questions suivant les dates que vous avez saisies à l'exercice précédent.__
```python
for e in Question.objects.filter(pub_date__year=2025):
    print(e)
```

- __3. Trouvez la deuxième question (pour laquelle l'attribut de clé primaire id = 2) de votre base 
de données, puis affichez les valeurs de tous ses attributs et tous les choix associés.__
```python
QuestionDeux = Question.objects.get(id=2)
print(QuestionDeux)
mesChoix = Choice.objects.filter(question=QuestionDeux)
for choix in mesChoix:
    print(choix)
```

- __4. Faites une boucle pour afficher les attributs de chaque question et leurs choix associés.__
```python
AllQuestion = Question.objects.all()
for cquestion in AllQuestion:
    print(cquestion)
    mesChoix = Choice.objects.filter(question=cquestion)
    for choix in mesChoix:
        print(choix)
```

- __5. Affichez le nombre de choix enregistrés pour chaque question.__
```python
AllQuestion = Question.objects.all()
for cquestion in AllQuestion:
    cvote = 0
    mesChoix = Choice.objects.filter(question=cquestion)
    for choix in mesChoix:
        cvote += choix.votes
    print(cquestion , " nombre de vote: ", cvote)
```

- __7. Triez les questions par ordre antéchronologique.__
```python
from django.db.models import F

print(Question.objects.order_by(F("pub_date").desc()))

```

- __9. Créez une question en utilisant le shell.__
```python
from django.utils import timezone
nouvelleQuestion = Question.objects.create(question_text="Niveau developpement?", pub_date=timezone.now())

```

- __10. Ajoutez 3 choix à cette question en utilisant le shell.__
```python
nouvelleQuestion.choice_set.create(choice_text="Amateur", votes=0)
nouvelleQuestion.choice_set.create(choice_text="Intermédiaire", votes=0)
nouvelleQuestion.choice_set.create(choice_text="Expert", votes=0)
```

- __11. Listez les questions publiées récemment__
```python
from django.db.models import F

QuestionsTries = Question.objects.order_by(F("pub_date").desc())[:5]
for question in QuestionsTries:
    print(question)
```