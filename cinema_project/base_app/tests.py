import unittest

from .models import Hall, Cinema


class SeatCreationTest(unittest.TestCase):
    def setUp(self):
        hall_obj = Hall(
            name="New Hall Unit Test",
            description="hall description",
            seat_capacity=20,
            cinema=Cinema.objects.get(pk=91)
        )
        hall_obj.save()

    def tearDown(self) -> None:
        Hall.objects.filter(name='New Hall Unit Test').delete()

    def test_seats_generated(self):
        new_hall = Hall.objects.get(name="New Hall Unit Test").seat_set.all()
        self.assertEqual(len(new_hall), 20, 'Ran tests for seat generation')
