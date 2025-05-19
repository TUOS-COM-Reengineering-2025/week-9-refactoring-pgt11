import unittest
import io
import contextlib

from main import CustomerManager, calculate_shipping_fee_for_fragile_items
from main import calculate_shipping_fee_for_heavy_items

class TestCustomerManager(unittest.TestCase):

    def test_add_customer(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_customer(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_add_purchase(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase]},
            cm.customers
        )

    def test_add_purchase_multiple(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase, purchase]},
            cm.customers
        )

    def test_discount_eligibility(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 600}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("Eligible for discount", output)

    def test_heavy_item_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 100, 'weight': 25}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 50)

    def test_fragile_item_shipping_fee(self):
        purchases = [{'price': 70, 'fragile': True}]

        fee = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee, 60)

    def test_no_special_items_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 40, 'weight': 5, 'fragile': False}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 20)

        fee_fragile = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee_fragile, 25)
        
    def test_potential_discount_customer(self):
        cm = CustomerManager()
        cm.add_customer("Tom", [{'price': 400}])
        with contextlib.redirect_stdout(io.StringIO()) as f:
            cm.generate_report()
        self.assertIn("Potential future discount customer", f.getvalue())

    def test_add_purchases_method(self):
        cm = CustomerManager()
        name = "TestUser"
        purchases = [{'price': 50}, {'price': 70}]
        cm.add_purchases(name, purchases)
        self.assertEqual(cm.customers[name], purchases)

    def test_tax_threshold_logic(self):
        cm = CustomerManager()
        cm.tax_threshold = 100
        cm.tax_rate = 0.2
        purchases = [{'price': 80}, {'price': 150}]
        total = cm._calculate_total_with_tax(purchases)
        expected = 80 + (150 * 1.2)
        self.assertAlmostEqual(total, expected)

    def test_priority_customer_label(self):
        cm = CustomerManager()
        self.assertEqual(cm._get_priority_label(1200), "VIP Customer!")
        self.assertEqual(cm._get_priority_label(850), "Priority Customer")
        self.assertIsNone(cm._get_priority_label(700))

    def test_priority_label_printed(self):
        cm = CustomerManager()
        cm.tax_threshold = 100
        cm.tax_rate = 0.2
        purchases = [{'price': 500}, {'price': 300}]  # total = 500 + 300*1.2 = 860
        cm.add_customer("RichGuy", purchases)
        with contextlib.redirect_stdout(io.StringIO()) as f:
            cm.generate_report()
        output = f.getvalue()
        self.assertIn("Priority Customer", output)


    def test_vip_label_printed(self):
        cm = CustomerManager()
        cm.add_customer("VIP", [{'price': 1100}])
        with contextlib.redirect_stdout(io.StringIO()) as f:
            cm.generate_report()
        output = f.getvalue()
        self.assertIn("VIP Customer!", output)

    def test_calculate_shipping_fee_for_heavy_items(self):
        heavy = [{'price': 100, 'weight': 25}]
        light = [{'price': 100, 'weight': 5}]
    
        self.assertEqual(calculate_shipping_fee_for_heavy_items(heavy), 50)
        self.assertEqual(calculate_shipping_fee_for_heavy_items(light), 20)
    def test_no_discount_label_printed(self):
        cm = CustomerManager()
        cm.add_customer("CheapCustomer", [{'price': 100}, {'price': 150}])  # total = 250
        with contextlib.redirect_stdout(io.StringIO()) as f:
            cm.generate_report()
        output = f.getvalue()
        self.assertIn("No discount", output)







if __name__ == "__main__":
    unittest.main()
