from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

def send_booking_confirmation_email(reservation):
    """Send booking confirmation email to the user"""
    try:
        subject = f"Confirmation de réservation #{reservation.id}"
        
        # Render HTML email template
        html_content = render_to_string('emails/booking_confirmation.html', {
            'reservation': reservation,
            'user': reservation.user,
        })
        
        # Create plain text version
        text_content = strip_tags(html_content)
        
        # Create email message
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[reservation.user.email]
        )
        
        # Attach HTML version
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send()
        
        logger.info(f"Booking confirmation email sent to {reservation.user.email} for reservation #{reservation.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send booking confirmation email: {str(e)}")
        return False

def send_payment_confirmation_email(payment):
    """Send payment confirmation email to the user"""
    try:
        reservation = payment.reservation
        subject = f"Confirmation de paiement - Réservation #{reservation.id}"
        
        # Simple text email for payment confirmation
        message = f"""
Bonjour {reservation.user.get_full_name()},

Votre paiement de {payment.amount}€ pour la réservation #{reservation.id} a été confirmé avec succès.

Détails de la transaction:
- Montant: {payment.amount}€
- Méthode: {payment.get_payment_method_display() if payment.payment_method else 'PayPal'}
- ID Transaction: {payment.transaction_id}
- Statut: {payment.get_status_display()}

Votre réservation est maintenant confirmée et votre véhicule vous attend!

Cordialement,
L'équipe Location de Voitures

---
Cet email a été envoyé automatiquement, merci de ne pas y répondre.
Pour toute question: support@location-voitures.com
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reservation.user.email],
            fail_silently=False,
        )
        
        logger.info(f"Payment confirmation email sent to {reservation.user.email} for payment #{payment.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send payment confirmation email: {str(e)}")
        return False

def send_reservation_status_update_email(reservation, old_status, new_status):
    """Send email when reservation status changes"""
    try:
        subject = f"Mise à jour de votre réservation #{reservation.id}"
        
        status_messages = {
            'confirmed': 'Votre réservation a été confirmée! Votre véhicule vous attend.',
            'cancelled': 'Votre réservation a été annulée. Si vous avez des questions, contactez-nous.',
            'completed': 'Votre location est terminée. Merci de votre confiance! N\'hésitez pas à laisser un avis.',
        }
        
        message = f"""
Bonjour {reservation.user.get_full_name()},

Le statut de votre réservation #{reservation.id} a été mis à jour.

Ancien statut: {old_status}
Nouveau statut: {new_status}

{status_messages.get(new_status, 'Votre réservation a été mise à jour.')}

Détails de la réservation:
- Véhicule: {reservation.car.brand} {reservation.car.model}
- Dates: du {reservation.start_date.strftime('%d/%m/%Y')} au {reservation.end_date.strftime('%d/%m/%Y')}
- Montant total: {reservation.total_price}€

Pour consulter vos réservations: http://localhost:8000/profile/

Cordialement,
L'équipe Location de Voitures

---
Pour toute question: support@location-voitures.com
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reservation.user.email],
            fail_silently=False,
        )
        
        logger.info(f"Status update email sent to {reservation.user.email} for reservation #{reservation.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send status update email: {str(e)}")
        return False

def send_contact_response_email(contact):
    """Send email response to contact form submission"""
    try:
        subject = f"Réponse à votre message: {contact.subject}"
        
        message = f"""
Bonjour {contact.name},

Merci de nous avoir contactés. Voici notre réponse à votre message:

Votre message:
"{contact.message}"

Notre réponse:
{contact.admin_response if contact.admin_response else "Nous avons bien reçu votre message et vous répondrons dans les plus brefs délais."}

Si vous avez d'autres questions, n'hésitez pas à nous recontacter.

Cordialement,
L'équipe Location de Voitures

---
Email: support@location-voitures.com
Téléphone: +33 1 23 45 67 89
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact.email],
            fail_silently=False,
        )
        
        logger.info(f"Contact response email sent to {contact.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send contact response email: {str(e)}")
        return False