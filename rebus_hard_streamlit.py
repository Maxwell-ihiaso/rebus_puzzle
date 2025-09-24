
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io, random, re
from typing import List, Dict, Any

def get_font(size: int):
    for name in ["DejaVuSans.ttf", "Arial.ttf", "LiberationSans-Regular.ttf"]:
        try:
            return ImageFont.truetype(name, size=size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_canvas(layout: List[Dict[str, Any]], w: int = 1100, h: int = 650, bg="#0b1220", fg="#e7edf7"):
    img = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((10, 10, w-10, h-10), radius=24, outline=fg, width=2)

    for it in layout:
        if "shape" in it:
            sh = it["shape"]
            if sh == "line":
                x1, y1, x2, y2 = it.get("xyxy", [100, 100, 100, 200])
                width = it.get("width", 4)
                color = it.get("color", fg)
                dashed = it.get("dashed", False)
                if not dashed:
                    d.line((x1, y1, x2, y2), fill=color, width=width)
                else:
                    dash_len, gap = 16, 10
                    dx, dy = x2-x1, y2-y1
                    dist = max(1, int((dx*dx + dy*dy) ** 0.5))
                    steps = max(1, dist // (dash_len + gap))
                    for i in range(steps+1):
                        t0 = i / (steps+1)
                        t1 = min(1, t0 + dash_len / max(1, dist))
                        sx = int(x1 + dx * t0); sy = int(y1 + dy * t0)
                        ex = int(x1 + dx * t1); ey = int(y1 + dy * t1)
                        d.line((sx, sy, ex, ey), fill=color, width=width)
            elif sh == "box":
                x1, y1, x2, y2 = it.get("xyxy", [300, 200, 800, 480])
                width = it.get("width", 4)
                color = it.get("color", fg)
                radius = it.get("radius", 18)
                dashed = it.get("dashed", False)
                if dashed:
                    dash_len, gap = 18, 12
                    x = x1
                    while x < x2:
                        d.line((x, y1, min(x+dash_len, x2), y1), fill=color, width=width); x += dash_len + gap
                    x = x1
                    while x < x2:
                        d.line((x, y2, min(x+dash_len, x2), y2), fill=color, width=width); x += dash_len + gap
                    y = y1
                    while y < y2:
                        d.line((x1, y, x1, min(y+dash_len, y2)), fill=color, width=width); y += dash_len + gap
                    y = y1
                    while y < y2:
                        d.line((x2, y, x2, min(y+dash_len, y2)), fill=color, width=width); y += dash_len + gap
                else:
                    d.rounded_rectangle((x1, y1, x2, y2), radius=radius, outline=color, width=width)
            continue

        text = it.get("text", "")
        size = it.get("size", 64)
        font = get_font(size)
        x, y = it.get("xy", [w//2, h//2])
        align = it.get("align", "center")
        color = it.get("color", fg)
        rotate = it.get("rotate", 0)
        underline = it.get("underline", False)

        bbox = font.getbbox(text)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        if align == "center":
            tx, ty = x - tw//2, y - th//2
        elif align == "left":
            tx, ty = x, y - th//2
        else:
            tx, ty = x - tw, y - th//2

        if it.get("box"):
            pad = it["box"].get("pad", 16)
            rx1, ry1 = tx - pad, ty - pad
            rx2, ry2 = tx + tw + pad, ty + th + pad
            radius = it["box"].get("radius", 12)
            out = it["box"].get("outline", color)
            fill = it["box"].get("fill", None)
            width = it["box"].get("width", 2)
            dashed = it["box"].get("dashed", False)
            if dashed:
                dash_len, gap = 14, 10
                x0 = rx1
                while x0 < rx2:
                    d.line((x0, ry1, min(x0+dash_len, rx2), ry1), fill=out, width=width); x0 += dash_len + gap
                x0 = rx1
                while x0 < rx2:
                    d.line((x0, ry2, min(x0+dash_len, rx2), ry2), fill=out, width=width); x0 += dash_len + gap
                y0 = ry1
                while y0 < ry2:
                    d.line((rx1, y0, rx1, min(y0+dash_len, ry2)), fill=out, width=width); y0 += dash_len + gap
                y0 = ry1
                while y0 < ry2:
                    d.line((rx2, y0, rx2, min(y0+dash_len, ry2)), fill=out, width=width); y0 += dash_len + gap
            else:
                d.rounded_rectangle((rx1, ry1, rx2, ry2), radius=radius, outline=out, width=width, fill=fill)

        txt = Image.new("RGBA", (tw+4, th+40), (0,0,0,0))
        ImageDraw.Draw(txt).text((2,2), text, font=font, fill=color)
        if underline:
            ImageDraw.Draw(txt).line((0, th+1, tw, th+1), fill=color, width=max(2, size//16))
        if rotate:
            txt = txt.rotate(rotate, expand=True)
        img.paste(txt, (int(tx), int(ty)), txt)

    return img

import re
def normalize(s: str) -> str:
    return re.sub(r"[^a-z]", "", s.lower())

PUZZLES = [
    {"id":"mind_over_matter","answer":"Mind Over Matter","hint":"One word over another.","layout":[
        {"text":"MIND","xy":[550,240],"size":110},
        {"text":"MATTER","xy":[550,400],"size":110,"color":"#94a3b8"}
    ]},
    {"id":"reading_between_lines","answer":"Reading Between the Lines","hint":"Look carefully at the lines.","layout":[
        {"shape":"line","xyxy":[220,220,880,220],"width":4,"color":"#94a3b8"},
        {"text":"READING","xy":[550,320],"size":108},
        {"shape":"line","xyxy":[220,420,880,420],"width":4,"color":"#94a3b8"}
    ]},
    {"id":"back_to_square_one","answer":"Back to Square One","hint":"Return to the starting point.","layout":[
        {"text":"◀ back","xy":[340,180],"size":54,"color":"#94a3b8","align":"left"},
        {"text":"ONE","xy":[550,330],"size":120},
        {"shape":"box","xyxy":[470,280,630,400],"width":5}
    ]},
    {"id":"head_over_heels","answer":"Head Over Heels","hint":"Orientation matters.","layout":[
        {"text":"HEAD","xy":[550,240],"size":110},
        {"text":"HEELS","xy":[550,430],"size":110,"rotate":180}
    ]},
    {"id":"once_in_a_blue_moon","answer":"Once in a Blue Moon","hint":"A color + a rarity.","layout":[
        {"text":"ONCE","xy":[360,280],"size":86,"color":"#94a3b8"},
        {"text":"MOON","xy":[560,330],"size":128},
        {"text":"BLUE","xy":[760,380],"size":86,"color":"#94a3b8"}
    ]},
    {"id":"time_flies","answer":"Time Flies","hint":"Up and away.","layout":[
        {"text":"TIME","xy":[500,320],"size":130},
        {"text":"↗ ↗ ↗","xy":[700,240],"size":80,"color":"#94a3b8"}
    ]},
    {"id":"man_overboard","answer":"Man Overboard","hint":"Over + thing you stand on.","layout":[
        {"text":"MAN","xy":[550,260],"size":110},
        {"text":"BOARD","xy":[550,420],"size":110}
    ]},
    {"id":"down_to_earth","answer":"Down to Earth","hint":"Follow the arrow.","layout":[
        {"text":"DOWN","xy":[550,240],"size":110},
        {"text":"↓","xy":[550,310],"size":90,"color":"#94a3b8"},
        {"text":"EARTH","xy":[550,400],"size":110}
    ]},
    {"id":"touchdown","answer":"Touchdown","hint":"Sports finish line vibe.","layout":[
        {"text":"TOUCH","xy":[550,260],"size":120},
        {"text":"↓","xy":[550,360],"size":110,"color":"#94a3b8"}
    ]},
    {"id":"small_talk","answer":"Small Talk","hint":"Check the scale.","layout":[
        {"text":"talk","xy":[550,330],"size":56}
    ]},
    {"id":"split_decision","answer":"Split Decision","hint":"It's divided.","layout":[
        {"text":"DECI|SION","xy":[550,330],"size":120}
    ]},
    {"id":"missing_you","answer":"Missing You","hint":"There's a gap.","layout":[
        {"text":"YO _","xy":[550,330],"size":140}
    ]},
    {"id":"undercover","answer":"Undercover","hint":"Someone is hiding.","layout":[
        {"text":"COVER","xy":[550,280],"size":120},
        {"text":"me","xy":[550,420],"size":88,"color":"#94a3b8"}
    ]},
    {"id":"turn_back_time","answer":"Turn Back Time","hint":"Reverse it.","layout":[
        {"text":"TIME","xy":[550,330],"size":120,"rotate":180},
        {"text":"BACK ◀","xy":[380,260],"size":72,"color":"#94a3b8","align":"left"}
    ]},
    {"id":"uphill_battle","answer":"Uphill Battle","hint":"A struggle on a slope.","layout":[
        {"text":"BATTLE","xy":[700,420],"size":110},
        {"shape":"line","xyxy":[280,480,820,240],"width":6,"color":"#94a3b8","dashed":True}
    ]},
    {"id":"long_story_short","answer":"Long Story Short","hint":"Length is the clue.","layout":[
        {"text":"STOOOOORY","xy":[550,300],"size":110},
        {"text":"short","xy":[740,400],"size":64,"color":"#94a3b8","align":"left"}
    ]},
    {"id":"elephant_in_room","answer":"The Elephant in the Room","hint":"Something obvious but ignored.","layout":[
        {"shape":"box","xyxy":[400,260,800,480],"width":4},
        {"text":"elephant","xy":[600,370],"size":64,"color":"#94a3b8"}
    ]},
    {"id":"cut_corners","answer":"Cut Corners","hint":"The shape isn't complete.","layout":[
        {"shape":"line","xyxy":[320,260,780,260],"width":5},
        {"shape":"line","xyxy":[320,520,780,520],"width":5},
        {"shape":"line","xyxy":[320,260,320,330],"width":5},
        {"shape":"line","xyxy":[780,260,780,330],"width":5},
        {"shape":"line","xyxy":[320,450,320,520],"width":5},
        {"shape":"line","xyxy":[780,450,780,520],"width":5}
    ]},
    {"id":"out_of_order","answer":"Out of Order","hint":"Scrambled.","layout":[
        {"text":"ou","xy":[150,330],"size":130},
        {"text":"t","xy":[550,530],"size":130},
        {"text":"OD RE R","xy":[550,330],"size":130},
        {"text":"out","xy":[700,460],"size":56,"color":"#94a3b8","align":"left"},
        {"text":"o u t","xy":[700,60],"size":56,"color":"#94a3b8","align":"left"}
    ]},
    {"id":"edge_case","answer":"Edge Case","hint":"Look to the margin.","layout":[
        {"text":"CASE","xy":[1060,340],"size":120,"align":"right"}
    ]},
    {"id":"rising_costs","answer":"Rising Costs","hint":"Climb.","layout":[
        {"text":"c o s t s","xy":[550,480],"size":90},
        {"text":"COSTS","xy":[550,360],"size":100},
        {"text":"COSTS","xy":[550,260],"size":110}
    ]},
    {"id":"on_the_fence","answer":"On the Fence","hint":"Perched.","layout":[
        {"text":"Sitting","xy":[550,260],"size":110},
        {"text":"--------","xy":[550,260],"size":110},
        {"text":"||||| FENCE |||||","xy":[550,380],"size":86}
    ]},
    {"id":"bottleneck","answer":"Bottleneck","hint":"A tight spot.","layout":[
        {"text":"BOTTLE","xy":[550,280],"size":120},
        {"text":"NECK","xy":[550,420],"size":88,"color":"#94a3b8"}
    ]},
    {"id":"penny_for_your_thoughts","answer":"Penny for Your Thoughts","hint":"Symbolic currency.","layout":[
        {"text":"¢   →   THOUGHTS","xy":[550,330],"size":112}
    ]},
    {"id":"food_for_thought_hard","answer":"Food for Thought","hint":"Letters, spacing, and a small word.","layout":[
        {"text":"F  O  O  D","xy":[430,260],"size":110,"align":"left"},
        # {"text":"for","xy":[550,330],"size":60,"color":"#94a3b8"},
        {"text":"TH( )UGHT","xy":[650,410],"size":100,"align":"right"}
    ]},
    {"id":"underestimate","answer":"Underestimate","hint":"Below the mark.","layout":[
        {"shape":"line","xyxy":[260,300,840,300],"width":5},
        {"text":"ESTIMATE","xy":[550,400],"size":120}
    ]},
    {"id":"connection_lost","answer":"Connection Lost","hint":"Mind the gap.","layout":[
        {"text":"CONNECT   — — —   ION","xy":[550,330],"size":100}
    ]},
    # {"id":"couch_potato","answer":"Couch Potato","hint":"One on another.","layout":[
    #     {"text":"COUCH","xy":[550,280],"size":120,"color":"#94a3b8"},
    #     {"text":"POTATO","xy":[550,420],"size":120}
    # ]},
    {"id":"hold_on","answer":"Hold On","hint":"Grip.","layout":[
        {"text":"[HOLD]   ON","xy":[550,330],"size":120}
    ]},
    {"id":"brain_freeze","answer":"Brain Freeze","hint":"Chilly upstairs.","layout":[
        {"text":"B  R  A  I  N","xy":[550,280],"size":110},
        {"text":"* * * * *","xy":[550,350],"size":70,"color":"#94a3b8"},
        {"text":"COLD","xy":[550,430],"size":110}
    ]},
    {"id":"thinking_cap","answer":"Thinking Cap","hint":"Headwear helps.","layout":[
        {"text":"CAP","xy":[550,260],"size":100},
        {"text":"THINKING","xy":[550,400],"size":110},
        {"shape":"line","xyxy":[390,360,710,360],"width":6,"color":"#94a3b8"}
    ]},
    {"id":"go_back_square_one","answer":"Go Back to Square One","hint":"Return to 1.","layout":[
        {"text":"GO  ◀","xy":[370,230],"size":66,"color":"#94a3b8","align":"left"},
        {"text":"1","xy":[550,335],"size":140},
        {"shape":"box","xyxy":[510,295,590,375],"width":5}
    ]},
    {"id":"silence_is_golden","answer":"Silence is Golden","hint":"Chemical hint.","layout":[
        {"text":"SILENCE","xy":[550,300],"size":110,"color":"#94a3b8"},
        {"text":"Au","xy":[550,400],"size":110}
    ]},
    {"id":"lost_in_translation","answer":"Lost in Translation","hint":"One word disappears.","layout":[
        {"text":"TRANSLATION","xy":[550,320],"size":120},
        {"text":"lost","xy":[420,360],"size":54,"color":"#94a3b8","align":"left"}
    ]},
    {"id":"no_idea","answer":"No Idea","hint":"A null of sorts.","layout":[
        {"text":"∅","xy":[470,300],"size":120,"color":"#94a3b8"},
        {"text":"IDEA","xy":[650,320],"size":120,"align":"left"}
    ]},
    {"id":"space_invader","answer":"Space Invader","hint":"Plenty of gaps.","layout":[
        # {"text":"S    P    A    C    E","xy":[550,300],"size":96},
        {"text":"I  N  V  A  D  E  R","xy":[550,400],"size":110}
    ]},
    {"id":"upper_hand","answer":"Upper Hand","hint":"Position matters.","layout":[
        {"text":"HAND","xy":[550,220],"size":110},
        {"text":"(upper)","xy":[550,300],"size":64,"color":"#94a3b8"}
    ]},
    {"id":"mind_blown","answer":"Mind Blown","hint":"Kaboom.","layout":[
        {"text":"MIND","xy":[500,300],"size":120},
        {"text":"BOOM!","xy":[700,380],"size":100,"color":"#94a3b8"}
    ]},
    {"id":"breakthrough","answer":"Breakthrough","hint":"Going past an obstacle.","layout":[
        {"text":"WALL","xy":[430,320],"size":110},
        {"text":"BREAK →","xy":[690,330],"size":100,"color":"#94a3b8","align":"left"}
    ]},
    {"id":"under_the_radar","answer":"Under the Radar","hint":"Stay unseen.","layout":[
        {"text":"RADAR","xy":[550,280],"size":120},
        {"shape":"line","xyxy":[350,340,750,340],"width":5},
        {"text":"me","xy":[550,400],"size":90,"color":"#94a3b8"}
    ]},
    {"id":"piece_of_cake","answer":"Piece of Cake","hint":"Slice it.","layout":[
        {"text":"[  CAKE  ]","xy":[550,320],"size":110},
        {"text":"piece →","xy":[380,360],"size":64,"color":"#94a3b8","align":"left"}
    ]},
    {"id":"break_even","answer":"Break Even","hint":"Equality interrupted.","layout":[
        {"text":"==","xy":[550,320],"size":140},
        {"text":"(break)","xy":[710,320],"size":64,"color":"#94a3b8","align":"left"}
    ]},
    {"id":"cold_feet","answer":"Cold Feet","hint":"Temperature + toes.","layout":[
        {"text":"C O L D","xy":[550,250],"size":100,"color":"#94a3b8"},
        {"text":"FEET","xy":[550,400],"size":120}
    ]},
    {"id":"outnumbered","answer":"Outnumbered","hint":"Overwhelmed by digits.","layout":[
        {"text":"1 2 3 4 5 6 7 8 9 10","xy":[550,300],"size":80},
        {"text":"me","xy":[550,400],"size":80,"color":"#94a3b8"}
    ]},
    {"id":"the_last_straw","answer":"The Last Straw","hint":"Final one.","layout":[
        {"text":"STRAW STRAW STRAW STRAW","xy":[550,300],"size":70},
        {"text":"→ last","xy":[780,340],"size":60,"color":"#94a3b8","align":"left"}
    ]},
    {"id":"corner_case","answer":"Corner Case","hint":"Top-left detail.","layout":[
        {"text":"CASE","xy":[700,420],"size":110},
        {"shape":"line","xyxy":[220,240,220,300],"width":8,"color":"#94a3b8"},
        {"shape":"line","xyxy":[220,240,280,240],"width":8,"color":"#94a3b8"}
    ]},
    {"id":"crossroads","answer":"Crossroads","hint":"Intersection.","layout":[
        {"shape":"line","xyxy":[550,240,550,500],"width":8},
        {"shape":"line","xyxy":[430,370,670,370],"width":8},
        {"text":"ROAD","xy":[550,170],"size":90}
    ]},
    {"id":"burnout","answer":"Burnout","hint":"Two-part word.","layout":[
        {"text":"BURN","xy":[520,300],"size":120},
        {"text":"OUT","xy":[700,360],"size":110,"color":"#94a3b8"}
    ]},
    {"id":"underline","answer":"Underline","hint":"Placement matters.","layout":[
        {"text":"LINE","xy":[550,280],"size":120},
        {"text":"UNDER","xy":[550,400],"size":110,"color":"#94a3b8"}
    ]},
    {"id":"leftovers","answer":"Leftovers","hint":"Two sides.","layout":[
        {"text":"-->","xy":[200,330],"size":120,"align":"left"},
        {"text":"OVER","xy":[900,330],"size":120,"align":"right"}
    ]},
]

ALIASES = {
    "go back to square one": ["back to square one","return to square one"],
    "reading between the lines": ["read between the lines"],
    "once in a blue moon": ["blue moon"],
    "a/b testing": ["ab testing","a b testing"],
}

def is_correct(guess: str, answer: str) -> bool:
    g = normalize(guess)
    a = normalize(answer)
    if g == a:
        return True
    for k, vals in ALIASES.items():
        if normalize(answer) == normalize(k):
            if g in [normalize(v) for v in vals] or g == normalize(k):
                return True
    return False

st.set_page_config(page_title="Hard Rebus — 50 Puzzles", page_icon="🧩", layout="wide")

if "order" not in st.session_state:
    st.session_state.order = list(range(len(PUZZLES)))
    random.shuffle(st.session_state.order)
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "show_hint" not in st.session_state:
    st.session_state.show_hint = False
if "reveal" not in st.session_state:
    st.session_state.reveal = False

st.title("🧩 Rebus Puzzle for Renda")
st.caption("made with ❤️ by Maxwell (torchLight).")

with st.sidebar:
    st.header("Controls")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Prev", width='stretch'):
            st.session_state.idx = (st.session_state.idx - 1) % len(PUZZLES)
            st.session_state.show_hint = False; st.session_state.reveal = False
    with col2:
        if st.button("Next ➡️", width='stretch'):
            st.session_state.idx = (st.session_state.idx + 1) % len(PUZZLES)
            st.session_state.show_hint = False; st.session_state.reveal = False
    if st.button("Shuffle 🔀", width='stretch'):
        random.shuffle(st.session_state.order)
        st.session_state.idx = 0
        st.session_state.show_hint = False; st.session_state.reveal = False
    st.divider()
    if st.button(("Show Hint 🤔" if not st.session_state.show_hint else "Hide Hint 🙈"), width='stretch'):
        st.session_state.show_hint = not st.session_state.show_hint
    if st.button(("Reveal ✅" if not st.session_state.reveal else "Hide ❌"), width='stretch'):
        st.session_state.reveal = not st.session_state.reveal

p = PUZZLES[st.session_state.order[st.session_state.idx]]
img = draw_canvas(p["layout"])
buf = io.BytesIO(); img.save(buf, format="PNG")
st.image(buf.getvalue(), width='stretch')
st.caption(f"Puzzle {st.session_state.idx+1} / {len(PUZZLES)}")

if st.session_state.show_hint:
    st.info(f"**Hint:** {p['hint']}")

if st.session_state.reveal:
    st.success(f"**Answer:** {p['answer']}")

st.subheader("Your Guess")
guess = st.text_input("Type your answer:", key=f"g_{st.session_state.order[st.session_state.idx]}")
if st.button("Check"):
    if is_correct(guess, p["answer"]):
        st.balloons()
        st.success("Correct! 🎉")
    else:
        st.error("Not quite. Try again!")

st.caption("Tip: Answers ignore case/punctuation. Use sidebar to navigate / shuffle / hint / reveal.")
