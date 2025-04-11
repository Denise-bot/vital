from secrets import token_urlsafe
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils import timezone
from datetime import timedelta

class TiposExames(models.Model):
    tipo_choices = (
        ('I', 'Exame de imagem'),
        ('S', 'Exame de Sangue')
    )
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    horario_inicial = models.IntegerField()
    horario_final = models.IntegerField()

    def __str__(self):
        return self.nome
    
class SolicitacaoExame(models.Model):
    choice_status = (
        ('E', 'Em análise'),
        ('F', 'Finalizado')
    )
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exame = models.ForeignKey(TiposExames, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=choice_status)
    resultado = models.FileField(upload_to="resultados", null=True, blank=True)
    requer_senha = models.BooleanField(default=False)
    senha = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f'{self.usuario} | {self.exame.nome}'

class PedidosExames(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exames = models.ManyToManyField(SolicitacaoExame)
    agendado = models.BooleanField(default=True)
    data = models.DateField()

    def __str__(self):
        return f'{self.usuario} | {self.data}'

class Exame(models.Model):
    nome = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=[('E', 'Em análise'), ('F', 'Finalizado')])

    def badge_template(self):
        if self.status == 'E':
            classes_css = 'bg-warning text-dark'
            texto = "Em análise"
        elif self.status == 'F':
            classes_css = 'bg-success'
            texto = "Finalizado"
        else:
            # Caso o status não seja 'E' nem 'F'
            classes_css = 'bg-secondary'  # Pode ser uma classe padrão
            texto = "Status desconhecido"
        
        return mark_safe(f"<span class='badge {classes_css}'>{texto}</span>")
    
class AcessoMedico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    identificacao = models.CharField(max_length=50)
    tempo_de_acesso = models.IntegerField() # Em horas
    criado_em = models.DateTimeField()
    data_exames_iniciais = models.DateField()
    data_exames_finais = models.DateField()
    token = models.CharField(max_length=20)

    def __str__(self):
        return self.token
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(6)

        super(AcessoMedico, self).save(*args, **kwargs)
   
    @property
    def status(self):
        return 'Expirado' if timezone.now() > (self.criado_em + timedelta(hours=self.tempo_de_acesso)) else 'Ativo'
  
    @property
    def url(self):
    #TODO: reverse
        return f"http://127.0.0.1:8000/exames/acesso_medico/{self.token}"
    