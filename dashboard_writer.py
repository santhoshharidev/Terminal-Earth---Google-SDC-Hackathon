import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

def convert_cost(cost_text):

    numbers = re.findall(r"\d+", cost_text)

    if len(numbers) >= 2:

        low = int(numbers[0])

        high = int(numbers[1])

        return (low + high) / 2 * 1000

    elif len(numbers) == 1:

        return int(numbers[0]) * 1000

    return 0

def convert_rating(rating_text):

    numbers = re.findall(r"\d+", rating_text)

    if len(numbers) > 0:

        return int(numbers[0])

    return 0

def convert_time(time_text):

    text = time_text.lower()

    if "d" in text:

        nums = re.findall(r"\d+", text)

        if len(nums) >= 2:

            return (int(nums[0]) + int(nums[1])) / 2 * 24

        elif len(nums) == 1:

            return int(nums[0]) * 24

    if "h" in text:

        nums = re.findall(r"\d+", text)

        if len(nums) > 0:

            return int(nums[0])

    return 0

def generate_dashboard(data):

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json",
        scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("Terminal Earth Dashboard")

    worksheet = sheet.sheet1

    worksheet.clear()

    worksheet.update(
        "A1",
        [["TERMINAL EARTH DASHBOARD"]]
    )

    worksheet.update(
        "A3",
        [["SHIPMENT SUMMARY"]]
    )

    worksheet.update(
        "D3",
        [["TRANSPORT COMPARISON"]]
    )

    cost_table = [["Mode", "Cost"]]

    time_table = [["Mode", "Hours"]]

    score_table = [["Mode", "Score"]]

    for item in data["transport_comparison"]:

        cost_table.append([
            item["mode"],
            convert_cost(item["cost"])
        ])

        time_table.append([
            item["mode"],
            convert_time(item["time"])
        ])

        score_table.append([
            item["mode"],
            convert_rating(item["rating"])
        ])

    worksheet.update("I4:J7", cost_table)

    worksheet.update("F11:G14", time_table)

    worksheet.update("I11:J14", score_table)

    worksheet.update(
        "F10",
        [["TIME COMPARISION"]]
    )

    worksheet.update(
        "I3",
        [["COST COMPARISION"]]
    )

    worksheet.update(
        "I10",
        [["SCORE COMPARISION"]]
    )

    worksheet.update(
        "A13",
        [["FINAL RECOMMENDATION"]]
    )

    summary_data = [
        ["Field", "Value"],
        ["Source", data["source"]],
        ["Destination", data["destination"]],
        ["Recommended Mode", data["recommended_mode"]],
        ["Estimated Cost", data["estimated_cost"]],
        ["Estimated Time", data["estimated_time"]],
        ["Risk", data["risk"]]
    ]

    worksheet.update("A4:B10", summary_data)

    comparison_data = [
        ["Mode", "Cost", "Time", "Score"]
    ]

    for item in data["transport_comparison"]:

        comparison_data.append([
            item["mode"],
            item["cost"],
            item["time"],
            item["rating"]
        ])

    worksheet.update(
        f"D4:G{4 + len(comparison_data) - 1}",
        comparison_data
    )

    worksheet.update(
        "A14:B15",
        [
            ["Recommendation",
             data["recommended_mode"]],

            ["Reason",
             data["recommendation_reason"]]
        ]
    )

    worksheet.format(
    "A1:G15",
    {
        "textFormat": {
            "fontSize": 11
        }
    }
)
    
    worksheet.format(
        "A3",
        {
            "textFormat": {
                "bold": True,
                "fontSize": 16
            }
        }
    )

    worksheet.format(
        "D3",
        {
            "textFormat": {
                "bold": True,
                "fontSize": 16
            }
        }
    )

    worksheet.format(
        "A14",
        {
            "textFormat": {
                "bold": True,
                "fontSize": 12
            }
        }
    )

    worksheet.format(
        "A15",
        {
            "textFormat": {
                "bold": True,
                "fontSize": 12
            }
        }
    )

    worksheet.format(
        "B14",
        {
            "textFormat": {
                "fontSize": 12
            }
        }
    )

    worksheet.format(
        "B15",
        {
            "textFormat": {
                "fontSize": 12
            }
        }
    )

    worksheet.format(
        "A13",
        {
            "textFormat": {
                "bold": True,
                "fontSize": 16
            }
        }
    )

    worksheet.format(
        "F10",
        {
            "textFormat": {
                "bold": True,
                "fontSize": 14
            }
        }
    )

    worksheet.format(
        "I10",
        {
            "textFormat": {
                "bold": True,
                "fontSize": 14
            }
        }
    )

    worksheet.format(
        "I3",
        {
            "textFormat": {
                "bold": True,
                "fontSize": 14
            }
        }
    )

    worksheet.format(
        "A4:B4",
        {
            "textFormat": {
                "bold": True
            }
        }
    )

    worksheet.format(
        "D4:G4",
        {
            "textFormat": {
                "bold": True
            }
        }
    )

    worksheet.format(
        "A4:B10",
        {
            "borders": {
                "top": {"style": "SOLID"},
                "bottom": {"style": "SOLID"},
                "left": {"style": "SOLID"},
                "right": {"style": "SOLID"}
            }
        }
    )

    worksheet.format(
        "D4:G7",
        {
            "borders": {
                "top": {"style": "SOLID"},
                "bottom": {"style": "SOLID"},
                "left": {"style": "SOLID"},
                "right": {"style": "SOLID"}
            }
        }
    )

   # Merge title cells

    worksheet.merge_cells("A1:G1")

    # Format dashboard title

    worksheet.format(
        "A1:G1",
        {
            "horizontalAlignment": "CENTER",
            "textFormat": {
                "bold": True,
                "fontSize": 28
            }
        }
    )
 
    return sheet.url