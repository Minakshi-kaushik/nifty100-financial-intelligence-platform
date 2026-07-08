import unittest

from src.analytics.peer import compute_peer_percentiles


class TestPeer(unittest.TestCase):
    def test_peer_table(self):

        df = compute_peer_percentiles()

        self.assertGreater(len(df), 0)

        self.assertIn(
            "percentile_rank",
            df.columns,
        )

        self.assertTrue((df["percentile_rank"] >= 0).all())

        self.assertTrue((df["percentile_rank"] <= 100).all())


if __name__ == "__main__":
    unittest.main()
