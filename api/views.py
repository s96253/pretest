from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.models import Order
from api.decorators import require_valid_token


@api_view(["POST"])
@require_valid_token
def import_order(request):
    data = request.data

    order_number = data.get("order_number")
    total_price = data.get("total_price")

    if order_number is None or total_price is None:
        return JsonResponse(
            {"detail": "Missing required fields: order_number, total_price"},
            status=400,
        )

    try:
        total_price_int = int(total_price)
        if total_price_int < 0:
            raise ValueError
    except (TypeError, ValueError):
        return JsonResponse({"detail": "total_price must be a non-negative integer"}, status=400)

    order, created = Order.objects.get_or_create(
        order_number=order_number,
        defaults={"total_price": total_price_int},
    )

    if not created:
        order.total_price = total_price_int
        order.save(update_fields=["total_price"])

    return JsonResponse(
        {
            "order_number": order.order_number,
            "total_price": order.total_price,
            "created_time": order.created_time.isoformat(),
        },
        status=201 if created else 200,
    )
