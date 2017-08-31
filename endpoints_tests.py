import unittest
import endpoints

class TestMethods(unittest.TestCase):

    def test_time_calc(self):
        self.assertEqual(endpoints.time_elapsed_calculator(2017, 7, 12, 2017, 7, 16).days, 4)
        self.assertEqual(endpoints.time_elapsed_calculator(2017, 7, 12, 2017, 8, 12).days, 31)
        self.assertEqual(endpoints.time_elapsed_calculator(2016, 7, 12, 2017, 7, 12).days, 365)

    def test_email_validation(self):
        self.assertTrue(endpoints.is_valid_email_address('testuser@gmail.com')['is_valid'])
        self.assertFalse(endpoints.is_valid_email_address('testuseratgmail.com')['is_valid'])
        self.assertFalse(endpoints.is_valid_email_address('@gmail.com')['is_valid'])
        self.assertFalse(endpoints.is_valid_email_address('testuser@gmailcom')['is_valid'])

    def test_temp_converter(self):
        self.assertEqual(endpoints.temperature_converter(-112.5, 'celcius', 'celcius')['result'], -112.5)
        self.assertEqual(endpoints.temperature_converter(45.8, 'celcius', 'kelvin')['result'], 318.95)
        self.assertEqual(round(endpoints.temperature_converter(100.22, 'celcius', 'fahrenheit')['result'], 3), 212.396)
        self.assertEqual(endpoints.temperature_converter(-112.5, 'kelvin', 'celcius')['result'], -385.65)
        self.assertEqual(endpoints.temperature_converter(45.8, 'kelvin', 'kelvin')['result'], 45.8)
        self.assertEqual(round(endpoints.temperature_converter(100.22, 'kelvin', 'fahrenheit')['result'], 3), -279.274)
        self.assertEqual(round(endpoints.temperature_converter(-112.5, 'fahrenheit', 'celcius')['result'], 6), -80.277778)
        self.assertEqual(round(endpoints.temperature_converter(45.8, 'fahrenheit', 'kelvin')['result'], 4), 280.8167)
        self.assertEqual(round(endpoints.temperature_converter(100.22, 'fahrenheit', 'fahrenheit')['result'], 2), 100.22)

    def test_length_converter(self):
        self.assertEqual(round(endpoints.length_converter(12.88, 'mm', 'ft')['result'], 9), 0.042257218)
        self.assertEqual(round(endpoints.length_converter(-88.88, 'yd', 'mi')['result'], 4), -0.0505)
        self.assertEqual(endpoints.length_converter(12.88, 'km', 'cm')['result'], 1288000)
        self.assertEqual(round(endpoints.length_converter(-88.88, 'inch', 'mi')['result'], 10), -0.0014027778)
        self.assertEqual(endpoints.length_converter(-88.88, 'km', 'm')['result'], -88880)

    def test_mass_converter(self):
        self.assertEqual(endpoints.mass_converter(1200, 'microgram', 'gram')['result'], 0.0012)
        self.assertEqual(endpoints.mass_converter(1200, 'milligram', 'gram')['result'], 1.2)
        self.assertEqual(endpoints.mass_converter(1200, 'gram', 'gram')['result'], 1200)
        self.assertEqual(endpoints.mass_converter(1200, 'kilogram', 'gram')['result'], 1200000.0)
        self.assertEqual(endpoints.mass_converter(.012, 'metric_ton', 'gram')['result'], 12000.0)
        self.assertEqual(round(endpoints.mass_converter(.003, 'us_ton', 'gram')['result'], 3), 2721.554)
        self.assertEqual(round(endpoints.mass_converter(.003, 'imperial_ton', 'gram')['result'], 3), 3048.141)
        self.assertEqual(round(endpoints.mass_converter(.003, 'stone', 'gram')['result'], 5), 19.05088)
        self.assertEqual(round(endpoints.mass_converter(.003, 'pound', 'gram')['result'], 7), 1.3607771)
        self.assertEqual(round(endpoints.mass_converter(1, 'ounce', 'gram')['result'], 4), 28.3495)
        self.assertEqual(endpoints.mass_converter(.12, 'gram', 'microgram')['result'], 120000)
        self.assertEqual(endpoints.mass_converter(.12, 'gram', 'milligram')['result'], 120)
        self.assertEqual(endpoints.mass_converter(1200, 'gram', 'gram')['result'], 1200)
        self.assertEqual(endpoints.mass_converter(1200, 'gram', 'kilogram')['result'], 1.2)
        self.assertEqual(endpoints.mass_converter(12000, 'gram', 'metric_ton')['result'], 0.012)
        self.assertEqual(round(endpoints.mass_converter(120000, 'gram', 'us_ton')['result'], 9), 0.132277357)
        self.assertEqual(round(endpoints.mass_converter(12000, 'gram', 'imperial_ton')['result'], 9), 0.011810478)
        self.assertEqual(round(endpoints.mass_converter(12000, 'gram', 'stone')['result'], 7), 1.8896765)
        self.assertEqual(round(endpoints.mass_converter(12000, 'gram', 'pound')['result'], 6), 26.455471)
        self.assertEqual(round(endpoints.mass_converter(120, 'gram', 'ounce')['result'], 5), 4.23288)
        self.assertEqual(round(endpoints.mass_converter(6.88, 'ounce', 'us_ton')['result'], 6), 0.000215)

    def test_day_of_week_calculator(self):
        self.assertEqual(endpoints.weekday_calculator(2017, 8, 23), 'Wednesday')
        self.assertEqual(endpoints.weekday_calculator(2017, 8, 24), 'Thursday')


if __name__ == '__main__':
    unittest.main()
