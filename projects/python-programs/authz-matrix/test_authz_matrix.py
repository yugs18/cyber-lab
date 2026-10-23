import unittest

from authz_matrix import EXPECTED_POLICY, is_allowed


class AuthorizationTests(unittest.TestCase):

    def test_all_permissions_match_policy(self):
        for role, actions in EXPECTED_POLICY.items():
            for action, expected in actions.items():
                with self.subTest(role=role, action=action):
                    self.assertEqual(
                        is_allowed(role, action, verbose=False),
                        expected,
                    )

    def test_user_can_read_own_profile(self):
        self.assertTrue(
            is_allowed("user", "read_own_profile", verbose=False)
        )

    def test_user_cannot_read_other_profiles(self):
        self.assertFalse(
            is_allowed("user", "read_other_profiles", verbose=False)
        )

    def test_user_cannot_delete_users(self):
        self.assertFalse(
            is_allowed("user", "delete_users", verbose=False)
        )

    def test_anonymous_cannot_update_profile(self):
        self.assertFalse(
            is_allowed("anonymous", "update_own_profile", verbose=False)
        )

    def test_unknown_role_is_denied(self):
        self.assertFalse(
            is_allowed("unknown", "delete_users", verbose=False)
        )

    def test_unknown_action_is_denied(self):
        self.assertFalse(
            is_allowed("user", "unknown_action", verbose=False)
        )


if __name__ == "__main__":
    unittest.main()