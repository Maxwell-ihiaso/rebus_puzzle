
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import io
from typing import List, Dict
import os
import emoji

def get_font(size: int):
    # for name in ["NotoSans.ttf","NotoSansSymbols2-Regular.ttf","NotoEmoji.ttf","DejaVuSans.ttf", "Arial.ttf", "LiberationSans-Regular.ttf"]:
    for name in ["NotoEmoji.ttf"]:
        try:
            return ImageFont.truetype(os.path.join("fonts", name), size=size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_puzzle(layout: List[Dict], w: int = 1100, h: int = 650, bg="#0b1220", fg="#e7edf7"):
    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)
    border = 8
    draw.rounded_rectangle((border, border, w-border, h-border), radius=24, outline=fg, width=2)

    for item in layout:
        text = item.get("text", "")
        x, y = item.get("xy", [w//2, h//2])
        size = item.get("size", 64)
        rotate = item.get("rotate", 0)
        align = item.get("align", "center")
        underline = item.get("underline", False)
        box = item.get("box", None)
        dashed = item.get("dashed", False)
        opacity = item.get("opacity", 255)

        emojis_rendered = emoji.emojize(text)
        print(emojis_rendered)

        font = get_font(size)
        txtFont = ImageFont.truetype(os.path.join("fonts", "DejaVuSans.ttf"), size=size)
        bbox = font.getbbox(text)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

        if align == "center":
            tx = x - tw//2
            ty = y - th//2
        elif align == "left":
            tx = x
            ty = y - th//2
        else:
            tx = x - tw
            ty = y - th//2

        print(tw, th, tx, ty, x, y, align)


        if box:
            pad = box.get("pad", 16)
            rx1, ry1 = tx - pad, ty - pad
            rx2, ry2 = tx + tw + pad, ty + th + pad
            radius = box.get("radius", 12)
            fill = box.get("fill", None)
            outline = box.get("outline", fg)
            width = box.get("width", 2)
            if dashed:
                dash_len = 12
                gap = 8
                cur = rx1
                while cur < rx2:
                    draw.line((cur, ry1, min(cur+dash_len, rx2), ry1), fill=outline, width=width)
                    cur += dash_len + gap
                cur = rx1
                while cur < rx2:
                    draw.line((cur, ry2, min(cur+dash_len, rx2), ry2), fill=outline, width=width)
                    cur += dash_len + gap
                cur = ry1
                while cur < ry2:
                    draw.line((rx1, cur, rx1, min(cur+dash_len, ry2)), fill=outline, width=width)
                    cur += dash_len + gap
                cur = ry1
                while cur < ry2:
                    draw.line((rx2, cur, rx2, min(cur+dash_len, ry2)), fill=outline, width=width)
                    cur += dash_len + gap
            else:
                draw.rounded_rectangle((rx1, ry1, rx2, ry2), radius=radius, outline=outline, width=width, fill=fill)

        txt_img = Image.new("RGBA", (tw+4, th+80), (0,0,0,0))
        txt_draw = ImageDraw.Draw(txt_img)

        
        txt_draw.text((2,2), emojis_rendered, font=font, fill=(231,237,247))
                
        if underline:
            txt_draw.line((0, th+1, tw, th+1), fill=(231,237,247, opacity), width=max(2, size//16))
        if rotate != 0:
            txt_img = txt_img.rotate(rotate, expand=True)
        img.paste(txt_img, (int(tx), int(ty)), txt_img)
    return img

PUZZLES = [
    {"id":"food_for_thought","answer":"Food for Thought","hint":"Groceries + thinking bubbles.","layout":[
        {"text":"FOOD", "xy":[360,250], "size":100},
        {"text":"🤔 🤔 🤔 🤔", "xy":[740,250], "size":88},
        {"text":"for", "xy":[550,350], "size":64, "underline":True}
    ]},
    {"id":"brainstorming","answer":"Brainstorming","hint":"Many THINKS.","layout":[
        {"text":"THINK", "xy":[520,220], "size":86},
        {"text":"THINK", "xy":[520,300], "size":86},
        {"text":"THINK", "xy":[520,380], "size":86}
    ]},
    {"id":"user_research","answer":"User Research","hint":"Lots of USERS.","layout":[
        {"text":"USER USER USER USER", "xy":[550,300], "size":72}
    ]},
    {"id":"roadmap","answer":"Roadmap","hint":"Road over map.","layout":[
        {"text":"ROAD", "xy":[550,250], "size":92},
        {"text":"────", "xy":[550,300], "size":72},
        {"text":"MAP", "xy":[550,360], "size":92}
    ]},
    {"id":"wireframe","answer":"Wireframe","hint":"Wire around a frame.","layout":[
        {"text":"FRAME", "xy":[550,300], "size":96, "box":{"pad":24}},
        {"text":"wire wire", "xy":[550,180], "size":48, "dashed":True}
    ]},
    {"id":"feedback_loop","answer":"Feedback Loop","hint":"Comments circling","layout":[
        {"text":"💬  →  💬  →  💬  →  💬", "xy":[550,300], "size":64}
    ]},
    {"id":"prototype","answer":"Prototype","hint":"First version build.","layout":[
        {"text":"PROTO", "xy":[450,280], "size":96},
        {"text":"type", "xy":[700,320], "size":72}
    ]},
    {"id":"persona","answer":"Persona","hint":"User archetype.","layout":[
        {"text":"USER → 👤", "xy":[550,300], "size":72}
    ]},
    {"id":"usability","answer":"Usability","hint":"Use + ability.","layout":[
        {"text":"USE + ABILITY", "xy":[550,300], "size":80}
    ]},
    {"id":"design_thinking","answer":"Design Thinking","hint":"Design + brain.","layout":[
        {"text":"🎨 + 🧠", "xy":[550,300], "size":100}
    ]},
    {"id":"coffee_break","answer":"Coffee Break","hint":"☕ + split line.","layout":[
        {"text":"☕", "xy":[450,300], "size":120},
        {"text":"— — —", "xy":[650,300], "size":80}
    ]},
    {"id":"deadline","answer":"Deadline","hint":"Line at time.","layout":[
        {"text":"🕒", "xy":[500,260], "size":110},
        {"text":"────", "xy":[600,320], "size":64}
    ]},
    {"id":"stand_up","answer":"Stand-Up","hint":"Standing ↑.","layout":[
        {"text":"stand", "xy":[520,260], "size":96},
        {"text":"↑", "xy":[520,340], "size":96}
    ]},
    {"id":"meeting_overload","answer":"Meeting Overload","hint":"Too many calendars.","layout":[
        {"text":"📅 📅 📅 📅 📅", "xy":[550,300], "size":72}
    ]},
    {"id":"team_spirit","answer":"Team Spirit","hint":"People + trophy.","layout":[
        {"text":"👩‍💻👨‍🎨👨‍💻👩‍💼  +  🏆", "xy":[550,300], "size":70}
    ]},
    {"id":"remote_work","answer":"Remote Work","hint":"House + laptop.","layout":[
        {"text":"🏠  +  💻", "xy":[550,300], "size":100}
    ]},
    {"id":"multitasking","answer":"Multitasking","hint":"Doing many at once.","layout":[
        {"text":"task  task  task  task", "xy":[550,280], "size":60},
        {"text":"all at once", "xy":[550,340], "size":56}
    ]},
    {"id":"work_life_balance","answer":"Work-Life Balance","hint":"Work ↔ Life.","layout":[
        {"text":"💼  ↔  🏡", "xy":[550,300], "size":120}
    ]},
    {"id":"big_picture","answer":"Big Picture","hint":"PICTURE made BIG.","layout":[
        {"text":"PICTURE", "xy":[550,300], "size":128}
    ]},
    {"id":"keep_it_simple","answer":"Keep It Simple","hint":"SIMPLE underlined.","layout":[
        {"text":"SIMPLE", "xy":[550,300], "size":210, "underline":True}
    ]},
    {"id":"sleep_on_it","answer":"Sleep on It","hint":"Bed on the word IT.","layout":[
        {"text":"🛏", "xy":[480,280], "size":110},
        {"text":"IT", "xy":[650,320], "size":110}
    ]},
    {"id":"time_is_money","answer":"Time is Money","hint":"Clock + money.","layout":[
        {"text":"🕒 = 💰", "xy":[550,300], "size":120}
    ]},
    {"id":"outside_the_box","answer":"Think Outside the Box","hint":"Brain outside a box.","layout":[
        {"text":"[  BOX  ]      🧠", "xy":[550,300], "size":72}
    ]},
    {"id":"two_heads","answer":"Two Heads are Better than One","hint":"Two heads > one.","layout":[
        {"text":"🙂🙂  >  🙂", "xy":[550,300], "size":110}
    ]},
    {"id":"trial_and_error","answer":"Trial and Error","hint":"Try → fail → learn.","layout":[
        {"text":"TRY → ❌ → LEARN → ✅", "xy":[550,300], "size":64}
    ]},
    {"id":"leap_of_faith","answer":"Leap of Faith","hint":"Jump + cross gap.","layout":[
        {"text":"🏃‍♂️  ⟶   ⛰  ⛰", "xy":[550,300], "size":88}
    ]},
    {"id":"walk_the_talk","answer":"Walk the Talk","hint":"Footprints + speech bubble.","layout":[
        {"text":"👣  +  💬", "xy":[550,300], "size":110}
    ]},
    {"id":"lock_and_key","answer":"Lock and Key","hint":"🔒 + 🔑.","layout":[
        {"text":"🔒  +  🔑", "xy":[550,300], "size":120}
    ]},
    {"id":"mixed_emotions","answer":"Mixed Emotions","hint":"Multiple faces.","layout":[
        {"text":"😃 😐 😢 😡", "xy":[550,300], "size":96}
    ]},
    {"id":"look_closer","answer":"Look Closer","hint":"Magnifier toward text.","layout":[
        {"text":"LOOK  🔍", "xy":[550,300], "size":100}
    ]},
    {"id":"talk_of_the_town","answer":"Talk of the Town","hint":"Many chat bubbles over skyline.","layout":[
        {"text":"🏙  +  💬💬💬", "xy":[550,300], "size":88}
    ]},
    {"id":"silver_lining","answer":"Silver Lining","hint":"Cloud with a bright edge.","layout":[
        {"text":"☁︎  ✨", "xy":[550,300], "size":120}
    ]},
    {"id":"light_bulb_moment","answer":"Light-Bulb Moment","hint":"Idea popped.","layout":[
        {"text":"💡  !", "xy":[550,300], "size":120}
    ]},
    {"id":"hit_the_ground_running","answer":"Hit the Ground Running","hint":"Start fast.","layout":[
        {"text":"START  →  🏃‍♀️💨", "xy":[550,300], "size":80}
    ]},
    {"id":"under_the_weather","answer":"Under the Weather","hint":"Umbrella below clouds.","layout":[
        {"text":"☁ ☁ ☁", "xy":[550,240], "size":86},
        {"text":"☂", "xy":[550,340], "size":120}
    ]},
    {"id":"on_the_same_page","answer":"On the Same Page","hint":"Two people, one page.","layout":[
        {"text":"👥  📄", "xy":[550,300], "size":110}
    ]},
    {"id":"icebreaker","answer":"Icebreaker","hint":"Breaking ice.","layout":[
        {"text":"❄️  ———  ❄️", "xy":[550,280], "size":90},
        {"text":"🚢", "xy":[550,360], "size":90}
    ]},
    {"id":"green_light","answer":"Green Light","hint":"Traffic signal on go.","layout":[
        {"text":"🟢", "xy":[550,300], "size":128}
    ]},
    {"id":"red_flag","answer":"Red Flag","hint":"Beware sign.","layout":[
        {"text":"🚩", "xy":[550,300], "size":128}
    ]},
    {"id":"user_journey","answer":"User Journey","hint":"Path with user.","layout":[
        {"text":"👤  ——→  📱", "xy":[550,300], "size":84}
    ]},
    {"id":"ab_testing","answer":"A/B Testing","hint":"A vs B.","layout":[
        {"text":"A    vs    B", "xy":[550,300], "size":110}
    ]},
    {"id":"customer_first","answer":"Customer First","hint":"Customer before others.","layout":[
        {"text":"CUSTOMER        FIRST", "xy":[550,300], "size":84}
    ]},
    {"id":"user_feedback","answer":"User Feedback","hint":"User with speech bubble.","layout":[
        {"text":"👤  💬", "xy":[550,300], "size":120}
    ]},
    {"id":"launch_day","answer":"Launch Day","hint":"Rocket + calendar.","layout":[
        {"text":"🚀  +  📅", "xy":[550,300], "size":110}
    ]},
    {"id":"backlog","answer":"Backlog","hint":"Tasks stacked.","layout":[
        {"text":"📋\\n📋\\n📋", "xy":[550,300], "size":80}
    ]},
    {"id":"priority_queue","answer":"Priority Queue","hint":"Important item first.","layout":[
        {"text":"⭐  →  item → item → item", "xy":[550,300], "size":72}
    ]},
    {"id":"quick_win","answer":"Quick Win","hint":"Fast + trophy.","layout":[
        {"text":"⚡  +  🏆", "xy":[550,300], "size":110}
    ]},
    {"id":"north_star","answer":"North Star","hint":"Compass + star.","layout":[
        {"text":"🧭  ⭐", "xy":[550,300], "size":110}
    ]},
    {"id":"growth_mindset","answer":"Growth Mindset","hint":"Brain with up arrow.","layout":[
        {"text":"🧠  📈", "xy":[550,300], "size":110}
    ]},
    {"id":"butterflies_in_stomach","answer":"Butterflies in My Stomach","hint":"Nervous excitement.","layout":[
        {"text":"🦋🦋🦋", "xy":[550,240], "size":80},
        {"text":"🙂", "xy":[550,360], "size":100}
    ]},
    {"id":"piece_of_cake","answer":"Piece of Cake","hint":"Easy task.","layout":[
        {"text":"🍰", "xy":[550,300], "size":128}
    ]},
    {"id":"spill_the_beans","answer":"Spill the Beans","hint":"Reveal a secret.","layout":[
        {"text":"🫘🫘🫘  ⟶", "xy":[550,300], "size":96}
    ]},
    {"id":"break_the_ice","answer":"Break the Ice","hint":"Crack snowflake.","layout":[
        {"text":"❄️  💥", "xy":[550,300], "size":120}
    ]},
    {"id":"hit_the_books","answer":"Hit the Books","hint":"Study hard.","layout":[
        {"text":"📚  💥", "xy":[550,300], "size":110}
    ]},
    {"id":"under_pressure","answer":"Under Pressure","hint":"Weight squeezing.","layout":[
        {"text":"⬇️  TEXT  ⬇️", "xy":[550,300], "size":96}
    ]},
    {"id":"on_fire","answer":"On Fire","hint":"Hot streak.","layout":[
        {"text":"🔥", "xy":[550,300], "size":140}
    ]},
    {"id":"cold_feet","answer":"Cold Feet","hint":"Nervous to proceed.","layout":[
        {"text":"🦶🦶  ❄️", "xy":[550,300], "size":110}
    ]},
    {"id":"break_even","answer":"Break Even","hint":"Split equals sign.","layout":[
        {"text":"=   (break)", "xy":[550,300], "size":96}
    ]},
    {"id":"turn_the_tables","answer":"Turn the Tables","hint":"Flip the layout.","layout":[
        {"text":"TABLE", "xy":[550,300], "size":110, "rotate":180}
    ]},
]

assert len(PUZZLES) >= 50

def init_state():
    if "puzzle_order" not in st.session_state:
        st.session_state.puzzle_order = list(range(len(PUZZLES)))
        random.shuffle(st.session_state.puzzle_order)
    if "idx" not in st.session_state:
        st.session_state.idx = 0
    if "score" not in st.session_state:
        st.session_state.score = {}
    if "teams" not in st.session_state:
        st.session_state.teams = []
    if "timer_secs" not in st.session_state:
        st.session_state.timer_secs = 60
    if "show_hint" not in st.session_state:
        st.session_state.show_hint = False
    if "revealed" not in st.session_state:
        st.session_state.revealed = False

def next_puzzle():
    st.session_state.idx = (st.session_state.idx + 1) % len(PUZZLES)
    st.session_state.show_hint = False
    st.session_state.revealed = False

def prev_puzzle():
    st.session_state.idx = (st.session_state.idx - 1) % len(PUZZLES)
    st.session_state.show_hint = False
    st.session_state.revealed = False

def add_point(team_name: str):
    st.session_state.score[team_name] = st.session_state.score.get(team_name, 0) + 1

st.set_page_config(page_title="Renda Rebus Puzzle", page_icon="🧩", layout="wide")
init_state()

st.title("🧩 Renda Rebus Puzzle")
st.caption("made with ❤️ by Maxwell (torchLight)")

with st.sidebar:
    st.header("Game Controls")
    mode = st.radio("Play as", ["Solo", "Teams"])
    if mode == "Teams":
        teams_input = st.text_input("Teams (comma-separated)", placeholder="Team Alpha, Team Beta, Design Squad")
        if st.button("Set Teams"):
            names = [t.strip() for t in teams_input.split(",") if t.strip()]
            if names:
                st.session_state.teams = names
                for n in names:
                    st.session_state.score.setdefault(n, 0)
    st.divider()
    st.markdown("**Round Timer**")
    st.session_state.timer_secs = st.slider("Seconds per round", min_value=15, max_value=180, value=60, step=5)
    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.button("⬅️ Previous", on_click=prev_puzzle, width='stretch')
    with col_b:
        st.button("Next ➡️", on_click=next_puzzle, width='stretch')
    if st.button("Shuffle Order 🔀", width='stretch'):
        random.shuffle(st.session_state.puzzle_order)
        st.session_state.idx = 0
        st.session_state.show_hint = False
        st.session_state.revealed = False
    st.divider()
    if st.button(("Show Hint 🤔" if not st.session_state.show_hint else "Hide Hint 🙈"), width='stretch'):
        st.session_state.show_hint = not st.session_state.show_hint
    if st.button(("Reveal Answer ✅" if not st.session_state.revealed else "Hide Answer ❌"), width='stretch'):
        st.session_state.revealed = not st.session_state.revealed

p_idx = st.session_state.puzzle_order[st.session_state.idx]
puz = PUZZLES[p_idx]

img = draw_puzzle(puz["layout"])
buf = io.BytesIO()
img.save(buf, format="PNG")
st.image(buf.getvalue(), width='stretch')

cols = st.columns(3)
with cols[0]:
    if st.session_state.show_hint:
        st.info(f"**Hint:** {puz['hint']}")
with cols[1]:
    st.metric("Round Timer (seconds)", value=st.session_state.timer_secs)
with cols[2]:
    st.caption(f"Puzzle {st.session_state.idx + 1} of {len(PUZZLES)}")

if st.session_state.revealed:
    st.success(f"**Answer:** {puz['answer']}")

st.divider()
st.subheader("Make a Guess")
guess = st.text_input("Type your guess here (not case-sensitive):", key=f"guess_{p_idx}")
left, right = st.columns([1,1])
with left:
    if st.button("Check Guess"):
        normalized = (guess or "").strip().lower()
        truth = puz["answer"].lower().replace('-', ' ')
        if normalized == truth or normalized.replace('-', ' ') == truth:
            st.balloons()
            st.success("Correct! 🎉")
        else:
            st.error("Not quite. Try again!")
with right:
    if st.button("Skip ➡️"):
        next_puzzle()

if mode == "Teams" and st.session_state.teams:
    st.subheader("Team Scores")
    cols = st.columns(len(st.session_state.teams))
    for i, t in enumerate(st.session_state.teams):
        with cols[i]:
            st.metric(t, st.session_state.score.get(t, 0))
            if st.button(f"+1 {t}", key=f"pt_{t}"):
                add_point(t)

st.caption("Tip: Use the sidebar to show hints, reveal answers, and navigate. Add or edit puzzles in the PUZZLES list.")
