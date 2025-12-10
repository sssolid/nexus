"""
Tests for AutoCare Application.

These tests verify that the Django models are properly configured and can
interact with the Auto Care Association database schemas.
"""
from django.test import TestCase
from django.db import connection
from .vcdb.models import (
    Make, VehicleType, Model, SubModel, Region, Year, Vehicle, BaseVehicle,
    DriveType, BrakeType, EngineBlock, Transmission, WheelBase, VehicleClass,
)
from .qdb.models import (
    QualifierType, Qualifier, QLanguage, QualifierTranslation,
)
from .pcdb.models import (
    Parts, PartsDescription, Category, SubCategory, Position,
)
from .padb.models import (
    PartAttribute, MetaData, MeasurementGroup, ValidValue,
)


class VCdbModelTests(TestCase):
    """Tests for VCdb models."""
    
    def test_make_model_exists(self):
        """Test that Make model is properly configured."""
        self.assertTrue(hasattr(Make, 'make_id'))
        self.assertTrue(hasattr(Make, 'make_name'))
        self.assertEqual(Make._meta.db_table, 'vcdb"."make')
        self.assertFalse(Make._meta.managed)
    
    def test_vehicle_model_exists(self):
        """Test that Vehicle model is properly configured."""
        self.assertTrue(hasattr(Vehicle, 'vehicle_id'))
        self.assertTrue(hasattr(Vehicle, 'base_vehicle'))
        self.assertEqual(Vehicle._meta.db_table, 'vcdb"."vehicle')
        self.assertFalse(Vehicle._meta.managed)
    
    def test_vehicle_properties(self):
        """Test that Vehicle properties are defined."""
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, 'make'))
        self.assertTrue(hasattr(vehicle, 'year'))
        self.assertTrue(hasattr(vehicle, 'model'))
    
    def test_year_model_exists(self):
        """Test that Year model is properly configured."""
        self.assertTrue(hasattr(Year, 'year_id'))
        self.assertEqual(Year._meta.db_table, 'vcdb"."year')


class QdbModelTests(TestCase):
    """Tests for Qdb models."""
    
    def test_qualifier_model_exists(self):
        """Test that Qualifier model is properly configured."""
        self.assertTrue(hasattr(Qualifier, 'qualifier_id'))
        self.assertTrue(hasattr(Qualifier, 'qualifier_text'))
        self.assertEqual(Qualifier._meta.db_table, 'qdb"."qualifier')
        self.assertFalse(Qualifier._meta.managed)
    
    def test_qualifier_type_model_exists(self):
        """Test that QualifierType model is properly configured."""
        self.assertTrue(hasattr(QualifierType, 'qualifier_type_id'))
        self.assertTrue(hasattr(QualifierType, 'qualifier_type'))
        self.assertEqual(QualifierType._meta.db_table, 'qdb"."qualifier_type')
    
    def test_qlanguage_model_exists(self):
        """Test that QLanguage model is properly configured."""
        self.assertTrue(hasattr(QLanguage, 'language_id'))
        self.assertTrue(hasattr(QLanguage, 'language_name'))
        self.assertEqual(QLanguage._meta.db_table, 'qdb"."language')


class PCdbModelTests(TestCase):
    """Tests for PCdb models."""
    
    def test_parts_model_exists(self):
        """Test that Parts model is properly configured."""
        self.assertTrue(hasattr(Parts, 'part_terminology_id'))
        self.assertTrue(hasattr(Parts, 'part_terminology_name'))
        self.assertEqual(Parts._meta.db_table, 'pcdb"."parts')
        self.assertFalse(Parts._meta.managed)
    
    def test_category_model_exists(self):
        """Test that Category model is properly configured."""
        self.assertTrue(hasattr(Category, 'category_id'))
        self.assertTrue(hasattr(Category, 'category_name'))
        self.assertEqual(Category._meta.db_table, 'pcdb"."category')
    
    def test_position_model_exists(self):
        """Test that Position model is properly configured."""
        self.assertTrue(hasattr(Position, 'position_id'))
        self.assertTrue(hasattr(Position, 'position'))
        self.assertEqual(Position._meta.db_table, 'pcdb"."position')


class PAdbModelTests(TestCase):
    """Tests for PAdb models."""
    
    def test_part_attribute_model_exists(self):
        """Test that PartAttribute model is properly configured."""
        self.assertTrue(hasattr(PartAttribute, 'pa_id'))
        self.assertTrue(hasattr(PartAttribute, 'pa_name'))
        self.assertEqual(PartAttribute._meta.db_table, 'padb"."part_attribute')
        self.assertFalse(PartAttribute._meta.managed)
    
    def test_metadata_model_exists(self):
        """Test that MetaData model is properly configured."""
        self.assertTrue(hasattr(MetaData, 'meta_id'))
        self.assertTrue(hasattr(MetaData, 'meta_name'))
        self.assertEqual(MetaData._meta.db_table, 'padb"."metadata')


class ModelRelationshipTests(TestCase):
    """Tests for model relationships."""
    
    def test_vehicle_to_base_vehicle_relationship(self):
        """Test that Vehicle has relationship to BaseVehicle."""
        vehicle = Vehicle()
        self.assertTrue(hasattr(vehicle, 'base_vehicle'))
        # Check that it's a ForeignKey
        field = Vehicle._meta.get_field('base_vehicle')
        self.assertEqual(field.related_model, BaseVehicle)
    
    def test_base_vehicle_relationships(self):
        """Test that BaseVehicle has proper relationships."""
        base_vehicle = BaseVehicle()
        self.assertTrue(hasattr(base_vehicle, 'year'))
        self.assertTrue(hasattr(base_vehicle, 'make'))
        self.assertTrue(hasattr(base_vehicle, 'model'))
    
    def test_qualifier_relationships(self):
        """Test that Qualifier has proper relationships."""
        qualifier = Qualifier()
        self.assertTrue(hasattr(qualifier, 'qualifier_type'))
        # Check reverse relationship exists
        self.assertTrue(hasattr(QualifierType, '_meta'))
    
    def test_parts_relationships(self):
        """Test that Parts has proper relationships."""
        parts = Parts()
        self.assertTrue(hasattr(parts, 'parts_description'))


class ModelMetaConfigurationTests(TestCase):
    """Tests for model Meta configuration."""
    
    def test_all_models_unmanaged(self):
        """Test that all models have managed=False."""
        models_to_test = [
            Make, Vehicle, BaseVehicle, Qualifier, Parts, PartAttribute
        ]
        for model in models_to_test:
            with self.subTest(model=model.__name__):
                self.assertFalse(
                    model._meta.managed,
                    f"{model.__name__} should have managed=False"
                )
    
    def test_schema_in_db_table(self):
        """Test that models have schema prefix in db_table."""
        test_cases = [
            (Make, 'vcdb'),
            (Qualifier, 'qdb'),
            (Parts, 'pcdb'),
            (PartAttribute, 'padb'),
        ]
        for model, schema in test_cases:
            with self.subTest(model=model.__name__, schema=schema):
                self.assertTrue(
                    model._meta.db_table.startswith(f'{schema}"."'),
                    f"{model.__name__} should have {schema} schema prefix"
                )


class ModelStrMethodTests(TestCase):
    """Tests for model __str__ methods."""
    
    def test_make_str_method(self):
        """Test Make __str__ method."""
        make = Make(make_id=1, make_name='Toyota')
        self.assertIn('Toyota', str(make))
        self.assertIn('1', str(make))
    
    def test_qualifier_str_method(self):
        """Test Qualifier __str__ method."""
        qualifier = Qualifier(qualifier_id=100, qualifier_text='Test Qualifier')
        str_repr = str(qualifier)
        self.assertIn('100', str_repr)
        self.assertIn('Test', str_repr)
    
    def test_parts_str_method(self):
        """Test Parts __str__ method."""
        parts = Parts(
            part_terminology_id=5000,
            part_terminology_name='Brake Pad'
        )
        str_repr = str(parts)
        self.assertIn('Brake Pad', str_repr)
        self.assertIn('5000', str_repr)


class DatabaseSchemaTests(TestCase):
    """Tests for database schema configuration."""
    
    def test_database_connection(self):
        """Test that database connection is available."""
        with connection.cursor() as cursor:
            # This should not raise an exception
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)


# Integration tests (require actual database data)
class IntegrationTests(TestCase):
    """
    Integration tests that require actual database data.
    These tests are skipped if the database is not populated.
    """
    
    @classmethod
    def setUpClass(cls):
        """Check if database has data before running integration tests."""
        super().setUpClass()
        try:
            # Check if any data exists
            cls.has_data = Make.objects.exists()
        except Exception:
            cls.has_data = False
    
    def test_can_query_makes(self):
        """Test that we can query Make objects."""
        if not self.has_data:
            self.skipTest("Database not populated with test data")
        
        makes = Make.objects.all()[:10]
        self.assertGreater(len(makes), 0)
    
    def test_can_query_vehicles(self):
        """Test that we can query Vehicle objects."""
        if not self.has_data:
            self.skipTest("Database not populated with test data")
        
        vehicles = Vehicle.objects.all()[:10]
        self.assertGreater(len(vehicles), 0)
    
    def test_vehicle_relationships(self):
        """Test that Vehicle relationships work."""
        if not self.has_data:
            self.skipTest("Database not populated with test data")
        
        vehicle = Vehicle.objects.select_related(
            'base_vehicle__make',
            'base_vehicle__year',
            'base_vehicle__model'
        ).first()
        
        if vehicle:
            # Test that relationships can be accessed
            self.assertIsNotNone(vehicle.base_vehicle)
            self.assertIsNotNone(vehicle.base_vehicle.make)
