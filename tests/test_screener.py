import unittest

from src.screener.engine import run_preset


class TestScreener(unittest.TestCase):
    def test_quality_compounder(self):

        df = run_preset("quality_compounder")

        self.assertGreater(len(df), 0)

        self.assertTrue((df["return_on_equity_pct"] >= 15).all())

        non_fin = df[df["broad_sector"] != "Financials"]

        self.assertTrue((non_fin["debt_to_equity"] <= 1).all())


if __name__ == "__main__":
    unittest.main()
