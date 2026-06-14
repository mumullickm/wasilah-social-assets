#!/usr/bin/env python3
"""Rebuild the Wasilah daily-posts dashboard (index.html), captions.txt, and the
manual-publish pack. Photos live in posts/dphoto-<id>.jpg, videos in
videos/vid-<id>.mp4. media_kind in the manifest decides which a post expects."""
import json, html, glob, os

MANIFEST = "/Users/mirazmullick/Desktop/App Building/Claude Code/Wasilah/wasilah-social/dphotos.json"
POSTED = {"01-M"}
posts = json.load(open(MANIFEST, encoding="utf-8"))
HASJPG = {os.path.basename(p)[7:-4] for p in glob.glob("posts/dphoto-*.jpg")}
HASVID = {os.path.basename(p)[4:-4] for p in glob.glob("videos/vid-*.mp4")}

def slotlabel(s): return {"morning": "Morning · 08:00", "evening": "Evening · 20:00"}.get(s, "Topical")

cards, caplines = [], []
for p in posts:
    pid = p["id"]; slot = p.get("slot", ""); kind = p.get("media_kind", "photo")
    isvid = kind == "video"
    ready = (pid in HASVID) if isvid else (pid in HASJPG)
    if pid in POSTED: st, scls = "Posted (IG+FB)", "s-posted"
    elif ready: st, scls = ("Video ready" if isvid else "Ready"), "s-ready"
    else: st, scls = ("Video pending" if isvid else "Pending"), "s-pending"
    if isvid and ready:
        thumb = (f'<a class="thumb" href="videos/vid-{pid}.mp4" target="_blank">'
                 f'<video src="videos/vid-{pid}.mp4" muted loop preload="metadata"></video>'
                 f'<span class="play">&#9654;</span><span class="badge {scls}">{st}</span></a>')
        dl = f'<a class="btn" href="videos/vid-{pid}.mp4" download="wasilah-day{p["day"]:02d}-morning.mp4">&#8595; Video</a>'
    elif (not isvid) and ready:
        thumb = (f'<a class="thumb" href="posts/dphoto-{pid}.jpg" target="_blank">'
                 f'<img loading="lazy" src="posts/dphoto-{pid}.jpg" alt=""><span class="badge {scls}">{st}</span></a>')
        dl = f'<a class="btn" href="posts/dphoto-{pid}.jpg" download="wasilah-day{p["day"]:02d}-evening.jpg">&#8595; Image</a>'
    else:
        thumb = f'<div class="thumb"><div class="ph">{"video pending" if isvid else "image pending"}</div><span class="badge {scls}">{st}</span></div>'
        dl = ""
    kindtag = '<span class="kind">VIDEO</span>' if isvid else ''
    cap = p["caption"]
    actions = f'<div class="actions">{dl}<button class="btn copy" data-cap="{html.escape(cap, quote=True)}">&#8862; Caption</button></div>' if ready else ''
    cards.append(f'<article class="card">{thumb}<div class="meta"><div class="row1"><span class="day">Day {p["day"]}</span><span class="slot">{slotlabel(slot)}</span>{kindtag}<span class="type">{html.escape(p.get("type",""))}</span></div><div class="hen">{html.escape(p.get("headline_en",""))}</div><div class="ref">{html.escape(p.get("reference_en",""))}</div>{actions}<details><summary>Show caption</summary><div class="cap">{html.escape(cap).replace(chr(10),"<br>")}</div></details></div></article>')
    caplines.append(f"===== Day {p['day']} {slot or 'topical'} ({pid}, {kind}) · {p.get('reference_en','')} =====\n{cap}\n")

open("captions.txt", "w", encoding="utf-8").write("\n".join(caplines))
nready = sum(1 for p in posts if (p['id'] in HASVID if p.get('media_kind') == 'video' else p['id'] in HASJPG))
CSS = """*{margin:0;padding:0;box-sizing:border-box}:root{--emerald:#004B49;--deep:#001F1E;--gold:#F1D592;--cream:#F4F0E0}
body{background:var(--deep);color:var(--cream);font-family:'Urbanist',system-ui,sans-serif;padding:26px 16px 70px}
header{max-width:1160px;margin:0 auto 24px;text-align:center}h1{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:30px}h1 span{color:var(--gold)}
.sub{color:rgba(244,240,224,.62);font-size:14px;margin-top:8px}.bulk{margin-top:14px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.bulk a{background:var(--gold);color:#3a2e0c;font-weight:700;font-size:13px;text-decoration:none;padding:9px 16px;border-radius:999px}.bulk a.alt{background:rgba(241,213,146,.14);color:var(--gold);border:1px solid rgba(241,213,146,.4)}
.grid{max-width:1160px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:18px}
.card{background:#02312f;border:1px solid rgba(241,213,146,.14);border-radius:14px;overflow:hidden}
.thumb{position:relative;display:block;aspect-ratio:4/5;background:#021a19}.thumb img,.thumb video{width:100%;height:100%;object-fit:cover;display:block}
.play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:40px;color:rgba(255,255,255,.92);text-shadow:0 2px 12px rgba(0,0,0,.6);pointer-events:none}
.ph{width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:rgba(244,240,224,.4);font-size:13px}
.badge{position:absolute;top:10px;left:10px;font-size:11px;font-weight:600;padding:4px 9px;border-radius:999px}.s-posted{background:#1f7a4d;color:#eafff2}.s-ready{background:rgba(241,213,146,.92);color:#3a2e0c}.s-pending{background:rgba(244,240,224,.16)}
.meta{padding:13px 14px 15px}.row1{display:flex;gap:7px;align-items:center;flex-wrap:wrap;font-size:11px;margin-bottom:9px}
.day{background:var(--gold);color:#3a2e0c;font-weight:700;padding:2px 8px;border-radius:6px}.slot{color:rgba(244,240,224,.6)}.kind{color:#06222e;background:rgba(120,180,255,.9);padding:1px 7px;border-radius:6px;font-weight:700}.type{margin-left:auto;color:var(--gold);border:1px solid rgba(241,213,146,.3);padding:1px 7px;border-radius:6px}
.hen{font-weight:700;font-size:16px;line-height:1.25}.ref{color:var(--gold);font-size:12px;margin-top:7px}
.actions{display:flex;gap:8px;margin-top:12px}.btn{flex:1;text-align:center;cursor:pointer;background:rgba(241,213,146,.12);color:var(--gold);border:1px solid rgba(241,213,146,.32);border-radius:8px;padding:8px 6px;font-size:12.5px;font-weight:600;font-family:inherit;text-decoration:none}.btn.done{background:#1f7a4d;color:#eafff2;border-color:#1f7a4d}
details{margin-top:11px}summary{cursor:pointer;color:rgba(241,213,146,.8);font-size:12px}.cap{font-size:12.5px;line-height:1.6;color:rgba(244,240,224,.82);margin-top:8px;font-family:'Hind Siliguri','Urbanist',sans-serif}
footer{max-width:1160px;margin:30px auto 0;text-align:center;color:rgba(244,240,224,.4);font-size:12px}"""
doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Wasilah · Daily Posts</title>'
 "<style>@import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700&family=Hind+Siliguri:wght@400;500;600&family=Fraunces:ital,wght@1,500&display=swap');" + CSS + "</style></head><body>"
 '<header><h1>Wasilah <span>Daily Posts</span></h1>'
 '<div class="sub">24 days · mornings are 4:5 videos, evenings are photos · publish on your own at 08:00 and 20:00 Dhaka</div>'
 '<div class="bulk"><a href="wasilah-posts.zip" download>&#8595; All photos (zip)</a><a class="alt" href="captions.txt" download>&#8595; All captions (txt)</a></div>'
 f'<div class="sub" style="margin-top:12px">{len(posts)} posts · {nready} ready · {len(posts)-nready} pending</div></header>'
 '<div class="grid">' + ''.join(cards) + '</div>'
 '<footer>Wasilah social content · download, copy, publish</footer>'
 "<script>document.querySelectorAll('.btn.copy').forEach(b=>b.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(b.dataset.cap);const t=b.textContent;b.textContent='\\u2713 Copied';b.classList.add('done');setTimeout(()=>{b.textContent=t;b.classList.remove('done')},1500);}catch(e){alert('Copy failed, use Show caption.');}}));"
 "document.querySelectorAll('video').forEach(v=>{v.addEventListener('mouseenter',()=>v.play());v.addEventListener('mouseleave',()=>{v.pause();v.currentTime=0;});});</script></body></html>")
open("index.html", "w", encoding="utf-8").write(doc)
print(f"dashboard: {len(posts)} posts, {nready} ready ({len(HASVID)} videos, {len(HASJPG)} photos)")
