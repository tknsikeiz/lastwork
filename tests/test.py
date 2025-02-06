import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../source'))) 
import unittest
from unittest.mock import patch
from io import StringIO
import sys

from app import process_purchase, process_payment, reset_sales, products

class TestTicketVendingMachine(unittest.TestCase):

    def test_purchase(self):
        with patch('builtins.input', side_effect=['1', 'c', '1000']), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            total = process_purchase() 
            process_payment(total) 

            output = mock_stdout.getvalue()
            self.assertIn("合計1000円です。", output) 
            self.assertIn("ご購入ありがとうございます。おつり0円です。", output) 

    def test_invalid_purchase(self):
        with patch('builtins.input', side_effect=['5', 'c']), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            total = process_purchase()
            output = mock_stdout.getvalue()
            self.assertIn("商品番号またはcを指定してください。", output)  

    def test_reset_sales(self):
        with patch('builtins.input', side_effect=['1', '3']), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            reset_sales() 
            output = mock_stdout.getvalue()
            self.assertIn("売上をリセットしました。", output)  
            for product in products.values():
                self.assertEqual(product['sold'], 0) 
                self.assertEqual(product['revenue'], 0) 

    def test_change_price(self):
        with patch('builtins.input', side_effect=['2', '900', 'c', '1000']), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            product_id = 2
            new_price = 900
            products[product_id]["price"] = new_price  

            total = process_purchase()
            process_payment(total)

            output = mock_stdout.getvalue()
            self.assertIn(f"合計{new_price}円です。", output)  

    def test_purchase(self):
        with patch('builtins.input', side_effect=['2', '1', 'c', '2000']), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            total = process_purchase() 
            process_payment(total) 

            output = mock_stdout.getvalue()
            self.assertIn("合計2800円です。", output) 


    def test_reset_sales(self):
        with patch('builtins.input', side_effect=['1', '3']), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            reset_sales() 
            output = mock_stdout.getvalue()
            self.assertIn("売上をリセットしました。", output)  
            for product in products.values():
                self.assertEqual(product['sold'], 0) 
                self.assertEqual(product['revenue'], 0) 

if __name__ == '__main__':
    unittest.main()
