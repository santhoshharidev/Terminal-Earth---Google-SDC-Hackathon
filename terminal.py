import google.generativeai as genai
from dotenv import load_dotenv
from tabulate import tabulate
import os
import json
import re
import webbrowser
from datetime import datetime
from dashboard_writer import generate_dashboard

# =====================================
# LOAD ENVIRONMENT VARIABLES
# =====================================

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =====================================
# GEMINI MODEL
# =====================================

model = genai.GenerativeModel("gemini-2.5-flash")

# =====================================
# TERMINAL HEADER
# =====================================

print("\n===================================")
print("      TERMINAL EARTH v1.0")
print("===================================\n")

def save_history(record):

    try:

        with open("history.json", "r") as file:
            history = json.load(file)

    except:

        history = []

    history.append(record)

    with open("history.json", "w") as file:
        json.dump(history, file, indent=4)

def get_last_shipment():

    try:

        with open("history.json", "r") as file:
            history = json.load(file)

        if len(history) > 0:
            return history[-1]

    except:
        pass

    return None


def build_context():

    last = get_last_shipment()

    if last is None:
        return ""

    return f"""
LAST SHIPMENT CONTEXT

Command:
{last['command']}

Source:
{last['source']}

Destination:
{last['destination']}

Recommended Mode:
{last['recommended_mode']}

Estimated Cost:
{last['estimated_cost']}
"""

# =====================================
# MAIN LOOP
# =====================================

while True:

    command = input("> ")

    if command.lower() == "exit":
        print("\nGoodbye!\n")
        break
    
    if command.lower() == "history":

        try:

            with open("history.json", "r") as file:
                history = json.load(file)

            print("\n===== COMMAND HISTORY =====\n")

            for item in history:

                print(
                    f"[{item['timestamp']}] "
                    f"{item['source']} -> "
                    f"{item['destination']} | "
                    f"{item['recommended_mode']}"
                )

            print()

        except:

            print("No history found.\n")

        continue

    if command.lower() == "last":

        last = get_last_shipment()

        if last:

            print("\n===== LAST SHIPMENT =====\n")

            for key, value in last.items():
                print(f"{key}: {value}")

            print()

        else:

            print("No shipment history found.\n")

        continue

    if command.lower() == "optimize":

        last = get_last_shipment()

        if not last:

            print("No shipment history found.\n")
            continue

        optimize_prompt = f"""
    You are a logistics optimization expert.

    Shipment:

    Source: {last['source']}
    Destination: {last['destination']}
    Recommended Mode: {last['recommended_mode']}
    Estimated Cost: {last['estimated_cost']}

    Suggest:

    1. Cost optimization
    2. Time optimization
    3. Best overall option

    Keep response short.
    """

        response = model.generate_content(optimize_prompt)

        print("\n========== OPTIMIZATION ==========\n")

        print(response.text)

        print("\n==================================\n")

        continue

    if command.lower() == "carbon":

        last = get_last_shipment()

        if not last:

            print("No shipment history found.\n")
            continue

        carbon_prompt = f"""
            You are a sustainability analyst.

            Shipment:

            Source: {last['source']}
            Destination: {last['destination']}

            Estimate CO2 emissions for:

            Truck
            Rail
            Air Cargo

            Return ONLY:

            Truck : value
            Rail : value
            Air Cargo : value

            Also tell:

            Greenest Option
            """
        
        response = model.generate_content(carbon_prompt)

        print("\n========== CARBON REPORT ==========\n")

        print(response.text)

        print("\n===================================\n")

        continue

    if command.lower() == "help":

        print("""
    Available Commands

    history
    last
    optimize
    carbon
    clear history
    help
    exit
    """)

        continue

    if command.lower() == "clear history":

        with open("history.json", "w") as file:
            json.dump([], file)

        print("History cleared.\n")

        continue

    context = build_context()

    prompt = f"""
You are Terminal Earth, an AI-powered logistics intelligence engine.

Previous Shipment Context:

{context}

Current User Request:

{command}

CONTEXT RULES:

1. If the user asks follow-up questions such as:
   - what if...
   - same shipment...
   - same route...
   - reduce budget...
   - increase budget...
   - increase weight...
   - decrease weight...
   - deliver faster...
   - deliver within X hours...
   - change deadline...

   Then continue using the previous shipment details unless the user explicitly changes them.

2. Never invent a new source or destination when previous context exists.

3. Always preserve shipment continuity across follow-up questions.

ANALYSIS REQUIREMENTS:

Analyze the shipment using realistic Indian logistics estimates.

Consider:

- Source
- Destination
- Cargo Weight
- Budget
- Delivery Deadline

Compare ONLY:

1. Truck
2. Rail
3. Air Cargo

OUTPUT RULES:

- Return ONLY valid JSON.
- No markdown.
- No explanations outside JSON.
- No ```json blocks.
- Keep all values SHORT.
- Cost should be a realistic range.

    Examples:

    "25k-60k INR"
    "10k-30k INR"
    "80k-250k INR"

Do not provide a single exact quotation unless explicitly requested.

- Time should be compact.
  Example: "30h"
- Rating should be:
  Example: "9/10"

ADVANTAGE RULES:

ONLY ONE SHORT KEYWORD.

Examples:
- Flexible
- Fast
- Reliable
- Cheap
- Secure

DRAWBACK RULES:

ONLY ONE SHORT KEYWORD.

Examples:
- Traffic
- Slow
- Expensive
- Limited
- Complex

BAD EXAMPLES:

❌ Door-to-door service, flexibility, relatively fast transport

❌ Potential delays due to traffic and road conditions

GOOD EXAMPLES:

✅ Flexible

✅ Traffic

✅ Cheap

✅ Expensive

RECOMMENDATION RULES:

recommendation_reason must be SHORT.

Maximum 10 words.

Example:

"Best balance of cost and delivery time"

COST ESTIMATION RULES

Use standard Indian domestic freight market rates.

Assume:

- Normal commercial shipment
- Shared freight when appropriate
- No premium express service unless requested
- No special handling unless requested

Typical reference ranges:

1000kg Chennai → Delhi

Truck:
25k-60k INR

Rail:
10k-30k INR

Air Cargo:
80k-250k INR

Do not generate inflated enterprise-level quotations.

Return EXACTLY this JSON:

{{
    "source":"",
    "destination":"",
    "recommended_mode":"",
    "estimated_cost":"",
    "estimated_time":"",
    "risk":"",
    "transport_comparison":[
        {{
            "mode":"Truck",
            "cost":"",
            "time":"",
            "rating":"",
            "advantage":"",
            "drawback":""
        }},
        {{
            "mode":"Rail",
            "cost":"",
            "time":"",
            "rating":"",
            "advantage":"",
            "drawback":""
        }},
        {{
            "mode":"Air Cargo",
            "cost":"",
            "time":"",
            "rating":"",
            "advantage":"",
            "drawback":""
        }}
    ],
    "recommendation_reason":""
}}
"""

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        # Remove accidental markdown formatting

        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)

        data = json.loads(text)

        source = data["source"]
        destination = data["destination"]

        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "command": command,
            "source": source,
            "destination": destination,
            "recommended_mode": data["recommended_mode"],
            "estimated_cost": data["estimated_cost"]
        }

        save_history(record)

        # =====================================
        # SUMMARY TABLE
        # =====================================

        summary_table = [
            ["Source", source],
            ["Destination", destination],
            ["Recommended Mode", data["recommended_mode"]],
            ["Estimated Cost", data["estimated_cost"]],
            ["Estimated Time", data["estimated_time"]],
            ["Risk Level", data["risk"]]
        ]

        print("\n")
        print("========== SHIPMENT SUMMARY ==========\n")

        print(
            tabulate(
                summary_table,
                headers=["Field", "Value"],
                tablefmt="grid"
            )
        )

        # =====================================
        # TRANSPORT COMPARISON TABLE
        # =====================================

        comparison_table = []

        for item in data["transport_comparison"]:

            comparison_table.append([
                item["mode"],
                item["cost"],
                item["time"],
                item["rating"],
                item["advantage"],
                item["drawback"]
            ])

        print(
            tabulate(
                comparison_table,
                headers=[
                    "Mode",
                    "Cost",
                    "Time",
                    "Score",
                    "Advantage",
                    "Drawback"
                ],
                tablefmt="grid"
            )
        )

        # =====================================
        # RECOMMENDATION
        # =====================================

        print("\n")
        print("========== RECOMMENDATION ==========\n")

        print(f"Recommended Mode : {data['recommended_mode']}\n")

        print(
            f"Reason : {data['recommendation_reason']}"
        )

        print("\n====================================\n")

        dashboard_choice = input(
            "\nGenerate Google Sheets Dashboard? (Y/N): "
        ).strip().lower()

        if dashboard_choice == "y":

            dashboard_url = generate_dashboard(data)

            print("\nDashboard Generated Successfully!")

            print(dashboard_url)

        # =====================================
        # OPEN GOOGLE MAPS
        # =====================================

        maps_url = (
            f"https://www.google.com/maps/dir/"
            f"{source}/{destination}"
        )

        while True:

            choice = input(
                "\nOpen Google Maps Route Analysis? (Y/N): "
            ).strip().lower()

            if choice == "y":

                print("\nOpening Google Maps...\n")

                webbrowser.open(maps_url)

                break

            elif choice == "n":

                print("\nGoogle Maps opening skipped.\n")

                break

            else:

                print("Please enter Y or N.")

    except Exception as e:

        print("\nERROR OCCURRED\n")
        print(e)
        print()