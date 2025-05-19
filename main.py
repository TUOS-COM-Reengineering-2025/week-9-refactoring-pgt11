class CustomerManager:
    def __init__(self):
        self.customers = {}
        self.tax_rate = 0.2
        self.tax_threshold = 100
        self.discount_threshold = 500

    def add_customer(self, name, purchases):
        if name in self.customers:
            self.customers[name].extend(purchases)
        else:
            self.customers[name] = purchases

    def add_purchase(self, name, purchase):
        self.add_customer(name, [purchase])

    def add_purchases(self, name, purchases):
        self.add_customer(name, purchases)

    def _calculate_total_with_tax(self, purchases):
        total = 0
        for item in purchases:
            price = item['price']
            if price > self.tax_threshold:
                total += price * (1 + self.tax_rate)
            else:
                total += price
        return total

    def _get_discount_label(self, total):
        if total > self.discount_threshold:
            return "Eligible for discount"
        elif total > 300:
            return "Potential future discount customer"
        else:
            return "No discount"

    def _get_priority_label(self, total):
        if total > 1000:
            return "VIP Customer!"
        elif total > 800:
            return "Priority Customer"
        return None

    def generate_report(self):
        for customer_name, purchases in self.customers.items():
            total = self._calculate_total_with_tax(purchases)
            print(customer_name)
            print(self._get_discount_label(total))
            priority = self._get_priority_label(total)
            if priority:
                print(priority)

    def calculate_shipping_fee(self, purchases):
        for purchase in purchases:
            if purchase.get('weight', 0) > 20:
                return 50
        return 20


def calculate_shipping_fee_for_heavy_items(purchases):
    for purchase in purchases:
        if purchase.get('weight', 0) > 20:
            return 50
    return 20


def calculate_shipping_fee_for_fragile_items(purchases):
    for purchase in purchases:
        if purchase.get('fragile', False):
            return 60
    return 25


flat_tax = 0.2
