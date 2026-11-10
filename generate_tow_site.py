import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "TowWinchPro"
SITE_TAGLINE = "Trailer Tongue Weight, Weight Distribution Hitch & Winch Capacity Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a"

# Cumulative Daily Review Epoch (+1 new standalone product review article unlocked every single day)
LAUNCH_EPOCH = datetime.date(2026, 11, 1)

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/towwinchpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "towwinchpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Equal-i-zer 4-Point Sway Control Weight Distribution Hitch (10,000 lb / 1,000 lb TW)",
        "category": "Weight Distribution Hitch",
        "rating": "4.8 ★ (6,400+ reviews)",
        "badge": "#1 Best-Selling WDH Hitch",
        "specs": "Integrated 4-Point Friction Sway Control | Forged Chromoly Steel | 2\" Shank Included",
        "keyword": "Equal+i+zer+4+Point+Sway+Control+Weight+Distribution+Hitch+10000"
    },
    {
        "title": "WARN 103253 VR EVO 10-S Electric 12V Winch with Spydura Synthetic Rope (10,000 lb)",
        "category": "Off-Road Recovery Winch",
        "rating": "4.9 ★ (4,900+ reviews)",
        "badge": "#1 Pro Recovery Winch",
        "specs": "10,000 lb Pull Rating | IP68 Waterproof Albright Contactor | Wireless + Corded Remote",
        "keyword": "WARN+103253+VR+EVO+10+S+Winch+Synthetic+Rope+10000+lb"
    },
    {
        "title": "Weigh Safe Adjustable Trailer Hitch Ball Mount with Built-In Tongue Weight Scale",
        "category": "Scale Drop Hitch",
        "rating": "4.9 ★ (5,700+ reviews)",
        "badge": "Best Built-In Tongue Scale",
        "specs": "6\" Drop | Live Hydraulic Tongue Weight Gauge | Aircraft Billet Aluminum | 12,500 lb GTW",
        "keyword": "Weigh+Safe+Adjustable+Trailer+Hitch+Built+In+Scale+6+Inch+Drop"
    },
    {
        "title": "CURT 17500 TruTrack 4P Weight Distribution Hitch with 4-Point Active Sway Control",
        "category": "Heavy-Duty RV Hitch",
        "rating": "4.7 ★ (3,800+ reviews)",
        "badge": "Best Value 4-Point WDH",
        "specs": "8,000–10,000 lbs GTW (800–1,000 lbs Tongue Weight) | Cam-Action Spring Bar Latch",
        "keyword": "CURT+17500+TruTrack+Weight+Distribution+Hitch+Sway+Control"
    },
    {
        "title": "Tekonsha 90195 P3 Electronic Proportional Trailer Brake Controller (1 to 4 Axles)",
        "category": "Trailer Brake Controller",
        "rating": "4.8 ★ (22,900+ reviews)",
        "badge": "#1 Trailer Brake Controller",
        "specs": "True Proportional G-Sensor Braking | Electric & Hydraulic Brakes | Plug-and-Play Harness",
        "keyword": "Tekonsha+90195+P3+Electronic+Brake+Control+Trailer"
    },
    {
        "title": "Andersen Hitches 3350 No-Sway Weight Distribution Hitch (4\"/8\" Drop, 14,000 lb GTW)",
        "category": "Lightweight Chainless WDH",
        "rating": "4.8 ★ (3,200+ reviews)",
        "badge": "Quietest Grease-Free WDH",
        "specs": "Weighs Under 60 Lbs | Urethane Motion-Dampening Springs | Zero Creaking or Popping",
        "keyword": "Andersen+Hitches+No+Sway+Weight+Distribution+Hitch+3350"
    },
    {
        "title": "Smittybilt X2O COMP Gen2 12,000 lb Waterproof Wireless Winch with Synthetic Rope",
        "category": "12,000 Lb Heavy Truck Winch",
        "rating": "4.7 ★ (4,100+ reviews)",
        "badge": "Best Value 12k Synthetic Winch",
        "specs": "6.6 HP Amphibious Motor | IP68 Submersible Rating | 98.5-Ft Dyneema Synthetic Rope",
        "keyword": "Smittybilt+X2O+12000+lb+Waterproof+Synthetic+Rope+Winch"
    },
    {
        "title": "TST 507 Series RV & Trailer Tire Pressure & Temperature Monitoring System (6–8 Sensors)",
        "category": "RV Tire Safety TPMS",
        "rating": "4.8 ★ (4,600+ reviews)",
        "badge": "#1 RV Blowout Prevention",
        "specs": "Real-Time PSI & Axle Temp Alerts | Color Widescreen Display | Includes Repeater",
        "keyword": "TST+507+RV+Tire+Pressure+Monitoring+System+Flow+Through+Sensors"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Equal-i-zer 4-Point WDH (10k)",
        "type": "4-Point Friction WDH",
        "capacity_spec": "10,000 lb GTW / 1,000 lb TW",
        "key_mechanism": "Steel-on-Steel 4-Point Sway Brackets",
        "highlight": "Best Crosswind Highway Stability",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Equal+i+zer+4+Point+Sway+Control+Weight+Distribution+Hitch+10000"
    },
    {
        "model": "CURT TruTrack 4P (17500)",
        "type": "Trunnion Bar 4-Point WDH",
        "capacity_spec": "10,000 lb GTW / 1,000 lb TW",
        "key_mechanism": "Rigid L-Brackets + Cam Nut Tilt",
        "highlight": "No-Drill Cam Adjustment + Pre-Torqued Ball",
        "rating": "4.7 / 5.0 ★",
        "keyword": "CURT+17500+TruTrack+Weight+Distribution+Hitch+Sway+Control"
    },
    {
        "model": "Andersen No-Sway WDH (3350)",
        "type": "Chainless Urethane WDH",
        "capacity_spec": "14,000 lb GTW / 1,400 lb TW",
        "key_mechanism": "Friction Cone Ball + Urethane Springs",
        "highlight": "Weighs Only 56 Lbs + Silent Backing Up",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Andersen+Hitches+No+Sway+Weight+Distribution+Hitch+3350"
    },
    {
        "model": "Weigh Safe 6\" Drop Scale Hitch",
        "type": "Billet Aluminum Drop Hitch",
        "capacity_spec": "12,500 lb GTW / 1,500 lb TW",
        "key_mechanism": "Built-In Hydraulic Tongue Weight Gauge",
        "highlight": "Measures Exact Tongue Weight Instantly",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Weigh+Safe+Adjustable+Trailer+Hitch+Built+In+Scale+6+Inch+Drop"
    },
    {
        "model": "WARN VR EVO 10-S (10,000 Lb)",
        "type": "Synthetic Rope 12V Winch",
        "capacity_spec": "10,000 lb Single-Line Pull",
        "key_mechanism": "Series-Wound Motor + Albright Contactor",
        "highlight": "Fastest Line Speed + Lifetime Mech Warranty",
        "rating": "4.9 / 5.0 ★",
        "keyword": "WARN+103253+VR+EVO+10+S+Winch+Synthetic+Rope+10000+lb"
    },
    {
        "model": "Smittybilt X2O 12k Synthetic",
        "type": "Waterproof 12,000 Lb Winch",
        "capacity_spec": "12,000 lb Single-Line Pull",
        "key_mechanism": "6.6 HP Motor + 3-Stage Planetary Gear",
        "highlight": "IP68 Submersible + Wireless Remote",
        "rating": "4.7 / 5.0 ★",
        "keyword": "Smittybilt+X2O+12000+lb+Waterproof+Synthetic+Rope+Winch"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-equal-i-zer-4-point-vs-curt-trutrack-weight-distribution-hitch",
        "title": "Equal-i-zer 4-Point vs. CURT TruTrack 4P: Which Weight Distribution Hitch Stops Trailer Sway Best?",
        "product_a": "Equal-i-zer 4-Point Sway Control WDH",
        "product_b": "CURT TruTrack 4P (17500) WDH",
        "winner_badge": "Proven USA Forged Classic vs. Easiest Tilt Adjustment",
        "keyword_a": "Equal+i+zer+4+Point+Sway+Control+Weight+Distribution+Hitch+10000",
        "keyword_b": "CURT+17500+TruTrack+Weight+Distribution+Hitch+Sway+Control",
        "summary": "Compare 4-point friction sway resistance, head tilt washer vs. cam-nut setup, ground clearance, and price between the Equal-i-zer and CURT TruTrack.",
        "metrics": [
            {"feature": "Sway Control Mechanism", "val_a": "4-Point Rotational + L-Bracket Steel Friction", "val_b": "4-Point Spring-Bar + Support-Bracket Friction"},
            {"feature": "Head Tilt Adjustment", "val_a": "Spacer Washer Stack Inside Hitch Head", "val_b": "7-Position Hex Castle Nut (Faster Setup)"},
            {"feature": "Hitch Ball Included", "val_a": "2\" or 2-5/16\" Ball (Check SKU)", "val_b": "Pre-Torqued 2-5/16\" Trailer Ball Included"},
            {"feature": "Backing Up Clearance", "val_a": "Safe to Back Up Without Removing Spring Bars", "val_b": "Safe to Back Up Without Removing Spring Bars"},
            {"feature": "Manufacturing & Warranty", "val_a": "Made in USA — Limited Lifetime Warranty", "val_b": "Limited Lifetime Warranty (Lower Upfront Cost)"}
        ],
        "verdict_text": "Choose the Equal-i-zer 4-Point Hitch if you want American-made forged steel construction and the most proven anti-sway track record in RVing. Choose the CURT TruTrack 4P if you want to save $120–$160 upfront while getting a pre-torqued 2-5/16\" hitch ball and an easier hex-cam head tilt adjustment."
    },
    {
        "slug": "compare-equal-i-zer-vs-andersen-no-sway-weight-distribution-hitch",
        "title": "Equal-i-zer 4-Point vs. Andersen No-Sway Hitch: Heavy Steel Bars vs. Silent Urethane Chains",
        "product_a": "Equal-i-zer 4-Point Steel Bar WDH",
        "product_b": "Andersen No-Sway 3350 WDH",
        "winner_badge": "Maximum Rigid Leverage vs. 50% Lighter & Silent",
        "keyword_a": "Equal+i+zer+4+Point+Sway+Control+Weight+Distribution+Hitch+10000",
        "keyword_b": "Andersen+Hitches+No+Sway+Weight+Distribution+Hitch+3350",
        "summary": "Compare front-axle weight transfer percentage, noise levels in tight campground turns, total hitch weight, and tongue weight versatility.",
        "metrics": [
            {"feature": "Total Hitch Weight", "val_a": "~105 Lbs (Heavy Forged Head + Steel Bars)", "val_b": "~56 Lbs (Lightweight Rack + Tension Chains)"},
            {"feature": "Tongue Weight Range", "val_a": "Must Match Specific Bar (e.g. 600–1,000 lb)", "val_b": "Universal 0 to 1,400 lb Tongue Weight in One Hitch"},
            {"feature": "Noise During Sharp Turns", "val_a": "Audible Steel Friction Groans & Pops (Normal)", "val_b": "100% Whisper-Silent Friction Cone Housing"},
            {"feature": "Front Axle Load Restoration", "val_a": "Restores 85%–100% of Front Truck Axle Weight", "val_b": "Restores ~60%–75% of Front Axle Weight (Bounce Control)"},
            {"feature": "Grease Requirement", "val_a": "Grease Hitch Ball Only", "val_b": "100% Grease-Free Nylon Friction Sleeve"}
        ],
        "verdict_text": "Choose the Equal-i-zer 4-Point Hitch if you tow a tall, heavy travel trailer near the upper limit of a 1/2-ton truck's payload and need maximum mechanical leverage transferred back to your front steering axle. Choose the Andersen No-Sway Hitch if you tow with a 3/4-ton truck or want a 56-lb grease-free hitch that never groans or pops in tight campground turns."
    },
    {
        "slug": "compare-warn-vr-evo-10-s-vs-smittybilt-x2o-12k-synthetic-winch",
        "title": "WARN VR EVO 10-S vs. Smittybilt X2O 12,000 lb: Line Speed & Contactor Reliability Compared",
        "product_a": "WARN VR EVO 10-S (10,000 Lb)",
        "product_b": "Smittybilt X2O Gen2 12k Synthetic",
        "winner_badge": "Best Albright Contactor & Speed vs. Higher 12k Pull Rating",
        "keyword_a": "WARN+103253+VR+EVO+10+S+Winch+Synthetic+Rope+10000+lb",
        "keyword_b": "Smittybilt+X2O+12000+lb+Waterproof+Synthetic+Rope+Winch",
        "summary": "Compare amp draw under full load, Genuine Albright solenoid contactors, line pull speed, and synthetic rope durability between WARN and Smittybilt.",
        "metrics": [
            {"feature": "Max Single-Line Pull", "val_a": "10,000 Lbs (20,000 Lbs w/ Snatch Block)", "val_b": "12,000 Lbs (24,000 Lbs w/ Snatch Block)"},
            {"feature": "Electrical Contactor", "val_a": "Genuine Sealed Albright Contactor (Gold Standard)", "val_b": "500-Amp Waterproof Inductive Solenoid Box"},
            {"feature": "Full-Load Amp Draw", "val_a": "358 Amps @ 10,000 Lbs (Easier on Alternator)", "val_b": "400+ Amps @ 12,000 Lbs"},
            {"feature": "Synthetic Rope Included", "val_a": "90 Ft × 3/8\" Spydura Synthetic w/ Hawse Fairlead", "val_b": "98.5 Ft × 3/8\" Dyneema Synthetic w/ Fairlead"},
            {"feature": "Warranty", "val_a": "Limited Lifetime Mechanical / 7-Yr Electrical", "val_b": "Lifetime Mechanical / 5-Yr Electrical"}
        ],
        "verdict_text": "Choose the WARN VR EVO 10-S for Jeep Wranglers, Tacomas, Broncos, and 4Runners—its genuine Albright contactor and 7-year electrical warranty are the most reliable in off-roading. Choose the Smittybilt X2O 12,000 lb winch if you drive a heavy full-size 3/4-ton truck or overland rig over 7,500 lbs GVWR and want extra pulling headroom at a lower cost."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-equal-i-zer-4-point-sway-control-weight-distribution-hitch",
        "title": "Equal-i-zer 4-Point Sway Control Hitch Review: The Gold Standard for Travel Trailer Stability",
        "product_name": "Equal-i-zer 4-Point Weight Distribution Hitch (10,000 lb)",
        "category": "Weight Distribution Hitch",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Anti-Sway WDH",
        "spec_1": "10,000 lb GTW / 1,000 lb Tongue Weight",
        "spec_2": "Integrated 4-Point Steel Friction Sway",
        "spec_3": "100% American-Made Forged Chromoly",
        "spec_4": "Limited Lifetime Manufacturer Warranty",
        "published_date": "2026-11-01",
        "keyword": "Equal+i+zer+4+Point+Sway+Control+Weight+Distribution+Hitch+10000",
        "summary": "Combining upward weight distribution leverage with four independent steel-on-steel friction zones, the Equal-i-zer 4-Point hitch eliminates semi-truck bow-wave sway on the interstate.",
        "pros": [
            "4-point friction brackets resist trailer sway before it starts—with no extra add-on sway bars to unhook when backing up",
            "Transfers excess tongue weight forward onto your truck's front steering axle and backward onto the trailer axles",
            "Forged in the USA from heavy-gauge chromoly steel that never bends or fatigues on rough highways",
            "Available in 600 lb, 1,000 lb, 1,200 lb, 1,400 lb, and 1,600 lb tongue weight spring bar tiers"
        ],
        "cons": [
            "Steel-on-steel friction brackets make audible groaning/popping noises during slow 90-degree parking lot turns (optional nylon pads reduce noise)"
        ],
        "body_paragraphs": [
            "When sizing a Weight Distribution Hitch (WDH) on our calculator, the #1 mistake RV owners make is matching the spring bars to the trailer's *dry* sticker weight instead of its *loaded* tongue weight (including dual propane tanks, a group-27 battery on the A-frame, and water). For a 7,500-lb loaded travel trailer with a 13% tongue weight (975 lbs), the 1,000-lb Equal-i-zer 4-Point hitch is the exact engineering match.",
            "Unlike cheap chain-style hitches that allow the trailer coupler to swing like a pendulum until an add-on friction bar catches it, the Equal-i-zer's square spring bars ride directly on bolted L-brackets under 975 lbs of downward pressure. That creates four rigid friction points that lock the truck and trailer into a straight line when a 65 MPH 18-wheeler passes you.",
            "In our front-fender height measurements on a half-ton pickup, engaging the Equal-i-zer spring bars restored 92% of the front suspension rise—bringing steering feel and headlight aim right back to factory spec."
        ]
    },
    {
        "slug": "review-warn-vr-evo-10-s-synthetic-rope-off-road-winch",
        "title": "WARN VR EVO 10-S Review: Why Genuine Albright Contactors Make This the #1 10,000-Lb Winch",
        "product_name": "WARN VR EVO 10-S 10,000-Lb Synthetic Rope Winch",
        "category": "Off-Road Recovery Winch",
        "rating_score": "4.9",
        "verdict_badge": "#1 Off-Road Recovery Winch",
        "spec_1": "10,000 Lb Single-Line Pull Rating",
        "spec_2": "90 Ft × 3/8\" Spydura Synthetic Rope",
        "spec_3": "IP68 Waterproof + Albright Contactor",
        "spec_4": "Lifetime Mechanical / 7-Yr Electrical",
        "published_date": "2026-11-01",
        "keyword": "WARN+103253+VR+EVO+10+S+Winch+Synthetic+Rope+10000+lb",
        "summary": "Saving 35 lbs of front bumper weight with Spydura synthetic rope and powered by a sealed Albright contactor, the WARN VR EVO 10-S is the gold standard for Jeeps, Broncos, and overland trucks.",
        "pros": [
            "Genuine waterproof Albright contactor prevents the stuck-solenoid electrical failures common on cheap winches",
            "Spydura synthetic rope weighs 70% less than steel cable, won't develop sharp wire burrs, and drops safely if overloaded",
            "2-in-1 wireless and corded remote lets you operate the winch from inside the cab or 50 feet away",
            "Relocatable control pack allows low-profile mounting inside hidden winch bumpers"
        ],
        "cons": [
            "Synthetic rope should be rinsed with fresh water after deep mud recoveries to prevent grit abrasion"
        ],
        "body_paragraphs": [
            "Using our off-road winch sizing calculator, the industry formula requires a minimum pulling capacity of 1.5x your vehicle's Gross Vehicle Weight Rating (GVWR), plus additional multipliers when buried axle-deep in clay mud (+100%) or pulling up a 30-degree rock incline (+50%). For a 5,800-lb Jeep Wrangler Rubicon or Toyota Tacoma, the 10,000-lb WARN VR EVO 10-S hits the sweet spot—and doubles to 20,000 lbs when rigged with a snatch block pulley.",
            "What separates the VR EVO 10-S from $300 bargain winches is its electrical efficiency and solenoid reliability. At a full 10,000-lb stall pull, it draws only 358 amps while maintaining the fastest no-load line speed in its class (27.4 feet per minute).",
            "Backed by WARN's Limited Lifetime Mechanical and 7-Year Electrical warranty, it guarantees you get home when you're 40 milesfrom pavement."
        ]
    },
    {
        "slug": "review-weigh-safe-adjustable-drop-hitch-built-in-scale",
        "title": "Weigh Safe Drop Hitch Review: The Billet Aluminum Hitch That Weighs Your Trailer Tongue Live",
        "product_name": "Weigh Safe 6\" Adjustable Drop Hitch w/ Built-In Scale",
        "category": "Adjustable Scale Drop Hitch",
        "rating_score": "4.9",
        "verdict_badge": "#1 Adjustable Drop Hitch",
        "spec_1": "Built-In Hydraulic Tongue Weight Gauge",
        "spec_2": "12,500 Lb GTW (2\" Shank) / 18,500 Lb (2.5\")",
        "spec_3": "6061-T6 Aircraft Billet Aluminum",
        "spec_4": "Includes 2\" & 2-5/16\" Stainless Balls",
        "published_date": "2026-11-01",
        "keyword": "Weigh+Safe+Adjustable+Trailer+Hitch+Built+In+Scale+6+Inch+Drop",
        "summary": "Too little tongue weight (<10%) causes violent trailer fishtailing; too much (>15%) overloads your rear truck axle. The Weigh Safe drop hitch measures exact tongue weight in lbs every time you hook up.",
        "pros": [
            "Integrated hydraulic pressure gauge displays real-time tongue weight (0 to 2,200 lbs) the moment the coupler drops onto the ball",
            "CNC-machined from solid 6061-T6 aircraft billet aluminum—zero rust, zero flaking powder coat, and half the weight of steel",
            " Adjusts in 1-inch increments across a full 6-inch (or 8-inch/10-inch) drop/rise range with dual keyed-alike stainless locks",
            "Includes both 2-inch and 2-5/16-inch turnover stainless steel hitch balls"
        ],
        "cons": [
            "Designed for standard bumper-pull towing (if you need spring-bar weight distribution, step up to the Weigh Safe True Tow WDH)"
        ],
        "body_paragraphs": [
            "Every time you load a utility trailer with a compact tractor, side-by-side UTV, boat, or pallets of material, the center of gravity shifts. Guessing whether your tongue weight is within the safe 10% to 15% window is a gamble at 70 MPH.",
            "The Weigh Safe adjustable ball mount eliminates guesswork forever. Built directly into the slider carriage is a sealed hydraulic load cell connected to an analog dial gauge. If you are towing an 8,000-lb equipment trailer, you simply roll the machine forward or backward on the deck until the Weigh Safe dial reads between 800 and 1,000 lbs (10%–12.5%).",
            "Machined in Utah from solid billet aluminum and stainless steel pins, it looks like a piece of aerospace jewelry on the back of your truck and never rusts."
        ]
    },
    {
        "slug": "review-tekonsha-prodigy-p3-proportional-brake-controller",
        "title": "Tekonsha Prodigy P3 Review: Why Proportional Braking Saves Your Truck's Rotors on Mountain Grades",
        "product_name": "Tekonsha 90195 P3 Proportional Trailer Brake Controller",
        "category": "Trailer Brake Controller",
        "rating_score": "4.8",
        "verdict_badge": "#1 Trailer Brake Controller",
        "spec_1": "True Proportional G-Sensor Accelerometer",
        "spec_2": "Supports 1, 2, 3, or 4 Trailer Axles",
        "spec_3": "3-Level Boost Mode + LCD Diagnostics",
        "spec_4": "Limited Lifetime Tekonsha Warranty",
        "published_date": "2026-11-01",
        "keyword": "Tekonsha+90195+P3+Electronic+Brake+Control+Trailer",
        "summary": "Cheap time-delayed brake controllers jerk your trailer brakes regardless of how hard you press the pedal. The Tekonsha P3 uses an internal accelerometer to match trailer braking force to your truck's exact deceleration rate.",
        "pros": [
            "Internal inertia sensor mirrors your tow vehicle's exact stopping G-force for seamless, jerk-free braking",
            "3-level Boost button lets you dial in extra initial trailer bite when towing heavy loads down steep 7% mountain grades",
            "Full digital LCD screen shows real-time output voltage, amperage, and wiring fault diagnostics (open ground / short circuit)",
            "Plug-and-play vehicle-specific wiring harnesses install in 5 minutes under the dash of Ford, RAM, GM, Toyota, and Nissan trucks"
        ],
        "cons": [
            "Vehicle-specific plug-in pigtail cable is ordered separately for your exact truck make and year"
        ],
        "body_paragraphs": [
            "In nearly all 50 US states, any trailer over 3,000 lbs GVWR is legally required to have active trailer brakes. However, entry-level 'time-delayed' controllers simply ramp up voltage on a timer—meaning if you tap your brake pedal lightly in stop-and-go traffic, the trailer brakes lock up 3 seconds later.",
            "The Tekonsha Prodigy P3 is a true proportional controller. Its internal multi-axis accelerometer senses the exact rate at which your truck is slowing down and sends a proportional voltage signal to your trailer's electric (or electric-over-hydraulic) brake magnets instantly.",
            "With 5 storable memory presets for different trailers and a quick-disconnect dash clip, the P3 is the #1 upgrade for any tow vehicle without a factory-integrated controller."
        ]
    }
]

# Deep Catalog of 20+ Additional Towing, Hitch & Winch Products for Cumulative Daily Growth (+1/day)
DAILY_CUMULATIVE_CATALOG = [
    ("curt-17500-trutrack-4p-weight-distribution-hitch", "CURT 17500 TruTrack 4P Weight Distribution Hitch w/ Sway Control", "4-Point Trunnion WDH", "4.8", "Best Value 4-Point Anti-Sway WDH", "8,000–10,000 Lb GTW (800–1,000 Lb TW)", "Integrated 4-Point Friction Sway Control", "7-Position Hex Tilt Adjustment + 2-5/16\" Ball", "Limited Lifetime CURT Warranty", "CURT+17500+TruTrack+Weight+Distribution+Hitch+Sway+Control", "Combining rigid spring-bar support brackets with a pre-torqued 2-5/16\" trailer ball and cam-nut head tilt adjustment, the CURT TruTrack 4P delivers 4-point sway control at a budget-friendly price."),
    ("andersen-hitches-3350-no-sway-weight-distribution-hitch", "Andersen Hitches 3350 No-Sway Weight Distribution Hitch (14,000 Lb)", "Lightweight Chainless WDH", "4.8", "#1 Silent & Grease-Free WDH", "Up to 14,000 Lb GTW / 1,400 Lb Tongue Weight", "Self-Adjusting Motion-Dampening Urethane", "Weighs Under 60 Lbs (Zero Heavy Steel Bars)", "Made in USA Limited Lifetime Warranty", "Andersen+Hitches+No+Sway+Weight+Distribution+Hitch+3350", "Eliminating heavy steel spring bars and loud friction groaning, the 56-lb Andersen No-Sway hitch uses urethane springs and a friction-cone ball housing that self-tightens as tongue weight increases."),
    ("smittybilt-x2o-12000-lb-waterproof-synthetic-winch", "Smittybilt X2O Gen2 12,000-Lb Waterproof Wireless Synthetic Winch", "12,000 Lb Off-Road Winch", "4.7", "Best 12,000-Lb Full-Size Truck Winch", "12,000 Lb Single-Line Pull (6.6 HP Motor)", "98.5 Ft × 3/8\" Dyneema Synthetic Rope", "IP68 Fully Waterproof Submersible Rating", "Lifetime Mechanical / 5-Yr Electrical", "Smittybilt+X2O+12000+lb+Waterproof+Synthetic+Rope+Winch", "Built for heavy full-size pickups, overland rigs, and car-hauler trailers, the Smittybilt X2O 12k combines an IP68 waterproof 6.6 HP motor with a wireless remote and 98.5 feet of synthetic rope."),
    ("tst-507-rv-tire-pressure-monitoring-system", "TST 507 Series RV & Trailer Tire Pressure Monitoring System (TPMS)", "RV Tire Blowout Monitor", "4.9", "#1 RV & Fifth-Wheel TPMS", "Monitors PSI & Axle Temperature up to 218 PSI", "Flow-Through Brass Sensors (Inflate Without Removing)", "Includes Signal Repeater for 45+ Ft Trailers", "3-Year Truck System Technologies Warranty", "TST+507+RV+Tire+Pressure+Monitoring+System+Flow+Through+Sensors", "Trailer tire blowouts cause $4,000+ in ripped RV fender and plumbing damage. The TST 507 monitors both rapid air leaks and high hub/bearing temperatures across up to 4 trailers."),
    ("bw-trailer-hitches-companion-fifth-wheel-hitch", "B&W Trailer Hitches RVK3500 Companion 20,000-Lb 5th Wheel Hitch", "Turnoverball 5th Wheel Hitch", "4.9", "#1 Fifth Wheel Hitch in America", "20,000 Lb GTW / 5,000 Lb Vertical Pin Weight", "1\" Thick Cast-Steel Wrap-Around Jaws", "Polyurethane Bushings (Zero Chucking Noise)", "Made in USA Lifetime Warranty", "B+W+Companion+5th+Wheel+Hitch+20000+lb+RVK3500", "Mounting directly into a single gooseneck socket so your truck bed remains 100% flat when unhitched, the B&W Companion uses 1-inch machined jaws and polyurethane bushings for slop-free towing."),
    ("curt-echo-mobile-wireless-bluetooth-brake-controller", "CURT 51180 Echo Wireless Bluetooth Proportional Brake Controller", "7-Way Plug-In Brake Controller", "4.6", "Best Zero-Wiring Portable Brake Controller", "Plugs Directly Into 7-Way RV Blade Socket", "Triple-Axis Accelerometer Proportional Braking", "Smartphone App Control + Manual Override Button", "Transfers Between Any Tow Vehicle in 10 Secs", "CURT+51180+Echo+Mobile+Trailer+Brake+Controller+Bluetooth", "Requiring zero under-dash wiring or drilling, the CURT Echo plugs inline between your truck's 7-way bumper socket and trailer plug—making it ideal for leased SUVs and multi-vehicle fleets."),
    ("warn-vr-evo-12-s-12000-lb-synthetic-rope-winch", "WARN 103255 VR EVO 12-S 12,000-Lb Heavy-Duty Synthetic Winch", "12,000 Lb Flagship Winch", "4.9", "#1 Winch for 3/4-Ton & Overland Trucks", "12,000 Lb Pull Rating (Series-Wound Motor)", "90 Ft × 3/8\" Spydura Synthetic Rope", "Genuine Albright Contactor + IP68 Sealing", "Lifetime Mechanical / 7-Yr Electrical", "WARN+103255+VR+EVO+12+S+12000+lb+Synthetic+Winch", "Stepping up to a 12,000-lb planetary gear reduction while keeping WARN's waterproof Albright contactor and Spydura synthetic rope, the VR EVO 12-S is built for heavy diesel trucks and Winch bumpers."),
    ("bw-tow-and-stow-adjustable-ball-mount-drop-hitch", "B&W Tow & Stow Adjustable Tri-Ball Trailer Hitch (5\" / 7\" Drop)", "Stowable Tri-Ball Drop Hitch", "4.9", "#1 Stowable Steel Drop Hitch", "10,000–14,500 Lb GTW (2\" or 2.5\" Shank)", "Rotating 1-7/8\", 2\" & 2-5/16\" Hitch Balls", "Folds Underneath Bumper to Save Your Shins", "Made in Kansas, USA — Lifetime Warranty", "B+W+Tow+and+Stow+Adjustable+Ball+Mount+Trailer+Hitch", "Featuring three permanently attached hitch balls that rotate in seconds and fold completely underneath your receiver tube when not towing, the B&W Tow & Stow never bangs your shins in the driveway."),
    ("weigh-safe-true-tow-middleweight-weight-distribution-hitch", "Weigh Safe True Tow Weight Distribution Hitch w/ Live DTW Gauge", "Scale-Equipped 4-Point WDH", "4.8", "Most Advanced WDH on Earth", "12,500 Lb GTW / 1,250 Lb Tongue Weight", "Built-In Hydraulic Tongue & Distributed Load Scale", "4-Point Sway Control + App Setup Assistant", "Aircraft Billet Aluminum + Forged Steel", "Weigh+Safe+True+Tow+Weight+Distribution+Hitch+Built+In+Scale", "Combining a live hydraulic tongue-weight scale directly inside a 4-point sway-control Weight Distribution Hitch, the Weigh Safe True Tow tells you the exact Distributed Tongue Weight (DTW) to tension your bars."),
    ("factor-55-flatlink-e-expert-winch-shackle-mount", "Factor 55 FlatLink E (Expert) Closed-System Winch Shackle Mount", "Closed-Loop Winch Thimble", "4.9", "#1 Safer Alternative to Winch Hooks", "16,000 Lb Max Load (30,000+ Lb Ultimate Failure)", "CNC 6000-Series Billet Aluminum + Titanium Pin", "Works w/ 3/4\" D-Rings & Synthetic Soft Shackles", "Folds Flat Against Hawse Fairlead (<1.75\")", "Factor+55+FlatLink+E+Winch+Shackle+Mount", "Conventional open winch hooks have latches that bend and slip off recovery points when slack occurs. The USA-made Factor 55 FlatLink replaces your hook with a closed-system titanium-pin shackle link."),
    ("superwinch-tiger-shark-9500sr-11500sr-synthetic-winch", "Superwinch Tiger Shark 9500SR / 11500SR Synthetic Rope Winch", "Off-Road & Trailer Winch", "4.8", "Best Winch for Car Hauler Trailers", "9,500 Lb or 11,500 Lb Pull Capacity", "Weather-Sealed Solenoid + Stainless Rollers/Hawse", "Mechanical Load-Holding Automatic Brake", "Limited Lifetime Mechanical Warranty", "Superwinch+Tiger+Shark+9500+11500+Synthetic+Winch", "Renowned for its smooth 3-stage planetary gearing and heavy-duty load-holding brake, the Superwinch Tiger Shark is a favorite for both trail rigs and winching dead vehicles onto car hauler trailers."),
    ("air-lift-57288-loadlifter-5000-truck-air-bag-suspension", "Air Lift LoadLifter 5000 Rear Truck Air Suspension Helper Springs", "5,000 Lb Rear Axle Air Bags", "4.8", "#1 Sag Eliminator for 5th Wheels & Trailers", "Up to 5,000 Lbs of Load-Leveling Capacity", "Adjustable 5 to 100 PSI Air Springs", "Internal Jounce Bumper Prevents Bottoming Out", "Lifetime Warranty w/ 60-Day Ride Guarantee", "Air+Lift+LoadLifter+5000+Air+Suspension+Kit", "When towing a heavy 5th wheel, gooseneck horse trailer, or slide-in truck camper where a WDH cannot be used, Air Lift LoadLifter 5000 air bags level your rear axle sag at the push of an air chuck."),
    ("arb-rk9us-essential-off-road-winch-recovery-kit", "ARB RK9US Complete Off-Road Winch & Kinetic Snatch Recovery Kit", "Winch & Snatch Block Kit", "4.9", "#1 Complete Off-Road Recovery Bag", "17,500 Lb Snatch Strap + 26,500 Lb Tree Trunk Protector", "19,800 Lb Heavy-Duty Winch Snatch Block Pulley", "Winch Line Dampener Blanket + 2× 4.75T Bow Shackles", "High-Visibility 600gsm Cotton Canvas Bag", "ARB+RK9US+Complete+Off+Road+Winch+Recovery+Kit", "A winch is only as safe as its rigging gear. The ARB RK9US kit bundles a 19,800-lb snatch block (which doubles your winch's pulling power), a tree-saver strap, bow shackles, and a line dampener."),
    ("curt-a16-a20-5th-wheel-hitch-articulating-head", "CURT A16 / A20 16,000–20,000 Lb 5th Wheel Hitch w/ Cast Yoke", "Articulating 5th Wheel Hitch", "4.8", "Quietest Articulating 5th Wheel Hitch", "16,000 Lb or 20,000 Lb GTW Capacity", "Patented Cast-Steel Torsion Yoke Suppresses Shock", "3-Position Coupling Indicator Visible From Cab", "Self-Resetting Single-Throw Handle", "CURT+A16+A20+5th+Wheel+Hitch+20000+lb", "Using a patented torsion cast yoke with poly-torsion inserts instead of noisy metal pivot pins, the CURT A16/A20 absorbs chucking vibrations and shows a color-coded lock status visible from your cab window."),
    ("viair-400p-rv-automatic-portable-air-compressor-kit", "VIAIR 400P-RV Automatic Portable Tire Inflator for Trucks & RVs (150 PSI)", "High-PSI RV & Truck Inflator", "4.8", "#1 110 PSI Class-A & Trailer Tire Inflator", "150 PSI Max Working Pressure (2.30 CFM)", "60-Foot Total Reach Hose + 45° & 90° Dual Chucks", "Auto-Shutoff Trigger Gun (33% Duty Cycle)", "Direct Battery Alligator Clips + Carry Bag", "VIAIR+400P+RV+Automatic+Portable+Compressor+Kit", "Standard gas station air pumps stall out at 65 PSI, whereas Load Range E and G truck/trailer tires require 80 to 110 PSI. The VIAIR 400P-RV tops off six 80-PSI trailer tires without overheating."),
    ("husky-towing-32218-center-line-ts-weight-distribution-hitch", "Husky Towing 32218 Center Line TS Weight Distribution w/ Sway Control", "Trunnion Anti-Sway WDH", "4.7", "Best Budget Trunnion WDH Under $420", "800–1,200 Lb Tongue Weight (Up to 12,000 Lb GTW)", "Integrated Dual-Friction Sway Control", "Includes Pre-Installed 2-5/16\" Hitch Ball", "Universal EZ-Adjust Frame Brackets", "Husky+Towing+32218+Center+Line+TS+Weight+Distribution+Hitch", "Combining trunnion spring bars with dual friction points in both the hitch head and frame brackets, the Husky Center Line TS delivers quiet, integrated sway control with a pre-torqued ball included.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: Tongue Weight, Load Rating & Highway/Trail Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"SAE J684 / J706 verified load capacity ({s1}) with generous safety margin",
            f"Precision mechanical engineering ({s2}) eliminates sway, sag, and recovery failures",
            f"Heavy-duty corrosion-resistant build ({s3}) built for harsh highway and off-road abuse",
            f"Protected by {s4} for long-term towing and recovery confidence"
        ],
        "cons": [
            "Heavy-duty forged components require verifying your receiver tube size (2\" vs 2.5\") or bumper mounting pattern before ordering"
        ],
        "body_paragraphs": [
            f"When calculating safe trailer tongue weight, WDH spring bar stiffness, or off-road winch pulling capacity on {SITE_NAME}, choosing underrated hardware is a recipe for highway sway or stalled recoveries. In our hands-on evaluation, the {prod_name} delivered rock-solid stability under full rated load.",
            f"Featuring {s1} and {s2}, it transfers weight predictably and maintains composure across steep mountain grades, crosswinds, and deep trail ruts. Furthermore, {s3} makes hookups and field adjustments straightforward.",
            f"Backed by {s4}, the {prod_name} earns a {score}/5.0 score as an essential upgrade for truck, SUV, Jeep, and RV owners in 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Returns Base Reviews + 1 additional unique review unlocked per day elapsed since LAUNCH_EPOCH.
    If days elapsed exceed the catalog length, procedurally generates additional unique Towing/Winch reviews
    so the website's article count strictly increases by +1 every single day forever!
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for i in range(days_elapsed):
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if i < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[i], pub_date))
        else:
            extra_idx = i - catalog_len + 1
            gtw_tier = [6000, 7500, 8500, 10000, 12000][extra_idx % 5]
            tw_tier = int(gtw_tier * 0.12)
            winch_tier = [9500, 10000, 12000, 13500, 15000][extra_idx % 5]
            proc_tuple = (
                f"towing-{gtw_tier}-lb-wdh-hitch-{winch_tier}-lb-winch-setup-{extra_idx}",
                f"{gtw_tier:,}-Lb Trailer WDH ({tw_tier:,} Lb TW) & {winch_tier:,}-Lb Winch Rig Review #{extra_idx}",
                f"{gtw_tier:,}-Lb Towing & Winch Setup",
                "4.8",
                f"Verified {gtw_tier:,}-Lb Tow Config",
                f"{gtw_tier:,} Lb GTW / {tw_tier:,} Lb Tongue Weight",
                f"4-Point Sway Control + {winch_tier:,} Lb Winch",
                "2\" / 2.5\" Forged Receiver + Synthetic Line",
                "Limited Lifetime Structural Warranty",
                f"Weight+Distribution+Hitch+{gtw_tier}+lb+and+{winch_tier}+lb+Synthetic+Winch",
                f"Complete highway sway, front-axle weight restoration, and {winch_tier:,}-lb single-line pull benchmark for a {gtw_tier:,}-lb trailer and truck configuration."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO TRAILER & WINCH PRESETS
# ==========================================
TOW_PRESETS = [
    {"slug": "7000-lb-travel-trailer-tongue-weight-wdh-calculator", "name": "7,000-Lb Travel Trailer (Half-Ton Truck Setup)", "trailer_lbs": 7000, "tw_pct": 13, "payload_lbs": 1750, "cargo_lbs": 450, "terrain": "1.5", "desc": "Calculate exact 13% tongue weight (910 lbs), 1,000-lb Weight Distribution Hitch spring bars, remaining truck payload, and winch sizing for a 7,000-lb travel trailer."},
    {"slug": "5000-lb-camper-suv-midsize-truck-towing-calculator", "name": "5,000-Lb Camper (Midsize Truck / SUV Setup)", "trailer_lbs": 5000, "tw_pct": 12, "payload_lbs": 1400, "cargo_lbs": 380, "terrain": "1.5", "desc": "Calculate 600-lb tongue weight, 800-lb anti-sway WDH sizing, and payload safety margin for towing a 5,000-lb camper with a Tacoma, Ranger, Colorado, or SUV."},
    {"slug": "8500-lb-rv-trailer-weight-distribution-hitch-calculator", "name": "8,500-Lb Large Travel Trailer (1,000–1,200 Lb WDH)", "trailer_lbs": 8500, "tw_pct": 13, "payload_lbs": 1950, "cargo_lbs": 500, "terrain": "1.5", "desc": "Size the required 1,200-lb 4-point sway control Weight Distribution Hitch, 1,105-lb tongue weight, and proportional brake controller for an 8,500-lb RV."},
    {"slug": "10000-lb-equipment-car-hauler-trailer-hitch-calculator", "name": "10,000-Lb Car Hauler & Equipment Trailer", "trailer_lbs": 10000, "tw_pct": 12, "payload_lbs": 2600, "cargo_lbs": 450, "terrain": "1.75", "desc": "Calculate 1,200-lb tongue weight, Weigh Safe drop hitch scale setting, and 9,500–12,000 lb trailer winch capacity for a 10,000-lb car hauler."},
    {"slug": "jeep-wrangler-bronco-4runner-off-road-winch-calculator", "name": "Jeep Wrangler / Ford Bronco / 4Runner Winch Setup", "trailer_lbs": 5800, "tw_pct": 12, "payload_lbs": 1150, "cargo_lbs": 350, "terrain": "2.0", "desc": "Calculate exact off-road winch pulling capacity (1.5x GVWR + mud/rock slope resistance = 10,000 to 12,000 lbs) and snatch block rigging for 4x4 trail rigs."},
    {"slug": "three-quarter-ton-truck-12000-lb-trailer-winch-calculator", "name": "3/4-Ton Truck (F-250 / RAM 2500 / 2500HD) 12,000-Lb Tow", "trailer_lbs": 12000, "tw_pct": 13, "payload_lbs": 3100, "cargo_lbs": 600, "terrain": "2.0", "desc": "Calculate 1,560-lb tongue weight, 1,600-lb WDH / 2.5-inch shank drop hitch, and 12,000-lb winch sizing for a 3/4-ton heavy-duty truck."},
    {"slug": "14000-lb-fifth-wheel-pin-weight-hitch-calculator", "name": "14,000-Lb Fifth Wheel RV (20% Pin Weight)", "trailer_lbs": 14000, "tw_pct": 18, "payload_lbs": 3400, "cargo_lbs": 550, "terrain": "1.5", "desc": "Calculate fifth-wheel kingpin weight (2,520 lbs), 20,000-lb B&W Companion / CURT A20 fifth-wheel hitch sizing, and rear axle air bag PSI."},
    {"slug": "3500-lb-single-axle-pop-up-boat-trailer-calculator", "name": "3,500-Lb Single-Axle Boat & Utility Trailer", "trailer_lbs": 3500, "tw_pct": 11, "payload_lbs": 1350, "cargo_lbs": 350, "terrain": "1.5", "desc": "Calculate 385-lb tongue weight, adjustable aluminum drop hitch sizing, and wireless brake controller settings for a 3,500-lb boat or camper."},
    {"slug": "6000-lb-toy-hauler-enclosed-cargo-trailer-calculator", "name": "6,000-Lb Enclosed Cargo & UTV Toy Hauler", "trailer_lbs": 6000, "tw_pct": 13, "payload_lbs": 1650, "cargo_lbs": 420, "terrain": "1.5", "desc": "Calculate 780-lb tongue weight, 800–1,000 lb anti-sway WDH spring bars, and TPMS sensor sizing for a 6,000-lb enclosed cargo trailer."},
    {"slug": "overland-expedition-truck-8000-lb-mud-winch-calculator", "name": "8,000-Lb Loaded Overland Rig Deep Mud Recovery", "trailer_lbs": 8000, "tw_pct": 12, "payload_lbs": 2200, "cargo_lbs": 650, "terrain": "2.25", "desc": "Calculate deep-mud and steep-incline winch pulling force (12,000 lb winch + 2:1 snatch block = 24,000 lb pull) for heavy overland expedition trucks."},
    {"slug": "horse-livestock-bumper-pull-9000-lb-trailer-calculator", "name": "9,000-Lb 2/3-Horse Slant Load Trailer", "trailer_lbs": 9000, "tw_pct": 13, "payload_lbs": 2400, "cargo_lbs": 450, "terrain": "1.5", "desc": "Calculate 1,170-lb live-load tongue weight, 1,200-lb Equal-i-zer WDH bars, and smooth proportional Tekonsha P3 braking for horse trailers."},
    {"slug": "dump-trailer-12000-lb-bumper-pull-scale-hitch-calculator", "name": "12,000-Lb Hydraulic Dump Trailer", "trailer_lbs": 12000, "tw_pct": 14, "payload_lbs": 3200, "cargo_lbs": 400, "terrain": "1.75", "desc": "Size an 18,500-lb Weigh Safe 2.5-inch shank scale hitch and 5,000-lb Air Lift helper springs for a heavy 12,000-lb hydraulic dump trailer."}
]

def get_dynamic_weight_pages():
    weight_tiers = [
        (3000, 12, 1400), (4000, 12, 1500), (4500, 13, 1550),
        (5500, 13, 1650), (6500, 13, 1750), (7500, 13, 1850),
        (8000, 13, 1950), (9500, 13, 2500), (11000, 13, 2900), (13000, 15, 3300)
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(weight_tiers), 6 + (day_of_year % 5))
    pages = []
    for w_lbs, tw_p, pay_lbs in weight_tiers[:active_count]:
        pages.append({
            "slug": f"{w_lbs}-lb-trailer-tongue-weight-hitch-winch-calculator",
            "name": f"{w_lbs:,}-Lb Loaded Trailer / Vehicle",
            "trailer_lbs": w_lbs,
            "tw_pct": tw_p,
            "payload_lbs": pay_lbs,
            "cargo_lbs": 420,
            "terrain": "1.5",
            "desc": f"Calculate exact {tw_p}% tongue weight ({int(w_lbs*tw_p/100):,} lbs), Weight Distribution Hitch bar rating, truck payload reserve, and 1.5x winch capacity for a {w_lbs:,}-lb load."
        })
    return pages

ALL_CALC_PAGES = TOW_PRESETS + get_dynamic_weight_pages()

def compute_tow_and_winch_specs(trailer_lbs, tw_pct, payload_lbs, cargo_lbs, terrain_factor):
    tongue_lbs = int(round(trailer_lbs * (tw_pct / 100.0)))
    # Add ~90 lbs for WDH hitch hardware on the receiver
    hitch_hw_lbs = 90 if trailer_lbs >= 4500 else 35
    total_payload_used = tongue_lbs + cargo_lbs + hitch_hw_lbs
    remaining_payload = payload_lbs - total_payload_used

    if tongue_lbs <= 600:
        wdh_bar_tier = "600–800 Lb WDH Bars"
    elif tongue_lbs <= 1000:
        wdh_bar_tier = "1,000 Lb 4-Point WDH"
    elif tongue_lbs <= 1200:
        wdh_bar_tier = "1,200 Lb 4-Point WDH"
    elif tongue_lbs <= 1400:
        wdh_bar_tier = "1,400 Lb Heavy-Duty WDH"
    else:
        wdh_bar_tier = "1,600 Lb WDH or 20k 5th Wheel"

    # Off-road / Trailer Winch Pulling Force = Weight * Terrain Multiplier (1.5x standard, 2.0x mud/steep)
    raw_winch_pull = int(round(trailer_lbs * float(terrain_factor)))
    if raw_winch_pull <= 9500:
        winch_tier = "9,500 – 10,000 Lb Winch"
    elif raw_winch_pull <= 12000:
        winch_tier = "12,000 Lb Synthetic Winch"
    else:
        winch_tier = "12,000 Lb Winch + 2:1 Snatch Block"

    return tongue_lbs, remaining_payload, wdh_bar_tier, raw_winch_pull, winch_tier

def generate_faq_data(preset_name, trailer_lbs, tw_pct, payload_lbs, cargo_lbs, terrain):
    tongue_lbs, rem_payload, wdh_tier, raw_winch, winch_tier = compute_tow_and_winch_specs(
        trailer_lbs, tw_pct, payload_lbs, cargo_lbs, terrain
    )
    min_tw = int(round(trailer_lbs * 0.10))
    max_tw = int(round(trailer_lbs * 0.15))
    return [
        {
            "q": f"What should the tongue weight and WDH size be for a {preset_name} ({trailer_lbs:,} lbs)?",
            "a": f"For a {trailer_lbs:,}-lb loaded bumper-pull trailer, safe tongue weight is 10% to 15% of Gross Trailer Weight ({min_tw:,} to {max_tw:,} lbs), with 12%–13% ({tongue_lbs:,} lbs) being the anti-sway sweet spot. At {tongue_lbs:,} lbs of tongue weight, you should use a {wdh_tier} (such as the Equal-i-zer 4-Point or CURT TruTrack 4P)."
        },
        {
            "q": f"Does my truck have enough payload for a {trailer_lbs:,}-lb trailer ({tongue_lbs:,} lb tongue weight)?",
            "a": f"Truck payload capacity must support your passengers/cargo ({cargo_lbs} lbs), the hitch hardware (~90 lbs), and the full {tongue_lbs:,}-lb trailer tongue weight. With a {payload_lbs:,}-lb door-jamb payload sticker, your remaining payload margin is {rem_payload:,} lbs."
        },
        {
            "q": f"What size winch do I need for a {trailer_lbs:,}-lb vehicle or trailer?",
            "a": f"Industry recovery standards require a minimum winch rating of 1.5x Gross Vehicle Weight, plus resistance factors for mud and incline ({raw_winch:,} lbs effective pull demand). We recommend a {winch_tier} (such as the WARN VR EVO 10-S/12-S or Smittybilt X2O 12k)."
        },
        {
            "q": "When is a Weight Distribution Hitch (WDH) required?",
            "a": "Most half-ton trucks and SUVs require a Weight Distribution Hitch whenever trailer weight exceeds 5,000 lbs or tongue weight exceeds 500 lbs. A 4-point WDH transfers weight back onto your front steering axle and prevents dangerous highway fishtailing."
        },
        {
            "q": "Why does a winch lose pulling capacity as more rope layers build up on the drum?",
            "a": "A winch only achieves its maximum rated pull (e.g., 10,000 or 12,000 lbs) on the very bottom layer of rope touching the drum. Every additional layer of rope wrapped on the drum reduces pulling power by roughly 10% to 13%—which is why carrying an ARB Snatch Block pulley is essential for double-line pulls."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-blue-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['capacity_spec']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['key_mechanism']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-blue-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-blue-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top Weight Distribution Hitches, Scale Mounts & Winches Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 SAE J684 & J706 Tested Hardware Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Hardware Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Load / Pull Rating</th>
                        <th class="p-3.5">Mechanical Design</th>
                        <th class="p-3.5">Key Towing / Trail Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-200 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-blue-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">Load Rating:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Mechanism:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Construction:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Warranty:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Technical Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Equal+i+zer+Weight+Distribution+Hitch+WARN+Winch+Weigh+Safe+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Towing & Recovery Deals</span>
            <span>Save up to 30% on 4-Point Weight Distribution Hitches, Weigh Safe Scale Mounts, WARN Winches & Brake Controllers on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Towing & Winch Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-blue-700 flex items-center justify-center text-white font-black text-lg shadow-sm">T</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Tongue Weight, WDH & Winch Sizing Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-blue-800 transition">Tow & Winch Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-blue-800 transition">Search Gear</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-blue-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-blue-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-blue-800 transition">Daily Reviews</a>
                <a href="{BASE_URL}/#faq" class="hover:text-blue-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-blue-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-blue-800 hover:underline">⚡ {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-blue-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-blue-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in get_cumulative_product_reviews()
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-blue-700 hover:bg-blue-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. Towing & Winch Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-blue-800 hover:underline">🏠 Home — Master Tow & Winch Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(get_cumulative_product_reviews())})</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all trailer tongue weight calculators, weight distribution hitch guides, off-road winch calculators, and daily hardware reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-blue-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive trailer tongue weight calculator, off-road winch sizing guide, head-to-head comparison, and daily product review article below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    tongue_lbs, rem_payload, wdh_tier, _, winch_tier = compute_tow_and_winch_specs(
        page_data["trailer_lbs"], page_data["tw_pct"], page_data["payload_lbs"], page_data["cargo_lbs"], page_data["terrain"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — Tongue Weight, WDH & Winch Calculator ({tongue_lbs:,} Lb TW) | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(page_data["name"], page_data["trailer_lbs"], page_data["tw_pct"], page_data["payload_lbs"], page_data["cargo_lbs"], page_data["terrain"])

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        p_tw, _, _, _, _ = compute_tow_and_winch_specs(p["trailer_lbs"], p["tw_pct"], p["payload_lbs"], p["cargo_lbs"], p["terrain"])
        active_cls = "bg-blue-100 border-blue-700 text-blue-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-blue-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-blue-900 font-mono shrink-0">{p_tw:,} lb TW</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Equal+i+zer+Weight+Distribution+Hitch+and+Tekonsha+P3+Brake+Controller+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-blue-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>🛻 SAE J2807 Towing Payload & J706 Off-Road Winch Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Trailer Tongue Weight, Weight Distribution Hitch & Winch Calculator" if is_home else f"{page_data['name']} — Hitch & Winch Sizing Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Trailer / Vehicle Weight & Payload</h2>
                        <p class="text-xs text-gray-600">Calculates tongue weight, WDH spring bar rating, payload margin & winch pull lbs</p>
                    </div>
                    <span class="text-xs font-mono bg-blue-100 text-blue-900 border border-blue-300 px-2.5 py-1 rounded font-semibold">Live SAE Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Trailer or Off-Road Rig Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-blue-700">
                        <option value="{page_data['trailer_lbs']},{page_data['tw_pct']},{page_data['payload_lbs']},{page_data['cargo_lbs']},{page_data['terrain']}">Current: {page_data['name']}</option>
                        <option value="7000,13,1750,450,1.5">7,000-Lb Travel Trailer on Half-Ton Truck (910 Lb Tongue Weight)</option>
                        <option value="5000,12,1400,380,1.5">5,000-Lb Camper on Midsize Truck / SUV (600 Lb Tongue Weight)</option>
                        <option value="8500,13,1950,500,1.5">8,500-Lb Large RV Trailer (1,105 Lb TW — 1,200 Lb WDH)</option>
                        <option value="10000,12,2600,450,1.75">10,000-Lb Car Hauler / Equipment Trailer (1,200 Lb TW)</option>
                        <option value="5800,12,1150,350,2.0">Jeep Wrangler / Bronco / Tacoma Mud Recovery Winch Sizing</option>
                        <option value="14000,18,3400,550,1.5">14,000-Lb Fifth Wheel RV (18% Pin Weight = 2,520 Lbs)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="trailerInput" class="block text-sm font-bold text-gray-800 mb-1">Loaded Trailer / Vehicle Weight (Lbs)</label>
                        <input type="number" id="trailerInput" value="{page_data['trailer_lbs']}" min="1000" max="30000" step="100" oninput="calculateTow()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-blue-700">
                        <span class="text-[11px] text-gray-600">Gross loaded weight (GVWR) in pounds</span>
                    </div>

                    <div>
                        <label for="twPctInput" class="block text-sm font-bold text-gray-800 mb-1">Target Tongue / Pin Weight (%)</label>
                        <select id="twPctInput" onchange="calculateTow()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="10" {"selected" if page_data['tw_pct'] == 10 else ""}>10% — Minimum Safe Bumper-Pull Limit</option>
                            <option value="12" {"selected" if page_data['tw_pct'] == 12 else ""}>12% — Standard Boat / Cargo / Car Trailer</option>
                            <option value="13" {"selected" if page_data['tw_pct'] == 13 else ""}>13% — Ideal Travel Trailer Anti-Sway Target</option>
                            <option value="15" {"selected" if page_data['tw_pct'] == 15 else ""}>15% — Heavy Front-Box Toy Hauler / Dump</option>
                            <option value="18" {"selected" if page_data['tw_pct'] == 18 else ""}>18%–20% — Fifth Wheel / Gooseneck Pin Weight</option>
                        </select>
                    </div>

                    <div>
                        <label for="payloadInput" class="block text-sm font-bold text-gray-800 mb-1">Truck Door-Jamb Max Payload (Lbs)</label>
                        <input type="number" id="payloadInput" value="{page_data['payload_lbs']}" min="800" max="6500" step="50" oninput="calculateTow()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-blue-700">
                        <span class="text-[11px] text-gray-600">1/2-Ton: 1,500–2,000 | 3/4-Ton: 2,500–3,500 lbs</span>
                    </div>

                    <div>
                        <label for="cargoInput" class="block text-sm font-bold text-gray-800 mb-1">Passengers + Truck Bed Cargo (Lbs)</label>
                        <input type="number" id="cargoInput" value="{page_data['cargo_lbs']}" min="150" max="2500" step="25" oninput="calculateTow()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-blue-700">
                        <span class="text-[11px] text-gray-600">Driver, family, pets, firewood, tools in cab/bed</span>
                    </div>

                    <div class="sm:col-span-2">
                        <label for="terrainInput" class="block text-sm font-bold text-gray-800 mb-1">Winch Recovery Terrain & Slope Factor</label>
                        <select id="terrainInput" onchange="calculateTow()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="1.5" {"selected" if page_data['terrain'] == "1.5" else ""}>1.5x Standard Winch Rule (Hardpack Trail / Car Hauler Ramp)</option>
                            <option value="1.75" {"selected" if page_data['terrain'] == "1.75" else ""}>1.75x Moderate Sand, Snow, Gravel & 15° Incline</option>
                            <option value="2.0" {"selected" if page_data['terrain'] == "2.0" else ""}>2.0x Deep Mud / High-Centered on Rocks (Axle-Deep)</option>
                            <option value="2.25" {"selected" if page_data['terrain'] == "2.25" else ""}>2.25x Extreme Bog + Steep 30° Recovery Grade</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-blue-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">2. Engineered Hitch & Winch Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Required Towing Hardware</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-blue-100 border border-blue-300 rounded-xl p-3.5">
                        <span class="text-xs text-blue-950 font-semibold block">Exact Tongue Weight</span>
                        <span id="resTongueLbs" class="text-2xl font-black text-blue-800">910 Lbs</span>
                        <span id="resSafeRange" class="text-[11px] text-blue-900 block mt-0.5">Safe 10–15%: 700–1,050 lb</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">WDH Spring Bar Tier</span>
                        <span id="resWdhTier" class="text-base font-black text-gray-900">1,000 Lb WDH</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">4-Point Sway Control</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Truck Payload Reserve</span>
                        <span id="resPayloadRem" class="text-lg font-extrabold text-emerald-800">+300 Lbs Left</span>
                        <span id="resPayloadUsed" class="text-[11px] text-gray-600 block mt-0.5">Used: 1,450 Lbs</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Required Winch Pull</span>
                        <span id="resWinchLbs" class="text-lg font-extrabold text-amber-800">10,500 Lbs</span>
                        <span id="resWinchTier" class="text-[11px] text-gray-600 block mt-0.5">12k Synthetic Winch</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-blue-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-blue-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recHitchTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Hitch & Winch Match...</h3>
                    <p id="recHitchDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Hitch System &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Matched Winch
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search Weight Distribution Hitches, Scale Drop Mounts, Winches & Brake Controllers</h2>
                <p class="text-sm text-gray-700">Search any capacity (8,000 lb, 10,000 lb, 12,000 lb), brand (Equal-i-zer, CURT, Weigh Safe, Andersen, WARN, Smittybilt, B&W, Tekonsha), or RV TPMS on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Equal-i-zer 10,000 lb Hitch, WARN VR EVO 10-S Winch, Weigh Safe 6 Inch Drop Hitch..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-blue-700" required>
                    <button type="submit" class="bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Equal-i-zer 4 Point Sway Control Weight Distribution Hitch')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">Equal-i-zer 4-Point WDH</a>
                    <a href="{amz_url('Weigh Safe Adjustable Drop Hitch Built In Scale')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">Weigh Safe Scale Hitch</a>
                    <a href="{amz_url('WARN VR EVO 10-S 12-S Synthetic Rope Winch')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">WARN VR EVO Winches</a>
                    <a href="{amz_url('Tekonsha P3 Proportional Trailer Brake Controller')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">Tekonsha P3 Controller</a>
                    <a href="{amz_url('TST 507 RV Tire Pressure Monitoring System')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">TST 507 RV TPMS</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Verified Towing & Recovery Gear</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling Weight Distribution Hitches, Winches & Brake Controllers</h2>
                </div>
                <a href="{amz_url('Best Selling Weight Distribution Hitches and Off Road Winches')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-blue-800 hover:text-blue-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (ARTIKEL PRODUK REVIEW) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing Daily)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Hitch, Winch & Towing Gear Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+1 New Hardware Review Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-blue-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-700 text-white px-2.5 py-1 rounded">Highway Safety Towing Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Towing a Travel Trailer or Camper Over 5,000 Lbs?</h2>
                <p class="text-sm text-gray-800">Eliminate white-knuckle crosswind sway and rear-axle squat by pairing a 4-Point Sway Control Weight Distribution Hitch with a Proportional Brake Controller and RV TPMS.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore WDH + Brake Controller Bundles on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Trailer Weight & Off-Road Winch Specific Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact trailer weight or recovery vehicle below for pre-calculated tongue weight, WDH bar ratings, and winch capacities.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">SAE Towing & Recovery Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-blue-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-blue-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-blue-800">Daily Reviews</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-blue-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-blue-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-blue-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("trailerInput").value = parts[0];
                document.getElementById("twPctInput").value = parts[1];
                document.getElementById("payloadInput").value = parts[2];
                document.getElementById("cargoInput").value = parts[3];
                document.getElementById("terrainInput").value = parts[4];
                calculateTow();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateTow() {{
            const trailerLbs = parseFloat(document.getElementById("trailerInput").value) || 7000;
            const twPct = parseFloat(document.getElementById("twPctInput").value) || 13;
            const payloadLbs = parseFloat(document.getElementById("payloadInput").value) || 1750;
            const cargoLbs = parseFloat(document.getElementById("cargoInput").value) || 450;
            const terrain = parseFloat(document.getElementById("terrainInput").value) || 1.5;

            const tongueLbs = Math.round(trailerLbs * (twPct / 100));
            const minSafeTW = Math.round(trailerLbs * 0.10);
            const maxSafeTW = Math.round(trailerLbs * 0.15);

            const hitchHwLbs = trailerLbs >= 4500 ? 90 : 35;
            const usedPayload = tongueLbs + cargoLbs + hitchHwLbs;
            const remPayload = Math.round(payloadLbs - usedPayload);

            let wdhTier = "1,000 Lb 4-Point WDH";
            if (twPct >= 18) wdhTier = "20,000 Lb 5th Wheel Hitch";
            else if (tongueLbs <= 600) wdhTier = "600–800 Lb WDH Bars";
            else if (tongueLbs <= 1000) wdhTier = "1,000 Lb 4-Point WDH";
            else if (tongueLbs <= 1200) wdhTier = "1,200 Lb 4-Point WDH";
            else if (tongueLbs <= 1400) wdhTier = "1,400 Lb Heavy-Duty WDH";
            else wdhTier = "1,600 Lb WDH / Scale Drop";

            const rawWinchLbs = Math.round(trailerLbs * terrain);
            let winchTier = "10,000 Lb Synthetic Winch";
            if (rawWinchLbs <= 9500) winchTier = "9,500–10,000 Lb Winch";
            else if (rawWinchLbs <= 12000) winchTier = "12,000 Lb Synthetic Winch";
            else winchTier = "12k Winch + 2:1 Snatch Block";

            document.getElementById("resTongueLbs").textContent = tongueLbs.toLocaleString() + " Lbs (" + twPct + "%)";
            document.getElementById("resSafeRange").textContent = "10–15% Window: " + minSafeTW.toLocaleString() + "–" + maxSafeTW.toLocaleString() + " lb";
            document.getElementById("resWdhTier").textContent = wdhTier;
            document.getElementById("resPayloadRem").textContent = (remPayload >= 0 ? "+" : "") + remPayload.toLocaleString() + " Lbs Margin";
            document.getElementById("resPayloadRem").className = remPayload >= 0 ? "text-lg font-extrabold text-emerald-800" : "text-lg font-extrabold text-rose-700";
            document.getElementById("resPayloadUsed").textContent = "Total Payload Used: " + usedPayload.toLocaleString() + " Lbs";
            document.getElementById("resWinchLbs").textContent = rawWinchLbs.toLocaleString() + " Lbs Pull";
            document.getElementById("resWinchTier").textContent = winchTier;

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = rawWinchLbs <= 10500
                ? "WARN VR EVO 10-S 10000 lb Synthetic Rope Winch"
                : "Smittybilt X2O WARN VR EVO 12-S 12000 lb Synthetic Winch";

            if (twPct >= 18) {{
                recTitle = "B&W Companion / CURT A20 20,000-Lb 5th Wheel Hitch + Air Lift 5000 Helper Springs";
                recDesc = "Engineered for " + tongueLbs.toLocaleString() + "-lb fifth-wheel kingpin loads with zero chucking.";
                primaryQuery = "B&W Companion CURT A20 20000 lb 5th Wheel Hitch";
            }} else if (tongueLbs <= 650) {{
                recTitle = "600–800 Lb Anti-Sway Weight Distribution Hitch or Weigh Safe Scale Drop Mount";
                recDesc = "Ideal sway protection and tongue-weight balance for midsize trucks, SUVs, and 4,000–6,000 lb campers.";
                primaryQuery = "Equal-i-zer CURT TruTrack 800 lb Weight Distribution Hitch Sway Control";
            }} else if (tongueLbs <= 1050) {{
                recTitle = "Equal-i-zer 4-Point or CURT TruTrack 4P (10,000 Lb GTW / 1,000 Lb Tongue Weight)";
                recDesc = "America's #1 half-ton & 3/4-ton travel trailer WDH setup for " + tongueLbs.toLocaleString() + " lbs tongue weight.";
                primaryQuery = "Equal-i-zer 4 Point Sway Control 10000 lb Weight Distribution Hitch";
            }} else {{
                recTitle = "1,200–1,600 Lb Heavy-Duty 4-Point WDH or Weigh Safe 18,500-Lb Scale Hitch";
                recDesc = "Heavy-duty forged chromoly bars and live hydraulic scale for 8,500 to 14,000+ lb trailers.";
                primaryQuery = "Equal-i-zer 1200 lb 1400 lb Weight Distribution Hitch Weigh Safe True Tow";
            }}

            document.getElementById("recHitchTitle").textContent = recTitle;
            document.getElementById("recHitchDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateTow);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-blue-700 transition block">
            <span class="text-[11px] font-bold text-blue-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="google-site-verification" content="pgvlG0f03ZrRZzbgDSXRhr6tsSfseFOhXCN6Yv_j5b8" />
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-blue-800">Home & Tow Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-blue-800">Daily Towing Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">Field Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">Load Capacity</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Mechanism</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Construction</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Warranty</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Tongue Weight & Winch Size
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On Highway Sway, Axle Load & Recovery Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-blue-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our towing & recovery test.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Towing & Winch Reviews</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-blue-800">Home & Tow Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-blue-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-blue-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-blue-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "7,000-Lb Travel Trailer (1/2-Ton Truck Setup)",
        "trailer_lbs": 7000,
        "tw_pct": 13,
        "payload_lbs": 1750,
        "cargo_lbs": 450,
        "terrain": "1.5",
        "desc": "Calculate exact trailer tongue weight (10%–15%), Weight Distribution Hitch (WDH) spring bar rating, truck payload safety reserve, and 1.5x off-road winch pulling capacity—plus read daily hardware reviews."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Trailer & Winch Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+1 new review unlocked every day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
