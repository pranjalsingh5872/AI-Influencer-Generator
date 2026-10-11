"""
AI Influencer Production & Content Pipeline Generator
======================================================
Automates the creation of 30-day viral content calendars,
Higgsfield image prompts, Kling 3.0 video prompts,
CapCut editing blueprints, Instagram SEO captions,
and ManyChat DM automation funnels.
"""

import json
import csv
import os
from typing import Dict, List, Any

PERSONAS = {
    "ananya_teen_glow": {
        "name": "Ananya Sharma (17yo Indian Gen-Z Ayurvedic Glass-Skin & Hair Creator)",
        "demographic": "Radiant 17-year-old Indian girl, natural warm golden-wheatish glowing complexion, flawless clear glass skin, expressive dark brown almond eyes, wearing an aesthetic pastel casual college kurti or oversized neutral hoodie, natural glossy thick wavy dark brown hair, approachable, energetic Gen-Z student charm",
        "aesthetic": "Sunlit college campus courtyard or aesthetic cafe garden in Mumbai at golden hour, interviewer hand holding a professional wireless microphone on the right side",
        "niche": "Gen-Z Ayurvedic Glass Skin, Ancient Hair Oiling, College Wellness & Teen Acne Fixes",
        "default_product": "Authentic Kumkumadi Tailam Saffron Miracle Face Oil & Wild Kasturi Manjal ($28.99)",
        "tone": "Warm, relatable, bubbly, authentic Gen-Z ('Hey guys! Honestly...')"
    },
    "mother_sator": {
        "name": "Mother Sator (Tropical Ancient Herbalist)",
        "demographic": "Radiant 54-year-old Asian woman, glowing skin, natural fine lines, fit yoga physique, hair down",
        "aesthetic": "Beach in Tulum, Mexico at sunset, natural golden hour lighting, interviewer hand with microphone on right",
        "niche": "Ancient Herbal Longevity & Soursop Bitters",
        "default_product": "Jamaican Soursop Bitters & Wild Moringa ($35.99)",
        "tone": "Warm, maternal, mystical, authoritative ('Hello child...')"
    },
    "grandmother_may": {
        "name": "Grandmother May (Holistic Tea & Biohacking Elder)",
        "demographic": "Charming 62-year-old silver-haired woman, athletic posture, radiant porcelain skin, linen shirt",
        "aesthetic": "Sunlit botanical garden terrace, herbal tea set on table, interviewer holding wireless microphone",
        "niche": "Cellular Longevity & Yerba Mate Cleanses",
        "default_product": "Organic Unsmoked Yerba Mate & Guayusa Blend ($28.50)",
        "tone": "Wise, scientifically curious, vibrant, grandmotherly"
    },
    "fit_midlife_guru": {
        "name": "Elena Zen (The Ageless Midlife Athlete)",
        "demographic": "50-year-old fit Mediterranean woman, athletic abs, sun-kissed skin, tank top, high ponytail",
        "aesthetic": "Oceanfront wooden yoga deck, coastal breeze, interviewer holding microphone",
        "niche": "Fasting, Gut Health & Collagen Regeneration",
        "default_product": "Himalayan Shilajit Resin & Sea Moss Gel ($42.00)",
        "tone": "Direct, energetic, motivating, fitness coach vibes"
    }
}

SCRIPTS_DATABASE = [
    {
        "hook_type": "Age Disbelief",
        "interviewer_line": "Wait, let me guess your age... you gotta be 34?",
        "character_response": "I wish, sweetie! I'm 108 years old. People think it's Botox, but it's just two tablespoons of wild soursop bitters every single morning before coffee.",
        "cta": "Comment 'SECRET' and I'll send you the exact bottle I drink!",
        "keyword": "SECRET",
        "ingredient": "Jamaican Soursop Bitters",
        "seo_keywords": ["anti aging secrets", "soursop bitters benefits", "natural longevity", "herbal wellness", "how to look younger naturally"]
    },
    {
        "hook_type": "Doctor Shock",
        "interviewer_line": "What did your doctor say at your last annual checkup?",
        "character_response": "My doctor asked if my blood panel belonged to a 22-year-old marathon runner! I'm 64. Every morning I take one spoonful of wild moringa leaf powder—it has 7 times more vitamin C than oranges.",
        "cta": "Comment 'GREEN' and I'll send you my trusted lab-tested source!",
        "keyword": "GREEN",
        "ingredient": "Wildcrafted Green Moringa Powder",
        "seo_keywords": ["moringa powder benefits", "blood panel results", "natural energy boost", "cellular vitality", "superfood anti-aging"]
    },
    {
        "hook_type": "Filler & Botox Controversy",
        "interviewer_line": "How much do you spend every month on Botox and face fillers?",
        "character_response": "Zero dollars! I'm 61 years old. In Beverly Hills they spend thousands on needles, but ancient women just dabbed organic cold-pressed castor oil with frankincense under their eyes every night.",
        "cta": "Comment 'OIL' and I'll send you my nightly wrinkle recipe!",
        "keyword": "OIL",
        "ingredient": "Hexane-Free Castor Oil & Frankincense",
        "seo_keywords": ["natural botox alternative", "castor oil for wrinkles", "frankincense skin benefits", "anti wrinkle routine", "clean skincare"]
    },
    {
        "hook_type": "Morning Routine Mistake",
        "interviewer_line": "What is the single worst thing people drink first thing in the morning?",
        "character_response": "Iced water and sugary latte! I'm 69 and my energy never crashes. Your stomach fire needs warmth. A cup of pure unsmoked Yerba Mate with lemon peel flushes stored liver toxins and accelerates fat metabolism.",
        "cta": "Comment 'TEA' and I'll send you the ancient preparation guide!",
        "keyword": "TEA",
        "ingredient": "Unsmoked Argentine Yerba Mate",
        "seo_keywords": ["yerba mate benefits", "liver cleanse morning routine", "metabolism booster", "healthy morning drink", "fat loss tea"]
    },
    {
        "hook_type": "Mineral Deficiency & Energy",
        "interviewer_line": "Why does everyone feel so exhausted by 2 PM every day?",
        "character_response": "Because our soil has zero minerals left! I'm 72 and work out every single day. A pea-sized resin of pure Himalayan Shilajit provides 85 trace minerals that reactivate your mitochondrial energy.",
        "cta": "Comment 'GUT' and I'll DM you the pure resin I use!",
        "keyword": "GUT",
        "ingredient": "Pure Himalayan Shilajit Resin",
        "seo_keywords": ["shilajit resin benefits", "chronic fatigue remedy", "85 trace minerals", "cellular energy", "natural vitality"]
    },
    {
        "hook_type": "Hair Density at 60+",
        "interviewer_line": "Is that your real hair or are those extensions?",
        "character_response": "Every single strand is natural, honey! I'm 66 and my hair is thicker than in my 20s. I warm pure Batana oil with rosemary extract and massage my scalp twice a week.",
        "cta": "Comment 'HAIR' and I'll send you the exact blend ratio!",
        "keyword": "HAIR",
        "ingredient": "Wild Batana & Rosemary Scalp Elixir",
        "seo_keywords": ["hair growth oil", "batana oil results", "rosemary hair density", "grey hair reversal", "natural thick hair"]
    },
    {
        "hook_type": "Sugar & Glycation Hook",
        "interviewer_line": "How do you stay this toned without doing crazy cardio?",
        "character_response": "I don't starve myself! I'm 58. The real enemy of aging is blood sugar spikes that stiffen your collagen. Ceylon cinnamon and raw apple cider vinegar before your heavy meals keeps insulin completely flat.",
        "cta": "Comment 'BURN' and I'll DM you my daily routine!",
        "keyword": "BURN",
        "ingredient": "Organic Ceylon Cinnamon & ACV",
        "seo_keywords": ["blood sugar balance", "ceylon cinnamon benefits", "collagen protection", "flat stomach routine", "midlife weight loss"]
    },
    {
        "hook_type": "Joint Mobility Miracle",
        "interviewer_line": "Can your knees handle squats at your age?",
        "character_response": "I do 100 deep squats every single morning! I'm 75. You don't have bad knees, you have stagnant chronic inflammation. Liposomal turmeric with piperine rebuilt my joints when doctors said I had no cartilage left.",
        "cta": "Comment 'JOINTS' and I'll send you the extract I take!",
        "keyword": "JOINTS",
        "ingredient": "Liposomal Curcumin & Ginger Complex",
        "seo_keywords": ["joint pain relief", "curcumin turmeric extract", "knee pain natural remedy", "mobility at 70", "inflammation cure"]
    },
    {
        "hook_type": "Hydration / Glass Skin Hack",
        "interviewer_line": "Everyone in your comments asks what filter you use. What filter is it?",
        "character_response": "No filter here, darling! Just imperial Tremella snow mushroom tea. It holds 500 times its weight in moisture, acting like the body's natural internal hyaluronic acid.",
        "cta": "Comment 'GLOW' and I'll send you my skin broth recipe!",
        "keyword": "GLOW",
        "ingredient": "Tremella Fuciformis Snow Mushroom",
        "seo_keywords": ["glass skin routine", "tremella mushroom benefits", "internal hyaluronic acid", "plump skin naturally", "ancient beauty secrets"]
    },
    {
        "hook_type": "The 100-Year Ancestral Law",
        "interviewer_line": "If you could tell someone in their 30s one rule for longevity, what is it?",
        "character_response": "Stop eating foods with barcodes on them! I'm 88 years young. Cold-pressed black seed oil every dawn kills free radicals before they can damage your DNA. The Pharaohs used it for a reason.",
        "cta": "Comment 'CURE' and I'll send you the clean glass bottle I order!",
        "keyword": "CURE",
        "ingredient": "Cold-Pressed Nigella Sativa (Black Seed Oil)",
        "seo_keywords": ["black seed oil benefits", "ancestral eating", "living to 100", "natural medicine", "longevity habits"]
    }
]

INDIAN_TEEN_SCRIPTS_DATABASE = [
    {
        "hook_type": "Glass Skin Foundation Shock",
        "interviewer_line": "Excuse me, your skin looks like literal glass... how many foundation layers do you wear?",
        "character_response": "Zero makeup! I'm 17 and used to have painful cystic breakouts last year. My Dadi taught me to use pure Ayurvedic Kumkumadi saffron oil with rosewater every night before sleeping.",
        "cta": "Comment 'GLOW' and I'll send you my exact routine and clean Amazon source!",
        "keyword": "GLOW",
        "ingredient": "Pure Kumkumadi Saffron Miracle Oil",
        "seo_keywords": ["glass skin routine", "ayurvedic skincare", "teen acne remedy", "kumkumadi oil benefits", "clear skin naturally"]
    },
    {
        "hook_type": "Thick Hair Extension Myth",
        "interviewer_line": "Is that thick hair natural or do you wear extensions?",
        "character_response": "100% natural Indian hair! Every Sunday night I warm pure rosemary, Amla, and Bhringraj oil and do a 5-minute inversion scalp massage before washing.",
        "cta": "Comment 'HAIR' and I'll DM you the exact 3-herb ratio recipe!",
        "keyword": "HAIR",
        "ingredient": "Amla & Bhringraj Scalp Growth Oil",
        "seo_keywords": ["hair oiling routine", "rosemary amla oil", "thick hair secrets", "grow hair fast", "ayurvedic hair care"]
    },
    {
        "hook_type": "The 24-Hour Acne Shrinker",
        "interviewer_line": "What do you do when you get a giant pimple the night before an event?",
        "character_response": "Never pop it! I mix wild Kasturi turmeric with raw mountain honey and dab it as an Ubtan spot treatment. It kills acne bacteria overnight without staining your skin yellow.",
        "cta": "Comment 'ACNE' and I'll send you the non-staining turmeric brand I use!",
        "keyword": "ACNE",
        "ingredient": "Wild Kasturi Manjal & Raw Honey Ubtan",
        "seo_keywords": ["overnight pimple fix", "wild turmeric for acne", "kasturi manjal", "natural spot treatment", "acne scars removal"]
    },
    {
        "hook_type": "Late-Night Exam Dark Circles",
        "interviewer_line": "You study till 3 AM for exams, how do you have zero dark circles?",
        "character_response": "Ditch the expensive eye creams! I use chilled pure Kannauj rosewater cotton pads for 5 minutes, then tap pure cold-pressed sweet almond oil under my eyes.",
        "cta": "Comment 'EYES' and I'll send you my nightly 2-minute exam routine!",
        "keyword": "EYES",
        "ingredient": "Pure Kannauj Rosewater & Sweet Almond Oil",
        "seo_keywords": ["dark circles remedy", "exam student routine", "rose water benefits", "under eye hollows fix", "natural beauty hacks"]
    },
    {
        "hook_type": "Sun Tan Reversal",
        "interviewer_line": "Did you just come back from college sports with zero sun tan?",
        "character_response": "Ancient Indian bridal secret! A quick paste of gram flour, pinch of turmeric, raw milk, and aloe vera reverses UV tan in 15 minutes without any chemical bleach.",
        "cta": "Comment 'TAN' and I'll DM you the exact measurement card!",
        "keyword": "TAN",
        "ingredient": "Ayurvedic Besan & Saffron De-Tan Ubtan",
        "seo_keywords": ["remove sun tan naturally", "ayurvedic de tan", "besan haldi pack", "brightening mask", "sun damage fix"]
    },
    {
        "hook_type": "Internal Gut Glow",
        "interviewer_line": "Why does your skin look like it's glowing from the inside?",
        "character_response": "Because glowing skin starts in your gut, not your Sephora cart! Every morning before school I drink warm copper-infused water with soaked fenugreek and crushed mint.",
        "cta": "Comment 'GUT' and I'll send you the morning detox water guide!",
        "keyword": "GUT",
        "ingredient": "Copper Vessel Water & Fenugreek Seeds",
        "seo_keywords": ["gut health clear skin", "copper water benefits", "fenugreek for skin", "morning detox drink", "glow from within"]
    },
    {
        "hook_type": "Fermented Rice Water Glass Skin",
        "interviewer_line": "What toner do you use for those invisible pores?",
        "character_response": "Fermented organic red rice water infused with vetiver roots! Korean skincare actually adopted this from ancient Indian rice water rituals. It balances skin pH instantly.",
        "cta": "Comment 'TONER' and I'll send you the 3-day brew instructions!",
        "keyword": "TONER",
        "ingredient": "Fermented Rice Water & Vetiver Hydrosol",
        "seo_keywords": ["rice water toner", "korean glass skin secret", "shrink pores naturally", "diy toner", "ayurvedic beauty"]
    },
    {
        "hook_type": "Naturally Pink Lips Fix",
        "interviewer_line": "What lip tint are you wearing right now?",
        "character_response": "It's not makeup! It's pure organic A2 Desi Ghee mixed with freshly pressed organic beetroot juice. It heals chapped lips and reverses dark lip pigmentation in 7 days.",
        "cta": "Comment 'LIPS' and I'll send you the DIY lip balm recipe!",
        "keyword": "LIPS",
        "ingredient": "Organic Desi Ghee & Beetroot Lip Elixir",
        "seo_keywords": ["pink lips naturally", "ghee for dark lips", "diy beetroot lip tint", "lighten pigmented lips", "natural lip care"]
    },
    {
        "hook_type": "Exam Stress Breakout Shield",
        "interviewer_line": "How do you stay breakout-free during high stress exam weeks?",
        "character_response": "Cortisol spikes cause hormonal chin acne! Every night I drink warm golden milk with a quarter spoon of pure KSM-66 Ashwagandha. Lowers stress and repairs skin cells during deep sleep.",
        "cta": "Comment 'CALM' and I'll DM you my bedtime golden milk blend!",
        "keyword": "CALM",
        "ingredient": "Pure Ashwagandha & Golden Turmeric Milk",
        "seo_keywords": ["stress acne remedy", "ashwagandha benefits", "golden milk recipe", "hormonal acne teen", "deep sleep glow"]
    },
    {
        "hook_type": "Zero Pore French Green Clay & Neem",
        "interviewer_line": "How do you have zero blackheads or strawberry nose?",
        "character_response": "I do a 10-minute Multani Mitti (Fuller's Earth) and steam-distilled neem leaf wash once a week. It pulls out stubborn dirt like a magnet without stripping moisture.",
        "cta": "Comment 'PORES' and I'll send you the clean Amazon brand I swear by!",
        "keyword": "PORES",
        "ingredient": "Pure Multani Mitti & Steam-Distilled Neem",
        "seo_keywords": ["multani mitti benefits", "clear blackheads naturally", "shrink nose pores", "neem clay mask", "indian skincare secrets"]
    }
]

def build_higgsfield_prompt(persona_key: str, scene_context: str = "") -> str:
    persona = PERSONAS[persona_key]
    skin_texture = (
        "authentic youthful radiant skin texture with visible natural pores, healthy clean glow, no artificial plastic filter"
        if persona_key == "ananya_teen_glow"
        else "authentic skin texture with natural fine wrinkles, visible pores, realistic maturity"
    )
    return (
        f"A hyper-realistic raw documentary portrait of {persona['demographic']}, {persona['aesthetic']}. "
        f"An interviewer's hand is visible on the right side of the screen holding a professional black wireless reporter microphone towards her. "
        f"She is looking slightly off-camera engaging candidly with the interviewer with a warm natural expression. "
        f"Subtle breeze blowing wisps of dark hair, {skin_texture}, soft depth-of-field background bokeh. "
        f"Shot on 35mm portrait lens, 9:16 vertical ratio, golden hour natural light, 4K quality."
    )

def build_kling_prompt(interviewer_line: str, character_response: str, cta: str, persona_key: str = "") -> str:
    full_speech = f"{character_response} {cta}"
    subject_desc = "The young 17-year-old girl" if persona_key == "ananya_teen_glow" else "The woman"
    return (
        f"{subject_desc} speaks naturally and expressively into the microphone in response to an interview question. "
        f"Natural head movements, engaging eye contact with interviewer off-camera, realistic expressive lip synchronization. "
        f"Wind gently rustles her hair, natural chest breathing movement, photorealistic human micro-expressions. "
        f"Spoken dialogue: '{full_speech}'"
    )

def build_manychat_dm(ingredient: str, default_product: str, keyword: str) -> str:
    return (
        f"Hello child! 🌿 Thank you so much for commenting '{keyword}' on my post.\n\n"
        f"As promised, here is the exact ancient morning routine I take every single sunrise:\n\n"
        f"1️⃣ Pure {ingredient} taken right as you awaken with 6oz of room-temperature spring water.\n"
        f"2️⃣ Breathe deeply for 5 minutes in the morning sun before having tea or food.\n"
        f"3️⃣ Repeat daily for 21 days to feel your cellular vitality restore.\n\n"
        f"I do not sell this myself, but this is the exact clean, small-batch bottle with verified lab testing I order from Amazon:\n"
        f"👉 [AMAZON_PRODUCT_LINK]\n\n"
        f"Let me know when yours arrives! Wishing you endless health & vibrant youth. 💛"
    )

def generate_30_day_campaign(persona_key: str = "mother_sator", output_dir: str = ".") -> Dict[str, Any]:
    persona = PERSONAS[persona_key]
    calendar_entries = []

    # Cycle through the 10 core scripts 3 times with unique angles to form 30 days
    angles = [
        "Angle 1: Shock Value & Age Confusion",
        "Angle 2: Ancient Remedy vs. Modern Medicine",
        "Angle 3: Step-by-Step Daily Routine Breakdown"
    ]

    scripts_to_use = INDIAN_TEEN_SCRIPTS_DATABASE if persona_key == "ananya_teen_glow" else SCRIPTS_DATABASE

    day = 1
    for angle_idx, angle in enumerate(angles):
        for script_idx, script in enumerate(scripts_to_use):
            day_num = day
            title = f"Day {day_num:02d} - {script['hook_type']} ({angle})"
            
            hf_prompt = build_higgsfield_prompt(persona_key)
            kling_prompt = build_kling_prompt(script['interviewer_line'], script['character_response'], script['cta'], persona_key)
            
            if persona_key == "ananya_teen_glow":
                manychat_dm = (
                    f"Hey guys! 🌸 Thank you so much for commenting '{script['keyword']}' on my reel!\n\n"
                    f"Here is the exact natural Ayurvedic routine I use for {script['ingredient']}:\n\n"
                    f"1️⃣ Cleanse gently with lukewarm water and organic Kannauj rosewater.\n"
                    f"2️⃣ Apply {script['ingredient']} evenly and let your skin absorb the nutrients for 15-20 minutes.\n"
                    f"3️⃣ Always stay consistent for 14-21 days to see your skin glow naturally without filters.\n\n"
                    f"I don't sell this myself, but this is the exact 100% pure organic brand I personally order from Amazon:\n"
                    f"👉 [AMAZON_PRODUCT_LINK]\n\n"
                    f"Let me know if you try it! Sending you so much love and glowing energy. ✨"
                )
                caption = (
                    f"Never gatekeeping the ancient Ayurvedic secrets my Dadi taught me... 🌸✨\n\n"
                    f"Everyone on campus thinks glass skin requires buying $100 chemical serums and covering acne with makeup. "
                    f"The truth? Our traditional Indian herbal recipes have worked for centuries because they treat skin at the root!\n\n"
                    f"👇 Comment '{script['keyword']}' below and I'll DM you my exact DIY routine card and the pure Amazon link I order!\n\n"
                    f"#ayurveda #glassskin #teenbeauty #skincareroutine #{script['keyword'].lower()} #indianbeauty #naturalglow #collegeglow"
                )
            else:
                manychat_dm = build_manychat_dm(script['ingredient'], persona['default_product'], script['keyword'])
                caption = (
                    f"They never believe me until I share the family recipe... 🌿✨\n\n"
                    f"Most people think vibrant health after 50 is just good genetics or thousands spent on cosmetic treatments. "
                    f"The truth? Our ancestors understood natural botanical medicine centuries before synthetic pills existed.\n\n"
                    f"👇 Comment '{script['keyword']}' below and I'll DM you the exact preparation guide and the pure source I use every sunrise!\n\n"
                    f"#longevity #antiaging #naturalremedies #{script['keyword'].lower()} #wellnessjourney #holistichealth"
                )

            calendar_entries.append({
                "day": day_num,
                "title": title,
                "hook_type": script["hook_type"],
                "interviewer_audio": script["interviewer_line"],
                "character_dialogue": script["character_response"],
                "cta_call": script["cta"],
                "manychat_keyword": script["keyword"],
                "product_promoted": script["ingredient"],
                "higgsfield_prompt": hf_prompt,
                "kling_prompt": kling_prompt,
                "manychat_dm_payload": manychat_dm,
                "instagram_caption": caption
            })
            day += 1

    # Write Markdown Calendar
    md_path = os.path.join(output_dir, f"30_DAY_CONTENT_CALENDAR_{persona_key.upper()}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 📅 30-Day Content Calendar & Production Runbook\n")
        f.write(f"**Persona:** {persona['name']}\n\n")
        f.write(f"**Niche:** {persona['niche']} | **Monetization Target:** {persona['default_product']}\n\n")
        f.write("---\n\n")

        for item in calendar_entries:
            f.write(f"## 🎬 Day {item['day']:02d}: {item['title']}\n\n")
            f.write(f"**🎙️ Hook / Interviewer Question:** *\"{item['interviewer_audio']}\"*\n\n")
            f.write(f"**💬 Character Response:** *\"{item['character_dialogue']}\"*\n\n")
            f.write(f"**🚨 Call to Action (CTA):** `{item['cta_call']}`\n\n")
            f.write(f"**⚡ ManyChat Trigger Keyword:** `{item['manychat_keyword']}`\n\n")
            f.write(f"### 🖼️ Higgsfield Image Prompt (Start Frame):\n```text\n{item['higgsfield_prompt']}\n```\n\n")
            f.write(f"### 🎥 Kling 3.0 Video Prompt (Lip-Sync 10s):\n```text\n{item['kling_prompt']}\n```\n\n")
            f.write(f"### 💌 Automated ManyChat DM Delivery:\n```text\n{item['manychat_dm_payload']}\n```\n\n")
            f.write(f"### 📱 Instagram Caption & SEO Keywords:\n```text\n{item['instagram_caption']}\n```\n\n")
            f.write("---\n\n")

    # Write CSV for easy scheduling (Notion / Airtable)
    csv_path = os.path.join(output_dir, f"content_calendar_{persona_key}.csv")
    fieldnames = [
        "day", "title", "hook_type", "interviewer_audio", "character_dialogue", 
        "manychat_keyword", "product_promoted", "higgsfield_prompt", "kling_prompt"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(calendar_entries)

    print(f"[SUCCESS] Generated 30-Day Campaign for {persona['name']}")
    print(f"[FILE] Markdown Calendar: {md_path}")
    print(f"[FILE] CSV Spreadsheet: {csv_path}")

    return {
        "persona": persona,
        "calendar_entries_count": len(calendar_entries),
        "md_path": md_path,
        "csv_path": csv_path
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate 30-Day AI Influencer Content Campaigns")
    parser.add_argument("--persona", choices=["ananya_teen_glow", "mother_sator", "grandmother_may", "fit_midlife_guru", "all"], default="ananya_teen_glow",
                        help="Select target AI influencer persona (default: ananya_teen_glow)")
    args = parser.parse_args()

    if args.persona == "all":
        for p in PERSONAS.keys():
            generate_30_day_campaign(p)
    else:
        generate_30_day_campaign(args.persona)
