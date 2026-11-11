#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from build_video import get_duration, load_words, group_words, make_caption, build_sound_effects, mix_voice_and_effects
from dynamic_scenes import render_scenes

def sfx_events(duration, visuals, groups):
    events=[]
    ids = {
      "browser":"keyboard-typing-steady-medium","webpage":"keyboard-typing-steady-medium",
      "phone":"click-tap-medium","certificate":"digital-power-up","shield":"notification-success-soft",
      "server":"mechanical-switch-light","network":"digital-process-subtle","database":"digital-process-subtle",
      "terminal":"keyboard-typing-steady-medium","dashboard":"data-chart-reveal","chart":"data-bar-grow",
      "comparison":"swish-medium","process":"tone-step-2","timeline":"tone-step-3","cta":"sting-warm-short",
      "typography":"pop-medium-in"
    }
    n=len(visuals)
    for i, visual in enumerate(visuals):
        at=duration*i/n
        if at < duration-.05:
            events.append({"id":"whoosh-medium-soft","moment":round(at+.24,3),"label":f"entrada de escena {i+1}","gain_db":-1.0})
            cue=ids.get(visual,"pop-small-in")
            events.append({"id":cue,"moment":round(at+.82,3),"label":f"acción visual: {visual}","gain_db":-2.0})
    for i,g in enumerate(groups):
        if i%6==3:
            at=float(g[0]["start"])+.02
            if at<duration-.05:
                events.append({"id":"pop-small-in","moment":round(at,3),"label":"acento de texto","gain_db":-2.0})
    return sorted(events,key=lambda x:x["moment"])

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--transcript",required=True);p.add_argument("--audio",required=True)
    p.add_argument("--template",required=True);p.add_argument("--output",required=True)
    p.add_argument("--assets",required=True);p.add_argument("--title",required=True)
    p.add_argument("--storyboard",required=True)
    a=p.parse_args()
    duration=get_duration(a.audio)
    words=load_words(a.transcript)
    if not words: raise RuntimeError("La transcripción aprobada no contiene palabras.")
    groups=group_words(words)
    captions=[]; caption_anims=[]
    for i,g in enumerate(groups):
        start=g[0]["start"]; next_start=groups[i+1][0]["start"] if i+1<len(groups) else duration
        end=min(duration,g[-1]["end"]+.10,max(start+.2,next_start-.02))
        markup,anim=make_caption(g,i,start,end,duration)
        captions.append(markup);caption_anims.append(anim)
    storyboard=json.loads(Path(a.storyboard).read_text(encoding="utf-8"))
    scene_html,scene_anims,starts,visuals=render_scenes(storyboard,duration)
    assets=Path(a.assets);assets.mkdir(parents=True,exist_ok=True)
    sfx_path=build_sound_effects(duration,words,groups,assets,events_override=sfx_events(duration,visuals,groups))
    mix_voice_and_effects(a.audio,sfx_path,assets/"narration.wav")
    template=Path(a.template).read_text(encoding="utf-8")
    replacements={
      "{{DURATION}}":f"{duration:.3f}","{{SCENES}}":scene_html,
      "{{SCENE_STARTS}}":",".join(f"{x:.3f}" for x in starts),
      "{{SCENE_ANIMS}}":scene_anims,"{{CAPTIONS}}":"\n".join(captions),
      "{{CAPTION_ANIMS}}":"\n".join(caption_anims)
    }
    for k,v in replacements.items(): template=template.replace(k,v)
    if re.search(r"\{\{[A-Z_]+\}\}",template): raise RuntimeError("Quedaron marcadores sin sustituir en la plantilla dinámica.")
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(template,encoding="utf-8")
    print(f"Composición dinámica creada: {len(visuals)} escenas | {len(words)} palabras | {duration:.1f}s")
if __name__=="__main__": main()
