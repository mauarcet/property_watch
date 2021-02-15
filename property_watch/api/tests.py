from django.test import TestCase
from api.models import Property, PropertyAmenity, PropertyDescription
from api.utils.normalizers import *


class PropertyTestCase(TestCase):
    def setUp(self):
        Property.objects.create(
            name="Casas en Venta en Farallón",
            price=1000000,
            street_name="Farallón",
            street_number="N/A",
            settlement="Jardines Del Pedregal",
            town="Alvaro Obregón",
            state="Mexico City",
            country="Mexico",
            size=1200,
            image="https://http2.mlstatic.com/S_835796-MLM44806521573_022021-I.jpg",
        )

    def test_property_created(self):
        """Property is created"""
        property = Property.objects.get(name="Casas en Venta en Farallón")
        self.assertEqual(property.id, 1)


class PropertyAmenityTestCase(TestCase):
    def setUp(self):
        property = Property.objects.create(
            name="Casas en Venta en Farallon",
            street_name="Farallon",
            street_number="N/A",
            settlement="Jardines Del Pedregal",
            town="Alvaro Obregón",
            state="Mexico City",
            country="Mexico",
            size=1200,
            price=1000000,
            image="https://http2.mlstatic.com/S_835796-MLM44806521573_022021-I.jpg",
        )
        PropertyAmenity.objects.create(property_id=property, name="Roof Top")

    def test_amenity_created(self):
        """Property is created"""
        property_amenity = PropertyAmenity.objects.get(pk=1)
        self.assertEqual(property_amenity.id, 1)
        self.assertEqual(property_amenity.name, "Roof Top")

class PropertyDescriptionTestCase(TestCase):
    def setUp(self):
        property = Property.objects.create(
            name="Casas en Venta en Farallon",
            street_name="Farallon",
            street_number="N/A",
            settlement="Jardines Del Pedregal",
            town="Alvaro Obregón",
            state="Mexico City",
            country="Mexico",
            size=1200,
            price=1000000,
            image="https://http2.mlstatic.com/S_835796-MLM44806521573_022021-I.jpg",
        )
        PropertyDescription.objects.create(property_id=property, text="This is a test of a property description")

    def test_description_created(self):
        """Property is created"""
        property_description  = PropertyDescription.objects.get(pk=1)
        self.assertEqual(property_description.id, 1)
        self.assertEqual(property_description.text, "This is a test of a property description")


class NormalizersTestCase(TestCase):
    def test_normalize_property_price(self):
        test_price = "$ 1,505,000"
        self.assertEqual(normalize_price(test_price), 1505000)

    def test_normalize_property_size(self):
        test_size = "85 m²"
        self.assertEqual(normalize_size(test_size), 85.0)

    def test_normalize_property_address(self):
        test_full_address = "Camino Real A Cuautlancingo 12, San Juan Cuautlancingo Centro, Cuautlancingo, Puebla"
        address_dict = {
            "street_name": "Camino Real A Cuautlancingo",
            "street_number": "12",
            "settlement": "San Juan Cuautlancingo Centro",
            "town": "Cuautlancingo",
            "state": "Puebla",
            "country": "Mexico",
        }
        self.assertDictEqual(normalize_address(test_full_address), address_dict)

    def test_normalize_property_address_without_number(self):
        test_full_address = "Camino Real A Cuautlancingo, San Juan Cuautlancingo Centro, Cuautlancingo, Puebla"
        address_dict = {
            "street_name": "Camino Real A Cuautlancingo",
            "street_number": "N/A",
            "settlement": "San Juan Cuautlancingo Centro",
            "town": "Cuautlancingo",
            "state": "Puebla",
            "country": "Mexico",
        }
        self.assertDictEqual(normalize_address(test_full_address), address_dict)

class PropertyFromScrapperTestCase(TestCase):
    def test_property_created_from_dirty_data(self):
        name="Casas en Venta en Cuatlancingo"
        price = "$ 1,505,000"
        full_address = "Camino Real A Cuautlancingo 12, San Juan Cuautlancingo Centro, Cuautlancingo, Puebla"
        size="85 m²"
        image="https://http2.mlstatic.com/S_892821-MLM44872984553_022021-I.jpg"

        norm_address = normalize_address(full_address)
        norm_price = normalize_price(price)
        norm_size = normalize_size(size)

        property = Property.objects.create(
            name=name,
            street_name=norm_address['street_name'],
            street_number=norm_address['street_number'],
            settlement=norm_address['settlement'],
            town=norm_address['town'],
            state=norm_address['state'],
            country=norm_address['country'],
            size=norm_size,
            price = norm_price,
            image="https://http2.mlstatic.com/S_835796-MLM44806521573_022021-I.jpg",
        )

        self.assertEqual(property.name, "Casas en Venta en Cuatlancingo")
        self.assertEqual(property.price, 1505000)
        self.assertEqual(property.size, 85.0)
        self.assertEqual(property.street_name, "Camino Real A Cuautlancingo")
        self.assertEqual(property.street_number, "12")
        self.assertEqual(property.settlement, "San Juan Cuautlancingo Centro")
        self.assertEqual(property.town, 'Cuautlancingo')
        self.assertEqual(property.state, 'Puebla')
        self.assertEqual(property.country, "Mexico")
        self.assertEqual(property.image, "https://http2.mlstatic.com/S_835796-MLM44806521573_022021-I.jpg")
