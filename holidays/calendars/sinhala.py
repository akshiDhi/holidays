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

from collections.abc import Iterable
from datetime import date

from holidays.calendars.custom import _CustomCalendar
from holidays.calendars.gregorian import JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC
from holidays.helpers import _normalize_tuple

BAK_POYA = "BAK_POYA"
BINARA_POYA = "BINARA_POYA"
DURUTHU_POYA = "DURUTHU_POYA"
ESALA_POYA = "ESALA_POYA"
IL_POYA = "IL_POYA"
MEDIN_POYA = "MEDIN_POYA"
NAWAM_POYA = "NAWAM_POYA"
NIKINI_POYA = "NIKINI_POYA"
POSON_POYA = "POSON_POYA"
UNDUVAP_POYA = "UNDUVAP_POYA"
VAP_POYA = "VAP_POYA"
VESAK_POYA = "VESAK_POYA"


class _SinhalaLunar:
    """
    Sinhala Lunar calendar for 2003-2052.

    Their Buddhist Uposatha day calculation method is different from Thai LuniSolar
    and Buddhist (Mahayana) used in East Asia.

    Due to the fact that Poya (Uposatha) days are calculated astronomically
    based on how close a particular day is closest to full moon at noon, and that
    an extra month is added every 33 months interval, this is hardcoded for now.

    Dates for 2003-2026 are taken from the official Sri Lanka Government Gazette
    and are exact.  Dates for 2027-2052 are estimated using the "noon rule"
    (Skyfield + de421.bsp, Lahiri ayanamsha) and may differ from the official
    gazette by at most 1 day in approximately 20% of cases.  They are tagged
    as estimated via the library's standard estimated_label mechanism.

    Adhi month dates are instead hardcoded in Sri Lanka country implementation.

    To regenerate 2027-2052 entries run:
        python -m scripts.calendar.sinhala_generator
    """

    START_YEAR = 2003
    # Last year for which Poya dates have been officially confirmed from the
    # Sri Lanka Government Gazette.  Dates from START_YEAR through CONFIRMED_YEAR
    # are exact; dates from CONFIRMED_YEAR+1 through END_YEAR are estimated.
    CONFIRMED_YEAR = 2026
    END_YEAR = 2052

    BAK_POYA_DATES = {
        2003: (APR, 16),
        2004: (APR, 5),
        2005: (APR, 23),
        2006: (APR, 13),
        2007: (APR, 2),
        2008: (APR, 19),
        2009: (APR, 9),
        2010: (MAR, 29),
        2011: (APR, 17),
        2012: (APR, 6),
        2013: (APR, 25),
        2014: (APR, 14),
        2015: (APR, 3),
        2016: (APR, 21),
        2017: (APR, 10),
        2018: (MAR, 31),
        2019: (APR, 19),
        2020: (APR, 7),
        2021: (APR, 26),
        2022: (APR, 16),
        2023: (APR, 5),
        2024: (APR, 23),
        2025: (APR, 12),
        2026: (APR, 1),
        # 2027-2052: astronomical estimates (noon rule, ~80% accuracy, ±1 day)
        2027: (APR, 20),
        2028: (APR, 9),
        2029: (MAR, 29),
        2030: (APR, 17),
        2031: (APR, 7),
        2032: (APR, 25),
        2033: (APR, 14),
        2034: (APR, 3),
        2035: (APR, 22),
        2036: (APR, 10),
        2037: (MAR, 31),
        2038: (APR, 19),
        2039: (APR, 8),
        2040: (APR, 26),
        2041: (APR, 16),
        2042: (APR, 5),
        2043: (APR, 24),
        2044: (APR, 12),
        2045: (APR, 1),
        2046: (APR, 20),
        2047: (APR, 10),
        2048: (MAR, 29),
        2049: (APR, 17),
        2050: (APR, 7),
        2051: (APR, 25),
        2052: (APR, 13),
    }

    BINARA_POYA_DATES = {
        2003: (SEP, 10),
        2004: (SEP, 28),
        2005: (SEP, 17),
        2006: (SEP, 7),
        2007: (SEP, 26),
        2008: (SEP, 14),
        2009: (SEP, 4),
        2010: (SEP, 22),
        2011: (SEP, 11),
        2012: (SEP, 29),
        2013: (SEP, 19),
        2014: (SEP, 8),
        2015: (SEP, 27),
        2016: (SEP, 16),
        2017: (SEP, 5),
        2018: (SEP, 24),
        2019: (SEP, 13),
        2020: (SEP, 1),
        2021: (SEP, 20),
        2022: (SEP, 10),
        2023: (SEP, 29),
        2024: (SEP, 17),
        2025: (SEP, 7),
        2026: (SEP, 26),
        # 2027-2052: astronomical estimates (noon rule, ~80% accuracy, ±1 day)
        2027: (SEP, 15),
        2028: (SEP, 3),
        2029: (SEP, 22),
        2030: (SEP, 11),
        2031: (SEP, 1),
        2032: (SEP, 19),
        2033: (SEP, 8),
        2034: (SEP, 27),
        2035: (SEP, 17),
        2036: (SEP, 5),
        2037: (SEP, 24),
        2038: (SEP, 13),
        2039: (SEP, 2),
        2040: (SEP, 20),
        2041: (SEP, 10),
        2042: (SEP, 29),
        2043: (SEP, 18),
        2044: (SEP, 7),
        2045: (SEP, 25),
        2046: (SEP, 15),
        2047: (SEP, 4),
        2048: (SEP, 21),
        2049: (SEP, 11),
        2050: (SEP, 1),
        2051: (SEP, 20),
        2052: (SEP, 8),
    }

    DURUTHU_POYA_DATES = {
        2003: (JAN, 17),
        2004: (JAN, 7),
        2005: (JAN, 24),
        2006: (JAN, 13),
        2007: (JAN, 3),
        2008: (JAN, 22),
        2009: ((JAN, 10), (DEC, 31)),
        2011: (JAN, 19),
        2012: (JAN, 8),
        2013: (JAN, 26),
        2014: (JAN, 15),
        2015: (JAN, 4),
        2016: (JAN, 23),
        2017: (JAN, 12),
        2018: (JAN, 1),
        2019: (JAN, 20),
        2020: (JAN, 10),
        2021: (JAN, 28),
        2022: (JAN, 17),
        2023: (JAN, 6),
        2024: (JAN, 25),
        2025: (JAN, 13),
        2026: (JAN, 3),
        # 2027-2052: astronomical estimates (noon rule, ~80% accuracy, ±1 day)
        # Note: years with two Duruthu entries have both Jan + Dec dates (same
        # pattern as 2009); years without a Jan entry had Duruthu in prev Dec.
        2027: (JAN, 22),
        2028: ((JAN, 11), (DEC, 31)),
        2030: (JAN, 19),
        2031: (JAN, 8),
        2032: (JAN, 27),
        2033: (JAN, 15),
        2034: (JAN, 4),
        2035: (JAN, 23),
        2036: (JAN, 13),
        2037: (JAN, 1),
        2038: (JAN, 20),
        2039: (JAN, 10),
        2040: (JAN, 29),
        2041: (JAN, 17),
        2042: (JAN, 6),
        2043: (JAN, 25),
        2044: (JAN, 14),
        2045: (JAN, 3),
        2046: (JAN, 22),
        2047: (JAN, 11),
        2048: (JAN, 1),
        2049: (JAN, 18),
        2050: (JAN, 7),
        2051: (JAN, 26),
        2052: (JAN, 15),
    }

    ESALA_POYA_DATES = {
        2003: (JUL, 13),
        2004: (JUL, 2),
        2005: (JUL, 21),
        2006: (JUL, 10),
        2007: (JUL, 29),
        2008: (JUL, 17),
        2009: (JUL, 6),
        2010: (JUL, 25),
        2011: (JUL, 14),
        2012: (JUL, 3),
        2013: (JUL, 22),
        2014: (JUL, 12),
        2015: (JUL, 31),
        2016: (JUL, 19),
        2017: (JUL, 8),
        2018: (JUL, 27),
        2019: (JUL, 16),
        2020: (JUL, 4),
        2021: (JUL, 23),
        2022: (JUL, 13),
        2023: (AUG, 1),
        2024: (JUL, 20),
        2025: (JUL, 10),
        2026: (JUL, 29),
        # 2027-2052: astronomical estimates (noon rule, ~80% accuracy, ±1 day)
        2027: (JUL, 18),
        2028: (JUL, 6),
        2029: (JUL, 25),
        2030: (JUL, 14),
        2031: (JUL, 4),
        2032: (JUL, 22),
        2033: (JUL, 12),
        2034: (JUL, 1),
        2035: (JUL, 20),
        2036: (JUL, 8),
        2037: (JUL, 26),
        2038: (JUL, 16),
        2039: (JUL, 5),
        2040: (JUL, 23),
        2041: (JUL, 13),
        2042: (JUL, 3),
        2043: (JUL, 21),
        2044: (JUL, 9),
        2045: (JUL, 28),
        2046: (JUL, 17),
        2047: (JUL, 7),
        2048: (JUL, 25),
        2049: (JUL, 14),
        2050: (JUL, 4),
        2051: (JUL, 23),
        2052: (JUL, 11),
    }

    IL_POYA_DATES = {
        2003: (NOV, 8),
        2004: (NOV, 26),
        2005: (NOV, 15),
        2006: (NOV, 5),
        2007: (NOV, 24),
        2008: (NOV, 12),
        2009: (NOV, 2),
        2010: (NOV, 21),
        2011: (NOV, 10),
        2012: (NOV, 27),
        2013: (NOV, 17),
        2014: (NOV, 6),
        2015: (NOV, 25),
        2016: (NOV, 14),
        2017: (NOV, 3),
        2018: (NOV, 22),
        2019: (NOV, 12),
        2020: (NOV, 29),
        2021: (NOV, 18),
        2022: (NOV, 7),
        2023: (NOV, 26),
        2024: (NOV, 15),
        2025: (NOV, 5),
        2026: (NOV, 24),
        # 2027-2052: astronomical estimates (noon rule, ~80% accuracy, ±1 day)
        2027: (NOV, 13),
        2028: (NOV, 2),
        2029: (NOV, 20),
        2030: (NOV, 9),
        2031: (NOV, 28),
        2032: (NOV, 17),
        2033: (NOV, 6),
        2034: (NOV, 25),
        2035: (NOV, 15),
        2036: (NOV, 3),
        2037: (NOV, 22),
        2038: (NOV, 11),
        2039: (NOV, 30),
        2040: (NOV, 18),
        2041: (NOV, 7),
        2042: (NOV, 26),
        2043: (NOV, 16),
        2044: (NOV, 5),
        2045: (NOV, 24),
        2046: (NOV, 13),
        2047: (NOV, 2),
        2048: (NOV, 20),
        2049: (NOV, 9),
        2050: (NOV, 28),
        2051: (NOV, 17),
        2052: (NOV, 6),
    }

    MEDIN_POYA_DATES = {
        2003: (MAR, 18),
        2004: (MAR, 6),
        2005: (MAR, 25),
        2006: (MAR, 14),
        2007: (MAR, 3),
        2008: (MAR, 21),
        2009: (MAR, 10),
        2010: (FEB, 28),
        2011: (MAR, 19),
        2012: (MAR, 7),
        2013: (MAR, 26),
        2014: (MAR, 16),
        2015: (MAR, 5),
        2016: (MAR, 22),
        2017: (MAR, 12),
        2018: (MAR, 1),
        2019: (MAR, 20),
        2020: (MAR, 9),
        2021: (MAR, 28),
        2022: (MAR, 17),
        2023: (MAR, 6),
        2024: (MAR, 24),
        2025: (MAR, 13),
        2026: (MAR, 2),
        # 2027-2052: astronomical estimates (noon rule, ~80% accuracy, ±1 day)
        2027: (MAR, 22),
        2028: (MAR, 10),
        2029: (FEB, 28),
        2030: (MAR, 19),
        2031: (MAR, 8),
        2032: (MAR, 26),
        2033: (MAR, 15),
        2034: (MAR, 4),
        2035: (MAR, 23),
        2036: (MAR, 12),
        2037: (MAR, 1),
        2038: (MAR, 20),
        2039: (MAR, 10),
        2040: (MAR, 28),
        2041: (MAR, 17),
        2042: (MAR, 6),
        2043: (MAR, 25),
        2044: (MAR, 13),
        2045: (MAR, 3),
        2046: (MAR, 22),
        2047: (MAR, 11),
        2048: (FEB, 29),
        2049: (MAR, 19),
        2050: (MAR, 8),
        2051: (MAR, 27),
        2052: (MAR, 15),
    }

    NAWAM_POYA_DATES = {
        2003: (FEB, 16),
        2004: (FEB, 5),
        2005: (FEB, 23),
        2006: (FEB, 12),
        2007: (FEB, 1),
        2008: (FEB, 20),
        2009: (FEB, 9),
        2010: (JAN, 29),
        2011: (FEB, 17),
        2012: (FEB, 7),
        2013: (FEB, 25),
        2014: (FEB, 14),
        2015: (FEB, 3),
        2016: (FEB, 22),
        2017: (FEB, 10),
        2018: (JAN, 31),
        2019: (FEB, 19),
        2020: (FEB, 8),
        2021: (FEB, 26),
        2022: (FEB, 16),
        2023: (FEB, 5),
        2024: (FEB, 23),
        2025: (FEB, 12),
        2026: (FEB, 1),
        # 2027-2052: astronomical estimates (noon rule, ~80% accuracy, ±1 day)
        2027: (FEB, 20),
        2028: (FEB, 10),
        2029: (JAN, 29),
        2030: (FEB, 17),
        2031: (FEB, 7),
        2032: (FEB, 26),
        2033: (FEB, 14),
        2034: (FEB, 3),
        2035: (FEB, 22),
        2036: (FEB, 11),
        2037: (JAN, 31),
        2038: (FEB, 19),
        2039: (FEB, 8),
        2040: (FEB, 27),
        2041: (FEB, 15),
        2042: (FEB, 4),
        2043: (FEB, 23),
        2044: (FEB, 13),
        2045: (FEB, 1),
        2046: (FEB, 20),
        2047: (FEB, 10),
        2048: (JAN, 30),
        2049: (FEB, 17),
        2050: (FEB, 6),
        2051: (FEB, 25),
        2052: (FEB, 14),
    }

    NIKINI_POYA_DATES = {
        2003: (AUG, 11),
        2004: (AUG, 29),
        2005: (AUG, 19),
        2006: (AUG, 9),
        2007: (AUG, 28),
        2008: (AUG, 16),
        2009: (AUG, 5),
        2010: (AUG, 24),
        2011: (AUG, 13),
        2012: (AUG, 1),
        2013: (AUG, 20),
        2014: (AUG, 10),
        2015: (AUG, 29),
        2016: (AUG, 17),
        2017: (AUG, 7),
        2018: (AUG, 25),
        2019: (AUG, 14),
        2020: (AUG, 3),
        2021: (AUG, 22),
        2022: (AUG, 11),
        2023: (AUG, 30),
        2024: (AUG, 19),
        2025: (AUG, 8),
        2026: (AUG, 27),
        # 2027-2052: astronomical estimates (noon rule, ~80% accuracy, ±1 day)
        2027: (AUG, 17),
        2028: (AUG, 5),
        2029: (AUG, 23),
        2030: (AUG, 13),
        2031: (AUG, 2),
        2032: (AUG, 20),
        2033: (AUG, 10),
        2034: (AUG, 29),
        2035: (AUG, 18),
        2036: (AUG, 6),
        2037: (AUG, 25),
        2038: (AUG, 14),
        2039: (AUG, 4),
        2040: (AUG, 22),
        2041: (AUG, 11),
        2042: (AUG, 1),
        2043: (AUG, 20),
        2044: (AUG, 8),
        2045: (AUG, 27),
        2046: (AUG, 16),
        2047: (AUG, 5),
        2048: (AUG, 23),
        2049: (AUG, 13),
        2050: (AUG, 2),
        2051: (AUG, 21),
        2052: (AUG, 10),
    }

    POSON_POYA_DATES = {
        2003: (JUN, 14),
        2004: (JUN, 2),
        2005: (JUN, 21),
        2006: (JUN, 11),
        2007: (JUN, 30),
        2008: (JUN, 18),
        2009: (JUN, 7),
        2010: (JUN, 25),
        2011: (JUN, 15),
        2012: (JUN, 4),
        2013: (JUN, 23),
        2014: (JUN, 12),
        2015: (JUN, 2),
        2016: (JUN, 19),
        2017: (JUN, 8),
        2018: (JUN, 27),
        2019: (JUN, 16),
        2020: (JUN, 5),
        2021: (JUN, 24),
        2022: (JUN, 14),
        2023: (JUN, 3),
        2024: (JUN, 21),
        2025: (JUN, 10),
        2026: (JUN, 29),
        # 2027-2052: astronomical estimates (noon rule, ~80% accuracy, ±1 day)
        2027: (JUN, 18),
        2028: (JUN, 6),
        2029: (JUN, 25),
        2030: (JUN, 15),
        2031: (JUN, 5),
        2032: (JUN, 23),
        2033: (JUN, 12),
        2034: (JUN, 1),
        2035: (JUN, 20),
        2036: (JUN, 8),
        2037: (MAY, 28),
        2038: (JUN, 16),
        2039: (JUN, 6),
        2040: (JUN, 24),
        2041: (JUN, 14),
        2042: (JUN, 3),
        2043: (JUN, 22),
        2044: (JUN, 10),
        2045: (MAY, 30),
        2046: (JUN, 18),
        2047: (JUN, 7),
        2048: (JUN, 25),
        2049: (JUN, 15),
        2050: (JUN, 5),
        2051: (JUN, 23),
        2052: (JUN, 12),
    }

    UNDUVAP_POYA_DATES = {
        2003: (DEC, 8),
        2004: (DEC, 26),
        2005: (DEC, 15),
        2006: (DEC, 4),
        2007: (DEC, 23),
        2008: (DEC, 12),
        2009: (DEC, 1),
        2010: (DEC, 20),
        2011: (DEC, 10),
        2012: (DEC, 27),
        2013: (DEC, 16),
        2014: (DEC, 6),
        2015: (DEC, 24),
        2016: (DEC, 13),
        2017: (DEC, 3),
        2018: (DEC, 22),
        2019: (DEC, 11),
        2020: (DEC, 29),
        2021: (DEC, 18),
        2022: (DEC, 7),
        2023: (DEC, 26),
        2024: (DEC, 14),
        2025: (DEC, 4),
        2026: (DEC, 23),
        # 2027-2052: astronomical estimates (noon rule, ~80% accuracy, ±1 day)
        2027: (DEC, 13),
        2028: (DEC, 1),
        2029: (DEC, 20),
        2030: (DEC, 9),
        2031: (DEC, 28),
        2032: (DEC, 16),
        2033: (DEC, 6),
        2034: (DEC, 25),
        2035: (DEC, 14),
        2036: (DEC, 3),
        2037: (DEC, 22),
        2038: (DEC, 11),
        2039: (DEC, 30),
        2040: (DEC, 18),
        2041: (DEC, 7),
        2042: (DEC, 26),
        2043: (DEC, 16),
        2044: (DEC, 4),
        2045: (DEC, 23),
        2046: (DEC, 13),
        2047: (DEC, 2),
        2048: (DEC, 20),
        2049: (DEC, 9),
        2050: (DEC, 27),
        2051: (DEC, 17),
        2052: (DEC, 6),
    }

    VAP_POYA_DATES = {
        2003: (OCT, 9),
        2004: (OCT, 27),
        2005: (OCT, 17),
        2006: (OCT, 6),
        2007: (OCT, 25),
        2008: (OCT, 14),
        2009: (OCT, 3),
        2010: (OCT, 22),
        2011: (OCT, 11),
        2012: (OCT, 29),
        2013: (OCT, 18),
        2014: (OCT, 8),
        2015: (OCT, 27),
        2016: (OCT, 15),
        2017: (OCT, 5),
        2018: (OCT, 24),
        2019: (OCT, 13),
        2020: (OCT, 30),
        2021: (OCT, 20),
        2022: (OCT, 9),
        2023: (OCT, 28),
        2024: (OCT, 17),
        2025: (OCT, 6),
        2026: (OCT, 25),
        # 2027-2052: astronomical estimates (noon rule, ~80% accuracy, ±1 day)
        2027: (OCT, 15),
        2028: (OCT, 3),
        2029: (OCT, 22),
        2030: (OCT, 11),
        2031: (OCT, 30),
        2032: (OCT, 18),
        2033: (OCT, 8),
        2034: (OCT, 27),
        2035: (OCT, 16),
        2036: (OCT, 5),
        2037: (OCT, 23),
        2038: (OCT, 12),
        2039: (OCT, 2),
        2040: (OCT, 19),
        2041: (OCT, 9),
        2042: (OCT, 28),
        2043: (OCT, 18),
        2044: (OCT, 6),
        2045: (OCT, 25),
        2046: (OCT, 14),
        2047: (OCT, 3),
        2048: (OCT, 21),
        2049: (OCT, 10),
        2050: (OCT, 29),
        2051: (OCT, 19),
        2052: (OCT, 8),
    }

    VESAK_POYA_DATES = {
        2003: (MAY, 15),
        2004: (MAY, 4),
        2005: (MAY, 23),
        2006: (MAY, 12),
        2007: (MAY, 1),
        2008: (MAY, 19),
        2009: (MAY, 8),
        2010: (MAY, 27),
        2011: (MAY, 17),
        2012: (MAY, 5),
        2013: (MAY, 24),
        2014: (MAY, 14),
        2015: (MAY, 3),
        2016: (MAY, 21),
        2017: (MAY, 10),
        2018: (APR, 29),
        2019: (MAY, 18),
        2020: (MAY, 7),
        2021: (MAY, 26),
        2022: (MAY, 15),
        2023: (MAY, 5),
        2024: (MAY, 23),
        2025: (MAY, 12),
        2026: (MAY, 1),
        # 2027-2052: astronomical estimates (noon rule, ~80% accuracy, ±1 day)
        2027: (MAY, 20),
        2028: (MAY, 8),
        2029: (MAY, 27),
        2030: (MAY, 17),
        2031: (MAY, 6),
        2032: (MAY, 24),
        2033: (MAY, 14),
        2034: (MAY, 3),
        2035: (MAY, 21),
        2036: (MAY, 10),
        2037: (APR, 29),
        2038: (MAY, 18),
        2039: (MAY, 8),
        2040: (MAY, 26),
        2041: (MAY, 15),
        2042: (MAY, 5),
        2043: (MAY, 23),
        2044: (MAY, 11),
        2045: (APR, 30),
        2046: (MAY, 19),
        2047: (MAY, 9),
        2048: (MAY, 27),
        2049: (MAY, 17),
        2050: (MAY, 6),
        2051: (MAY, 25),
        2052: (MAY, 13),
    }

    def _get_holiday(self, holiday: str, year: int) -> tuple[date | None, bool]:
        if year < self.START_YEAR or year > self.END_YEAR:
            return None, True
        dates = getattr(self, f"{holiday}_DATES", {})
        dt = dates.get(year, ())
        estimated = year > self.CONFIRMED_YEAR
        return (date(year, *dt) if dt else None), estimated

    def _get_holiday_set(self, holiday: str, year: int) -> Iterable[tuple[date, bool]]:
        if year < self.START_YEAR or year > self.END_YEAR:
            return
        dates = getattr(self, f"{holiday}_DATES", {})
        for yr in (year - 1, year):
            for dt in _normalize_tuple(dates.get(yr, ())):
                yield date(yr, *dt), yr > self.CONFIRMED_YEAR

    def bak_poya_date(self, year: int) -> tuple[date | None, bool]:
        return self._get_holiday(BAK_POYA, year)

    def binara_poya_date(self, year: int) -> tuple[date | None, bool]:
        return self._get_holiday(BINARA_POYA, year)

    def duruthu_poya_date(self, year: int) -> Iterable[tuple[date, bool]]:
        return self._get_holiday_set(DURUTHU_POYA, year)

    def esala_poya_date(self, year: int) -> tuple[date | None, bool]:
        return self._get_holiday(ESALA_POYA, year)

    def il_poya_date(self, year: int) -> tuple[date | None, bool]:
        return self._get_holiday(IL_POYA, year)

    def medin_poya_date(self, year: int) -> tuple[date | None, bool]:
        return self._get_holiday(MEDIN_POYA, year)

    def nawam_poya_date(self, year: int) -> tuple[date | None, bool]:
        return self._get_holiday(NAWAM_POYA, year)

    def nikini_poya_date(self, year: int) -> tuple[date | None, bool]:
        return self._get_holiday(NIKINI_POYA, year)

    def poson_poya_date(self, year: int) -> tuple[date | None, bool]:
        return self._get_holiday(POSON_POYA, year)

    def unduvap_poya_date(self, year: int) -> tuple[date | None, bool]:
        return self._get_holiday(UNDUVAP_POYA, year)

    def vap_poya_date(self, year: int) -> tuple[date | None, bool]:
        return self._get_holiday(VAP_POYA, year)

    def vesak_poya_date(self, year: int) -> tuple[date | None, bool]:
        return self._get_holiday(VESAK_POYA, year)


class _CustomSinhalaHolidays(_CustomCalendar, _SinhalaLunar):
    pass
