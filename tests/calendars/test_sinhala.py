#  holidays
#  --------
#  A fast, efficient Python library for generating country, province and state
#  specific sets of holidays on the fly. It aims to make determining whether a
#  specific date is a holiday as fast and flexible as possible.
#
#  Authors: Vacanza Team and individual contributors (see CONTRIBUTORS file)
#           dr-prodigy <dr.prodigy.github@gmail.com> (c) 2017-2023
#           ryanss <ryanssdev@icloud.com> (c) 2014-2017
#  Website: https://github.com/vacanza/holidays
#  License: MIT (see LICENSE file)

import unittest
from datetime import date

from holidays import calendars
from holidays.calendars.gregorian import (
    JAN,
    FEB,
    MAR,
    APR,
    MAY,
    JUN,
    JUL,
    AUG,
    SEP,
    OCT,
    NOV,
    DEC,
)


class TestSinhalaLunarCalendar(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.calendar = calendars._SinhalaLunar()

    # ------------------------------------------------------------------ #
    # Boundary conditions
    # ------------------------------------------------------------------ #

    def test_range_constants(self):
        self.assertEqual(self.calendar.START_YEAR, 2003)
        self.assertEqual(self.calendar.CONFIRMED_YEAR, 2026)
        self.assertEqual(self.calendar.END_YEAR, 2052)

    def test_out_of_range_returns_none(self):
        """Years outside [START_YEAR, END_YEAR] must return (None, True) - no date, any flag."""
        before = self.calendar.START_YEAR - 1
        after = self.calendar.END_YEAR + 1

        for method in (
            self.calendar.bak_poya_date,
            self.calendar.binara_poya_date,
            self.calendar.esala_poya_date,
            self.calendar.il_poya_date,
            self.calendar.medin_poya_date,
            self.calendar.nawam_poya_date,
            self.calendar.nikini_poya_date,
            self.calendar.poson_poya_date,
            self.calendar.unduvap_poya_date,
            self.calendar.vap_poya_date,
            self.calendar.vesak_poya_date,
        ):
            with self.subTest(method=method.__name__, year=before):
                dt, _ = method(before)
                self.assertIsNone(dt)
            with self.subTest(method=method.__name__, year=after):
                dt, _ = method(after)
                self.assertIsNone(dt)

        # Duruthu returns an iterable; out-of-range -> empty
        self.assertEqual(list(self.calendar.duruthu_poya_date(before)), [])
        self.assertEqual(list(self.calendar.duruthu_poya_date(after)), [])

    # ------------------------------------------------------------------ #
    # Confirmed dates (2003-2026) - estimated flag must be False
    # ------------------------------------------------------------------ #

    def test_vesak_poya_confirmed(self):
        confirmed = {
            2003: date(2003, MAY, 15),
            2006: date(2006, MAY, 12),
            2010: date(2010, MAY, 27),
            2015: date(2015, MAY, 3),
            2018: date(2018, APR, 29),
            2022: date(2022, MAY, 15),
            2024: date(2024, MAY, 23),
            2025: date(2025, MAY, 12),
            2026: date(2026, MAY, 1),
        }
        for year, expected_date in confirmed.items():
            with self.subTest(year=year):
                dt, estimated = self.calendar.vesak_poya_date(year)
                self.assertEqual(dt, expected_date)
                self.assertFalse(estimated, f"{year} should not be estimated")

    def test_poson_poya_confirmed(self):
        confirmed = {
            2003: date(2003, JUN, 14),
            2010: date(2010, JUN, 25),
            2022: date(2022, JUN, 14),
            2026: date(2026, JUN, 29),
        }
        for year, expected_date in confirmed.items():
            with self.subTest(year=year):
                dt, estimated = self.calendar.poson_poya_date(year)
                self.assertEqual(dt, expected_date)
                self.assertFalse(estimated)

    def test_nawam_poya_confirmed(self):
        confirmed = {
            2003: date(2003, FEB, 16),
            2015: date(2015, FEB, 3),
            2023: date(2023, FEB, 5),
            2026: date(2026, FEB, 1),
        }
        for year, expected_date in confirmed.items():
            with self.subTest(year=year):
                dt, estimated = self.calendar.nawam_poya_date(year)
                self.assertEqual(dt, expected_date)
                self.assertFalse(estimated)

    def test_bak_poya_confirmed(self):
        confirmed = {
            2010: date(2010, MAR, 29),
            2020: date(2020, APR, 7),
            2026: date(2026, APR, 1),
        }
        for year, expected_date in confirmed.items():
            with self.subTest(year=year):
                dt, estimated = self.calendar.bak_poya_date(year)
                self.assertEqual(dt, expected_date)
                self.assertFalse(estimated)

    def test_esala_poya_confirmed(self):
        confirmed = {
            2020: date(2020, JUL, 4),
            2023: date(2023, AUG, 1),
            2026: date(2026, JUL, 29),
        }
        for year, expected_date in confirmed.items():
            with self.subTest(year=year):
                dt, estimated = self.calendar.esala_poya_date(year)
                self.assertEqual(dt, expected_date)
                self.assertFalse(estimated)

    def test_nikini_poya_confirmed(self):
        confirmed = {
            2003: date(2003, AUG, 11),
            2020: date(2020, AUG, 3),
            2026: date(2026, AUG, 27),
        }
        for year, expected_date in confirmed.items():
            with self.subTest(year=year):
                dt, estimated = self.calendar.nikini_poya_date(year)
                self.assertEqual(dt, expected_date)
                self.assertFalse(estimated)

    def test_binara_poya_confirmed(self):
        confirmed = {
            2020: date(2020, SEP, 1),
            2026: date(2026, SEP, 26),
        }
        for year, expected_date in confirmed.items():
            with self.subTest(year=year):
                dt, estimated = self.calendar.binara_poya_date(year)
                self.assertEqual(dt, expected_date)
                self.assertFalse(estimated)

    def test_vap_poya_confirmed(self):
        confirmed = {
            2003: date(2003, OCT, 9),
            2020: date(2020, OCT, 30),
            2026: date(2026, OCT, 25),
        }
        for year, expected_date in confirmed.items():
            with self.subTest(year=year):
                dt, estimated = self.calendar.vap_poya_date(year)
                self.assertEqual(dt, expected_date)
                self.assertFalse(estimated)

    def test_il_poya_confirmed(self):
        confirmed = {
            2003: date(2003, NOV, 8),
            2020: date(2020, NOV, 29),
            2026: date(2026, NOV, 24),
        }
        for year, expected_date in confirmed.items():
            with self.subTest(year=year):
                dt, estimated = self.calendar.il_poya_date(year)
                self.assertEqual(dt, expected_date)
                self.assertFalse(estimated)

    def test_unduvap_poya_confirmed(self):
        confirmed = {
            2003: date(2003, DEC, 8),
            2020: date(2020, DEC, 29),
            2026: date(2026, DEC, 23),
        }
        for year, expected_date in confirmed.items():
            with self.subTest(year=year):
                dt, estimated = self.calendar.unduvap_poya_date(year)
                self.assertEqual(dt, expected_date)
                self.assertFalse(estimated)

    def test_medin_poya_confirmed(self):
        confirmed = {
            2003: date(2003, MAR, 18),
            2020: date(2020, MAR, 9),
            2026: date(2026, MAR, 2),
        }
        for year, expected_date in confirmed.items():
            with self.subTest(year=year):
                dt, estimated = self.calendar.medin_poya_date(year)
                self.assertEqual(dt, expected_date)
                self.assertFalse(estimated)

    # ------------------------------------------------------------------ #
    # Duruthu (set method - may return 1 or 2 entries)
    # ------------------------------------------------------------------ #

    def test_duruthu_poya_confirmed(self):
        """Confirmed single-year Duruthu lookups must contain the correct date, not estimated."""
        # duruthu_poya_date(year) looks at (year-1, year) - we check the primary entry
        confirmed = {
            # (year arg, expected date in that result set)
            2011: date(2011, JAN, 19),
            2022: date(2022, JAN, 17),
            2025: date(2025, JAN, 13),
        }
        for year, expected_date in confirmed.items():
            with self.subTest(year=year):
                entries = list(self.calendar.duruthu_poya_date(year))
                dates = [e[0] for e in entries]
                self.assertIn(expected_date, dates)
                for _, estimated in entries:
                    self.assertFalse(estimated)

    def test_duruthu_poya_double_2009(self):
        """
        2009 is a known multi-Duruthu year.
        duruthu_poya_date(2009) looks at (2008, 2009):
        - DURUTHU_POYA_DATES[2008] has multiple entries (Jan 22 2008 + Dec entries)
        - DURUTHU_POYA_DATES[2009] has Jan 10 2009 + Dec 31 2009
        Result is 3 entries total.
        """
        entries = list(self.calendar.duruthu_poya_date(2009))
        self.assertEqual(len(entries), 3)
        dates = [e[0] for e in entries]
        self.assertIn(date(2009, JAN, 10), dates)
        self.assertIn(date(2009, DEC, 31), dates)
        for _, estimated in entries:
            self.assertFalse(estimated)

    def test_duruthu_poya_double_2028(self):
        """
        2028 produces 3 Duruthu entries (all estimated):
        duruthu_poya_date(2028) looks at (2027, 2028).
        """
        entries = list(self.calendar.duruthu_poya_date(2028))
        self.assertEqual(len(entries), 3)
        dates = [e[0] for e in entries]
        self.assertIn(date(2028, JAN, 11), dates)
        self.assertIn(date(2028, DEC, 31), dates)
        for _, estimated in entries:
            self.assertTrue(estimated)

    # ------------------------------------------------------------------ #
    # Estimated dates (2027-2052) - flag must be True
    # ------------------------------------------------------------------ #

    def test_estimated_flag_future_years(self):
        """All single-date methods for 2027+ must return estimated=True."""
        for year in (2027, 2030, 2040, 2052):
            with self.subTest(year=year):
                for method in (
                    self.calendar.bak_poya_date,
                    self.calendar.binara_poya_date,
                    self.calendar.esala_poya_date,
                    self.calendar.il_poya_date,
                    self.calendar.medin_poya_date,
                    self.calendar.nawam_poya_date,
                    self.calendar.nikini_poya_date,
                    self.calendar.poson_poya_date,
                    self.calendar.unduvap_poya_date,
                    self.calendar.vap_poya_date,
                    self.calendar.vesak_poya_date,
                ):
                    dt, estimated = method(year)
                    self.assertIsNotNone(dt, f"{method.__name__}({year}) returned None")
                    self.assertTrue(estimated, f"{method.__name__}({year}) must be estimated")

                for dt, estimated in self.calendar.duruthu_poya_date(year):
                    # duruthu_poya_date spans (year-1, year), so the first entry
                    # may come from CONFIRMED_YEAR and have estimated=False.
                    # Only check that dates in the estimated range are flagged.
                    if dt.year > self.calendar.CONFIRMED_YEAR:
                        self.assertTrue(
                            estimated,
                            f"duruthu_poya_date({year}): {dt} must be estimated",
                        )

    def test_estimated_spot_checks(self):
        """
        Spot-check future astronomical dates from the generator.
        Best-effort (~80% accuracy, +-1 day); may diverge from official gazettes.
        """
        spot_checks = [
            (2027, self.calendar.vesak_poya_date, date(2027, MAY, 20)),
            (2027, self.calendar.poson_poya_date, date(2027, JUN, 18)),
            (2030, self.calendar.vesak_poya_date, date(2030, MAY, 17)),
            (2052, self.calendar.vesak_poya_date, date(2052, MAY, 13)),
            (2052, self.calendar.binara_poya_date, date(2052, SEP, 8)),
        ]
        for year, method, expected in spot_checks:
            with self.subTest(year=year, method=method.__name__):
                dt, estimated = method(year)
                self.assertEqual(dt, expected)
                self.assertTrue(estimated)


if __name__ == "__main__":
    unittest.main()
