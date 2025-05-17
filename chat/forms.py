from django import forms

class RoomForm(forms.Form):
    """
    Form for creating a new chat room.
    """
    name = forms.CharField(
        label="Room Name",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )