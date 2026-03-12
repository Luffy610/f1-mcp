import pandas as pd
from core.session_cache import session_cache
from connectors.ergast_client import ErgastClient


class DriverService:

    def __init__(self):
        self.ergast = ErgastClient()

    def load_session(self, year, gp, session):
        return session_cache.get_session(year, gp, session)

    # TOOL 13
    def list_drivers(self, year, gp, session):

        s = self.load_session(year, gp, session)

        drivers = []

        for drv in s.drivers:
            info = s.get_driver(drv)

            drivers.append({
                "code": drv,
                "name": f"{info['FirstName']} {info['LastName']}"
            })

        return drivers

    # TOOL 14
    def get_driver_info(self, year, gp, session, driver):

        s = self.load_session(year, gp, session)

        info = s.get_driver(driver)

        # Sanitize all values for JSON serialization
        from core.serialization import sanitize_value
        return {k: sanitize_value(v) for k, v in dict(info).items()}

    # TOOL 15
    def get_driver_team(self, year, gp, session, driver):

        s = self.load_session(year, gp, session)

        info = s.get_driver(driver)

        return {
            "driver": driver,
            "team": info.get("TeamName")
        }

    # TOOL 16
    def get_driver_number(self, year, gp, session, driver):

        s = self.load_session(year, gp, session)

        info = s.get_driver(driver)

        return {
            "driver": driver,
            "number": info.get("DriverNumber")
        }

    # TOOL 17
    def get_teammate(self, year, gp, session, driver):

        s = self.load_session(year, gp, session)

        info = s.get_driver(driver)
        team = info.get("TeamName")

        for num in s.drivers:
            drv_info = s.get_driver(num)
            abbrev = drv_info.get("Abbreviation")

            if abbrev != driver and drv_info.get("TeamName") == team:
                return {
                    "driver": driver,
                    "teammate": abbrev,
                    "team": team
                }

        return None

    # TOOL 18
    def get_driver_grid_position(self, year, gp, session, driver):

        s = self.load_session(year, gp, session)

        results = s.results

        row = results[results["Abbreviation"] == driver]

        if row.empty:
            return None

        val = row["GridPosition"].values[0]
        if pd.isna(val):
            return None
        return int(val)

    # TOOL 19
    def get_driver_finish_position(self, year, gp, session, driver):

        s = self.load_session(year, gp, session)

        results = s.results

        row = results[results["Abbreviation"] == driver]

        if row.empty:
            return None

        val = row["Position"].values[0]
        if pd.isna(val):
            return None
        return int(val)

    # TOOL 20
    def get_driver_points(self, year, gp, session, driver):

        s = self.load_session(year, gp, session)

        results = s.results

        row = results[results["Abbreviation"] == driver]

        if row.empty:
            return None

        return float(row["Points"].values[0])

    # TOOL 21
    def get_constructor_standings(self, year):

        data = self.ergast.get_constructor_standings(year)

        standings = []

        for row in data:
            standings.append({
                "position": row["position"],
                "constructor": row["constructorName"],
                "points": row["points"]
            })

        return standings

    # TOOL 22
    def get_driver_standings(self, year):

        data = self.ergast.get_driver_standings(year)

        standings = []

        for row in data:
            standings.append({
                "position": row["position"],
                "driver": f"{row['givenName']} {row['familyName']}",
                "points": row["points"],
                "constructor": row["constructorNames"]
            })

        return standings