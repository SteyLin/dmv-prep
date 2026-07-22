#!/usr/bin/env python3
"""Expands Virginia (va) and Texas (tx) question banks to >=50 each in questions.js.
Keeps existing questions, adds new ones, and upgrades weak TX explanations.
Does NOT touch other states. Re-runs of this script are idempotent on counts.
"""
import re, json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
JS = os.path.join(ROOT, "questions.js")

js = open(JS).read()
m = re.search(r'window\.QUESTIONS\s*=\s*(\{.*\})\s*;?\s*$', js, re.S)
data = json.loads(m.group(1))

# ---- NEW VIRGINIA QUESTIONS (adds on top of existing 25 -> 55) ----
va_new = [
 {"q":"In Virginia, what is the basic speed rule?",
  "options":["You must drive at a speed that is reasonable and prudent for conditions","Always at the posted limit regardless of weather","As fast as the car behind you allows"],
  "answer":0,"ref":"VA Driver Manual - Speed","explanation":"Virginia uses the basic speed rule: never drive faster than is reasonable and prudent for current conditions, even below the posted limit."},
 {"q":"What is Virginia's default speed limit in a business or residential district unless posted otherwise?",
  "options":["25 mph","35 mph","45 mph"],"answer":0,"ref":"VA Driver Manual - Speed","explanation":"Unless signs say otherwise, the limit is 25 mph in business and residential areas."},
 {"q":"Under Virginia law, you can be charged with reckless driving for exceeding the limit by how much?",
  "options":["20 mph or more above the limit, or over 85 mph","Any amount over the limit","Only over 100 mph"],"answer":0,"ref":"VA Reckless Driving","explanation":"Reckless driving includes driving 20 mph or more above the limit or faster than 85 mph, regardless of the posted limit."},
 {"q":"What is the minimum age for a Virginia learner's permit (driver's license)?",
  "options":["15 years and 6 months","14 years","16 years"],"answer":0,"ref":"VA Licensing","explanation":"Virginia issues a learner's permit at age 15 years and 6 months."},
 {"q":"A Virginia driver with a learner's permit must be accompanied by a licensed driver who is at least:",
  "options":["21 years old","16 years old","18 years old"],"answer":0,"ref":"VA Licensing","explanation":"A licensed driver age 21 or older must supervise a permit holder."},
 {"q":"When must Virginia headlights be on?",
  "options":["From sunset to sunrise and in low visibility","Only on highways","Never in city"],"answer":0,"ref":"VA Lights","explanation":"Use headlights from sunset to sunrise and whenever you cannot see 500 feet ahead."},
 {"q":"In Virginia, a right turn on red is allowed unless:",
  "options":["A sign prohibits it or it is unsafe","Always prohibited","Only in rural areas"],"answer":0,"ref":"VA Turns","explanation":"You may turn right on red after stopping, unless a sign forbids it or cross traffic is present."},
 {"q":"What is the legal BAC limit for drivers 21 and older in Virginia?",
  "options":["0.08%","0.05%","0.00%"],"answer":0,"ref":"VA DUI","explanation":"For drivers 21+, the limit is 0.08% BAC; lower for younger/novice drivers."},
 {"q":"Virginia's 'Move Over' law requires you to:",
  "options":["Move over or slow down for stopped emergency/utility vehicles","Speed up to pass","Ignore them"],"answer":0,"ref":"VA Move Over","explanation":"You must move over one lane or slow to a safe speed when approaching stopped emergency, tow or utility vehicles."},
 {"q":"When approaching a school bus with flashing red lights on a two-lane road you must:",
  "options":["Stop in both directions","Pass slowly","Only stop if behind it"],"answer":0,"ref":"VA School Bus","explanation":"On a two-lane road all traffic must stop for a school bus with flashing red lights."},
 {"q":"What should you do at a steady red traffic signal?",
  "options":["Stop, then turn right if safe (unless signed otherwise)","Go immediately","Stop only if turning left"],"answer":0,"ref":"VA Signals","explanation":"A red light means stop; a right turn after stopping is allowed unless posted otherwise."},
 {"q":"A yellow (amber) traffic signal means:",
  "options":["Stop if you can do so safely","Accelerate","Always go"],"answer":0,"ref":"VA Signals","explanation":"Amber warns the light is changing; stop if you can safely, otherwise clear the intersection."},
 {"q":"In Virginia, following too closely (tailgating) is:",
  "options":["Illegal and a traffic infraction","Allowed in fast lanes","Only illegal at night"],"answer":0,"ref":"VA Following","explanation":"You must keep a safe distance; tailgating is an infraction that raises crash risk."},
 {"q":"What is the penalty risk for driving without insurance in Virginia?",
  "options":["Fines, license suspension, and uninsured motorist fee","None","Only a warning"],"answer":0,"ref":"VA Insurance","explanation":"Virginia requires insurance or payment of an uninsured motorist fee; driving uninsured risks fines and suspension."},
 {"q":"When parking downhill with a curb you should turn your wheels:",
  "options":["Toward the curb","Away from the curb","Straight"],"answer":0,"ref":"VA Parking","explanation":"Turn wheels toward the curb so the car rolls into it if it moves."},
 {"q":"A solid white line on the road means:",
  "options":["You should not change lanes","You may pass freely","It is a bike lane"],"answer":0,"ref":"VA Markings","explanation":"Solid white lines separate lanes where lane changes are discouraged or prohibited."},
 {"q":"What does a round sign with a red ring and a white horizontal bar mean?",
  "options":["Do not enter","Yield","Stop"],"answer":0,"ref":"VA Signs","explanation":"The round red-and-white bar is the 'do not enter' sign."},
 {"q":"In Virginia, child passengers must be in an approved restraint until what age?",
  "options":["8 years old (and 4'9\" tall)","2 years old","12 years old"],"answer":0,"ref":"VA Child Safety","explanation":"Children must use a proper car seat/booster until age 8 or 4 feet 9 inches tall."},
 {"q":"What is the speed limit in a school zone when children are present?",
  "options":["25 mph","45 mph","35 mph"],"answer":0,"ref":"VA School Zone","explanation":"School zone limits drop to 25 mph when children are present."},
 {"q":"When two vehicles reach an uncontrolled intersection at the same time, who yields?",
  "options":["The driver on the left yields to the right","The driver on the right yields","Larger vehicle"],"answer":0,"ref":"VA Right of Way","explanation":"At an uncontrolled intersection, yield to the vehicle on your right."},
 {"q":"A flashing yellow traffic signal means:",
  "options":["Proceed with caution","Stop fully","Speed up"],"answer":0,"ref":"VA Signals","explanation":"Flashing yellow means slow down and proceed with caution."},
 {"q":"In Virginia, you may not text or email while driving:",
  "options":["True, it is prohibited for all drivers","Only for learners","Only at night"],"answer":0,"ref":"VA Distraction","explanation":"Handheld texting/emailing is banned for all drivers; use hands-free if needed."},
 {"q":"What should you do if your car starts to hydroplane?",
  "options":["Ease off the accelerator and steer straight","Brake hard","Turn sharply"],"answer":0,"ref":"VA Weather","explanation":"Hydroplaning means tyres ride on water; ease off the gas and keep the wheel straight."},
 {"q":"A green arrow with a red light means:",
  "options":["You may go only in the arrow direction","Go straight","Stop"],"answer":0,"ref":"VA Signals","explanation":"A green arrow permits movement only in that direction, even if the main light is red."},
 {"q":"What is the minimum tread depth for tyres in Virginia?",
  "options":["2/32 of an inch","1/16 of an inch","1/4 of an inch"],"answer":0,"ref":"VA Vehicle","explanation":"Tyres must have at least 2/32 inch tread to be legal and safe."},
 {"q":"When approaching a railroad crossing with flashing lights you must:",
  "options":["Stop and wait until lights stop","Look both ways then go","Speed up"],"answer":0,"ref":"VA Rail","explanation":"Flashing lights mean a train is coming; stop and wait until it is safe."},
 {"q":"In Virginia, a driver under 18 with a provisional license may not drive between:",
  "options":["Midnight and 4 a.m. without exception","6 a.m. and 8 p.m.","No restriction"],"answer":0,"ref":"VA Licensing","explanation":"Provisional drivers under 18 face a curfew from midnight to 4 a.m."},
 {"q":"What does a pentagon-shaped (house) sign indicate?",
  "options":["A school zone or crossing","A hospital","A curve"],"answer":0,"ref":"VA Signs","explanation":"The yellow pentagon warns of a school area and child pedestrians."},
 {"q":"When merging onto a highway you should:",
  "options":["Match the speed of traffic and merge safely","Stop at the end of the ramp","Force your way in"],"answer":0,"ref":"VA Merging","explanation":"Build speed on the ramp and merge with a safe gap in traffic."},
 {"q":"What is the purpose of an advisory speed sign on a curve?",
  "options":["A suggested safe speed for that curve","A legal maximum","A minimum speed"],"answer":0,"ref":"VA Signs","explanation":"Advisory speeds are recommended for safe travel through curves or ramps."},
 {"q":"If you are involved in a crash you must:",
  "options":["Stop, help the injured, and report it","Drive away if minor","Hide"],"answer":0,"ref":"VA Crashes","explanation":"You must stop, aid the injured and report the crash to police if required."},
 {"q":"A blue sign with a large 'H' indicates:",
  "options":["A hospital / medical service","A highway","A hazard"],"answer":0,"ref":"VA Signs","explanation":"Blue service signs point to hospitals, gas and assistance."},
 {"q":"In Virginia, you must yield to a pedestrian:",
  "options":["In any crosswalk, marked or unmarked","Only at lights","Never"],"answer":0,"ref":"VA Pedestrians","explanation":"Pedestrians in crosswalks have the right of way; stop and let them cross."}
]

# ---- NEW TEXAS QUESTIONS (adds on top of existing 10 -> 55, explanations upgraded) ----
tx_new = [
 {"q":"What is the maximum speed limit in an urban district (unless otherwise posted) in Texas?",
  "options":["30 mph","45 mph","55 mph"],"answer":0,"ref":"TX Driver Handbook - Speed","explanation":"Texas sets the default urban district limit at 30 mph unless a sign shows otherwise."},
 {"q":"On most Texas highways outside urban districts the default speed limit is:",
  "options":["70 mph","55 mph","45 mph"],"answer":0,"ref":"TX Speed","explanation":"Many rural highways default to 70 mph, and some to 75 mph whereposted."},
 {"q":"Texas uses which side of the road?",
  "options":["Right-hand side","Left-hand side","Either"],"answer":0,"ref":"TX Rules","explanation":"Texas, like the rest of the US, drives on the right; overtake on the left."},
 {"q":"What is the legal BAC limit for adult drivers in Texas?",
  "options":["0.08%","0.05%","0.00%"],"answer":0,"ref":"TX DUI","explanation":"For drivers 21+, the limit is 0.08% BAC; zero for minors."},
 {"q":"A Texas driver under 21 with any detectable alcohol (DUI minor) faces:",
  "options":["A fine, license suspension and possible jail","No penalty","Only a warning"],"answer":0,"ref":"TX DUI","explanation":"Texas has zero tolerance for under-21 drinking and driving."},
 {"q":"When may you turn right on red in Texas?",
  "options":["After a full stop, if no sign prohibits it","Never","Only on highways"],"answer":0,"ref":"TX Turns","explanation":"Turn right after stopping unless a sign forbids it and the way is clear."},
 {"q":"A steady red light means:",
  "options":["Stop and wait for green","Go if no police","Slow down"],"answer":0,"ref":"TX Signals","explanation":"Red means stop behind the line until the light is green."},
 {"q":"A flashing yellow light means:",
  "options":["Proceed with caution","Stop fully","Speed up"],"answer":0,"ref":"TX Signals","explanation":"Flashing yellow tells you to slow and go carefully."},
 {"q":"At a 4-way stop, who goes first?",
  "options":["The first driver to stop","The largest vehicle","Whoever honks"],"answer":0,"ref":"TX Right of Way","explanation":"At a 4-way stop, the first to arrive proceeds first; if tied, yield right."},
 {"q":"When two cars reach an intersection at the same time, who yields?",
  "options":["The driver on the left yields to the right","The driver on the right yields","Nobody"],"answer":0,"ref":"TX Right of Way","explanation":"Yield to the vehicle on your right at an uncontrolled intersection."},
 {"q":"Texas 'Move Over' law requires drivers to:",
  "options":["Move over or slow down for stopped emergency vehicles","Speed past","Ignore them"],"answer":0,"ref":"TX Move Over","explanation":"Move over a lane or slow down for stopped police, fire, EMS and tow trucks."},
 {"q":"You must stop for a school bus with flashing red lights:",
  "options":["In both directions unless divided by a barrier","Only if behind it","Never on highways"],"answer":0,"ref":"TX School Bus","explanation":"On undivided roads all traffic stops; on divided roads only same-direction traffic stops."},
 {"q":"The minimum learner permit age in Texas is:",
  "options":["15 years","14 years","16 years"],"answer":0,"ref":"TX Licensing","explanation":"Texas issues a learner license at 15 (with driver education)."},
 {"q":"A Texas teen with a learner license must be supervised by a licensed driver aged at least:",
  "options":["21 years","16 years","18 years"],"answer":0,"ref":"TX Licensing","explanation":"A licensed driver 21+ must ride in the front seat with a learner."},
 {"q":"Texas requires headlights from:",
  "options":["30 minutes after sunset to 30 before sunrise","Noon only","Never"],"answer":0,"ref":"TX Lights","explanation":"Use headlights from dusk to dawn and in poor visibility."},
 {"q":"When parking downhill with a curb, turn your wheels:",
  "options":["Toward the curb","Away from the curb","Straight"],"answer":0,"ref":"TX Parking","explanation":"Curb the front wheels so the car rolls into the curb if it moves."},
 {"q":"A solid yellow line on your side of the centre means:",
  "options":["No passing","Pass freely","Bus lane"],"answer":0,"ref":"TX Markings","explanation":"A solid yellow on your side prohibits crossing to pass."},
 {"q":"A broken white line separates:",
  "options":["Lanes of traffic moving the same direction","Opposite directions","A bike lane"],"answer":0,"ref":"TX Markings","explanation":"Broken white lines separate same-direction lanes; change with care."},
 {"q":"What does a red octagonal sign mean?",
  "options":["Stop","Yield","Speed limit"],"answer":0,"ref":"TX Signs","explanation":"The red octagon is the STOP sign; stop fully at the line."},
 {"q":"What does a red triangle with an exclamation mark warn of?",
  "options":["A hazard ahead","A stop","A hospital"],"answer":0,"ref":"TX Signs","explanation":"Red triangles warn of hazards such as curves or crossings."},
 {"q":"What does a yellow diamond sign indicate?",
  "options":["A warning of a specific hazard","A speed limit","A direction"],"answer":0,"ref":"TX Signs","explanation":"Diamond signs warn of road hazards like deer or bumps."},
 {"q":"A green sign gives:",
  "options":["Direction and distance information","Warnings","Stops"],"answer":0,"ref":"TX Signs","explanation":"Green signs guide with route numbers and destinations."},
 {"q":"What does a flashing red light at a crossing mean?",
  "options":["Stop, then go when safe","Slow down","Ignore"],"answer":0,"ref":"TX Signals","explanation":"Flashing red is treated like a stop sign."},
 {"q":"When approaching a railroad crossing with flashing lights you must:",
  "options":["Stop and wait until safe","Look then go quickly","Speed up"],"answer":0,"ref":"TX Rail","explanation":"Stop for flashing lights or a descending gate; trains cannot stop quickly."},
 {"q":"If your vehicle breaks down on a highway you should:",
  "options":["Pull off the road, use hazard lights, call for help","Stand in the lane","Keep driving"],"answer":0,"ref":"TX Breakdown","explanation":"Get off the roadway, warn others and call for assistance."},
 {"q":"You must yield to pedestrians:",
  "options":["In crosswalks and at intersections","Only on green","Never"],"answer":0,"ref":"TX Pedestrians","explanation":"Pedestrians in crosswalks have the right of way."},
 {"q":"Texas child passengers must use an approved restraint until:",
  "options":["8 years old or 4'9\" tall","2 years old","12 years old"],"answer":0,"ref":"TX Child Safety","explanation":"Children need a car seat or booster until age 8 or 4'9\"."},
 {"q":"What is the speed limit in a Texas school zone when active?",
  "options":["20 mph (or as posted)","45 mph","35 mph"],"answer":0,"ref":"TX School Zone","explanation":"School zones drop to 20 mph (or posted) when children are present/lights flash."},
 {"q":"When being passed you should:",
  "options":["Keep your speed and stay right","Speed up","Move left"],"answer":0,"ref":"TX Overtaking","explanation":"Don't speed up; hold steady and let the passer finish."},
 {"q":"A vehicle turning left must yield to:",
  "options":["Oncoming traffic going straight","Pedestrians only","Nobody"],"answer":0,"ref":"TX Turns","explanation":"A left turn crosses oncoming traffic, so yield to straight-moving vehicles."},
 {"q":"What should you do in heavy fog?",
  "options":["Slow down and use low beams","Use high beams","Speed up"],"answer":0,"ref":"TX Weather","explanation":"Low beams cut glare in fog; high beams reflect back."},
 {"q":"If you skid on a wet road you should:",
  "options":["Steer gently toward where you want to go","Brake hard","Accelerate"],"answer":0,"ref":"TX Weather","explanation":"Ease off and steer smoothly; avoid hard braking."},
 {"q":"In Texas, using a handheld phone while driving is banned for:",
  "options":["Drivers in school zones and bus operators, and texting is banned for all","Nobody","Only learners"],"answer":0,"ref":"TX Distraction","explanation":"Handheld use is restricted in school zones and for bus drivers; texting is banned for all."},
 {"q":"When parking on a hill without a curb you should turn wheels:",
  "options":["Toward the side of the road","Toward traffic","Straight"],"answer":0,"ref":"TX Parking","explanation":"Turn wheels toward the shoulder so the car rolls off the road, not into it."},
 {"q":"What is the purpose of an advisory curve speed sign?",
  "options":["A safe suggested speed for the curve","A legal maximum","A minimum"],"answer":0,"ref":"TX Signs","explanation":"Advisory speeds recommend a safe pace through curves and ramps."},
 {"q":"A blue sign with an 'H' shows:",
  "options":["Hospital / medical services","Highway","Hazard"],"answer":0,"ref":"TX Signs","explanation":"Blue service signs point to hospitals and help."},
 {"q":"If you are in a collision you must:",
  "options":["Stop, help and exchange information","Leave if minor","Hide"],"answer":0,"ref":"TX Crashes","explanation":"Stop, check for injuries, call 911 if needed and swap details."},
 {"q":"A round sign with a red ring and white bar means:",
  "options":["Do not enter","Yield","Stop"],"answer":0,"ref":"TX Signs","explanation":"The round red-and-white bar is a 'do not enter' sign."},
 {"q":"When a traffic signal is dark (power out) you should treat it as:",
  "options":["A 4-way stop","A green light","Ignore it"],"answer":0,"ref":"TX Signals","explanation":"A dark signal is treated like a stop sign; proceed when safe."},
 {"q":"Texas minimum tyre tread depth is:",
  "options":["2/32 of an inch","1/8 of an inch","1/2 inch"],"answer":0,"ref":"TX Vehicle","explanation":"Tyres must have at least 2/32 inch tread to be legal."},
 {"q":"When merging onto a freeway you should:",
  "options":["Accelerate on the ramp and merge with a gap","Stop at the end","Force in"],"answer":0,"ref":"TX Merging","explanation":"Build speed on the ramp and merge smoothly with traffic."},
 {"q":"A flashing yellow arrow means:",
  "options":["Left turn permitted after yielding","Stop","Go straight"],"answer":0,"ref":"TX Signals","explanation":"A flashing yellow arrow allows a left turn after yielding to oncoming traffic."},
 {"q":"In Texas, headlights must also be on when:",
  "options":["Wipers are in use (if required by local rule) or low visibility","Only at night","Never"],"answer":0,"ref":"TX Lights","explanation":"Use lights whenever visibility is poor, including heavy rain."},
 {"q":"What does a white rectangular sign with black letters usually give?",
  "options":["A regulation or instruction","A warning","A direction only"],"answer":0,"ref":"TX Signs","explanation":"White rectangular signs state laws and regulations."},
 {"q":"When sharing the road with a large truck you should:",
  "options":["Avoid its blind spots and give room","Tailgate","Cut in front closely"],"answer":0,"ref":"TX Large Vehicles","explanation":"Trucks have big blind spots and long stopping distances; don't linger beside them."}
]

# Upgrade weak TX explanations (only those that are just a reference) - map by question text
tx_upgrade = {
 "What is the maximum speed limit in an urban district (unless otherwise posted) in Texas?":
   "TX Driver Handbook - Chapter 8: the default urban district limit is 30 mph unless posted otherwise."
}

# Apply
va_existing = data["va"]["questions"]
va_texts = {q["q"].strip().lower() for q in va_existing}
added_va = 0
for q in va_new:
    if q["q"].strip().lower() not in va_texts:
        va_existing.append(q); added_va += 1; va_texts.add(q["q"].strip().lower())

tx_existing = data["tx"]["questions"]
tx_texts = {q["q"].strip().lower() for q in tx_existing}
# upgrade weak explanations first
for q in tx_existing:
    if q["q"] in tx_upgrade and len(q.get("explanation","").strip()) < 40:
        q["explanation"] = tx_upgrade[q["q"]]
added_tx = 0
for q in tx_new:
    if q["q"].strip().lower() not in tx_texts:
        tx_existing.append(q); added_tx += 1; tx_texts.add(q["q"].strip().lower())

# Write back (pretty, preserve structure)
out = "window.QUESTIONS = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
open(JS, "w").write(out)
print(f"VA: {len(va_existing)} questions (added {added_va})")
print(f"TX: {len(tx_existing)} questions (added {added_tx})")
