from django import forms

from users.models import Person, Relation

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name',
            'last_name',
            'city',
            'profession',
            'birth_date',
            'date_of_death',
            'x_pos',
            'y_pos'
        ]


class RelationForm(forms.ModelForm):
    class Meta:
        model = Relation
        fields = [
            'parent',
            'child',
        ]
