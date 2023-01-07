import datetime
from django import forms
from gestao.models import perfilUsuarioModel
from django.core.files.images import get_image_dimensions

class perfilForm(forms.ModelForm):
   class Meta:
       model = perfilUsuarioModel
       fields = ['usuario', 'funcao', 'nivelAcesso', 'avatar']
   def clean_avatar(self):
       imagem = self.cleaned_data.get("avatar")
       if not imagem:
           raise forms.ValidationError("Sem imagem!")
       else:
           w, h = get_image_dimensions(imagem)
           if w > 300:
               raise forms.ValidationError("A imagem tem %i pixels de largura, o limite é de 300px" % w)
           if h > 300:
               raise forms.ValidationError("A imagem tem %i pixels de altura, o limite é de 300px" % h)
       return imagem



