from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AppTokenGenerator(PasswordResetTokenGenerator):
    
    def _make_hash_values(self, user, timestamp):
        # Crée la chaîne de caractères unique à partir de l'utilisateur et du timestamp
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)

# Créer une instance du générateur de token
account_activation_token = AppTokenGenerator()
