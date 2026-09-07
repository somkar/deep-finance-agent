from src.deepagent.tools import get_company_sector


def test_get_company_sector_known_company() -> None:
    assert get_company_sector.invoke({"company_name": "Microsoft"}) == "Technology"


def test_get_company_sector_unknown_company() -> None:
    assert get_company_sector.invoke({"company_name": "Unknown Co"}) == (
        "Sector information for Unknown Co is not available."
    )
