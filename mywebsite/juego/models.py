from django.db import models

class Player(models.Model):
    player_id = models.CharField(max_length=100, unique=True)  # ID único del jugador
    color = models.CharField(max_length=7)  # Color en formato hexadecimal (#RRGGBB)

    def __str__(self):
        return f"Player {self.player_id} - Color {self.color}"
