from django.test import TestCase

# Create your tests here.
def form(request):
	return render(request, "test.html", {})

def create_transaction(request):
	 result = braintree.Transaction.sale({
        "amount": "1000.00",
        "credit_card": {
            "number": request.form["number"],
            "cvv": request.form["cvv"],
            "expiration_month": request.form["month"],
            "expiration_year": request.form["year"]
        },
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success:
        return "<h1>Success! Transaction ID: {0}</h1>".format(result.transaction.id)
    else:
        return "<h1>Error: {0}</h1>".format(result.message)