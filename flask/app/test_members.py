import logging
import unittest
import json
import uuid
from unittest.mock import patch

from members import create_member, member_is_valid, MemberAlreadyExistsError

# Matcher which returns true if member_id of the called_with object matches the
# expected id; using string comparison, since the UUID objects will not be
# identical.
class HasMemberIdMatcher:
    def __init__(self, expected_id):
        self.expected_id = expected_id

    def __eq__(self, actual):
        if "member_id" not in actual:
            return False
        return str(actual["member_id"]) == str(self.expected_id)

class TestDB(unittest.TestCase):
    @patch("db.find_member_by")
    def test_member_is_valid_when_found(self,
                                        mock_find_member_by):
        member_id = uuid.UUID('00000000-0000-0000-0000-000000000000')
        mock_find_member_by.return_value = {
            "member_id": member_id,
            "first_name": "John",
            "last_name": "Doe",
            "dob": "01/01/1970",
            "country": "US"
        }
        assert member_is_valid(member_id) is True

    @patch("db.find_member_by")
    def test_member_is_not_valid_when_not_found(self,
                                                mock_find_member_by):
        member_id = uuid.UUID('00000000-0000-0000-0000-000000000000')
        mock_find_member_by.return_value = None
        assert member_is_valid(member_id) is False

    @patch("db.insert_member")
    @patch("members.member_is_valid")
    def test_create_member_raises_when_member_exists(self,
                                                     mock_member_is_valid,
                                                     mock_insert_member):
        mock_insert_member.return_value = None
        mock_member_is_valid.return_value = True
        with self.assertRaises(MemberAlreadyExistsError):
            create_member("John", "Doe", "01/01/1970", "US")

    @patch("db.insert_member")
    @patch("members.member_is_valid")
    def test_create_member_raises_when_properties_missing(self,
                                                          mock_member_is_valid,
                                                          mock_insert_member):
        mock_insert_member.return_value = None
        mock_member_is_valid.return_value = False
        with self.assertRaises(ValueError):
            create_member("John", "Doe", "US")

    @patch("db.insert_member")
    @patch("members.member_is_valid")
    def test_create_member_adds_uuid_to_insert(self,
                                               mock_member_is_valid,
                                               mock_insert_member):
        mock_member_is_valid.return_value = False

        expected_id = uuid.uuid5(uuid.NAMESPACE_DNS, json.dumps({
            "first_name": "John",
            "last_name": "Doe",
            "dob": "01/01/1970",
            "country": "US"
        }));
        match_member_id = HasMemberIdMatcher(expected_id)

        member_id = create_member(
            first_name="John",
            last_name="Doe",
            dob="01/01/1970",
            country="US"
        )

        mock_insert_member.assert_called_with(match_member_id)

        # assert member id exists
        assert member_id is not None

if __name__ == '__main__':
    unittest.main()
