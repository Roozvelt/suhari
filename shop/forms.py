from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_type', 'address', 'payment_type']
        widgets = {
            'payment_type': forms.RadioSelect(choices=[
                ('card', 'Оплата картой онлайн'),
                ('cash', 'Наличными при получении')
            ])
        }

    def clean(self):
        cleaned_data = super().clean()
        delivery_type = cleaned_data.get('delivery_type')
        address = cleaned_data.get('address')
        if delivery_type == 'delivery' and not address:
            self.add_error('address', 'Введите адрес доставки')
        return cleaned_data

class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }