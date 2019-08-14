from collections import Counter
from flask import request
from flask_restful import Resource

from libs.strings import gettext
from models.item import ItemModel
from models.order import OrderModel, ItemsInOrder
from schemas.order import OrderSchema

order_schema = OrderSchema()


class Order(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        items = []
        item_id_quantities = Counter(data["item_ids"])

        for _id, count in item_id_quantities.most_common():
            item = ItemModel.find_by_id(_id)
            if not item:
                return (
                    {
                        "message": gettext(
                            "order_item_by_id_not_found"
                        ).format(_id)
                    },
                    404,
                )

            items.append(ItemsInOrder(item_id=_id, quantity=count))

        order = OrderModel(items=items, status="pending")
        order.save_to_db()

        order.set_status("failed")
        order.charge_with_stripe(data["token"])
        order.set_status("complete")
        return order_schema.dump(order)
