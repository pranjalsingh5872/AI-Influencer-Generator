import asyncio
import edge_tts

text = (
    "Zero makeup! I'm 17 and used to have painful cystic breakouts last year. "
    "My Dadi taught me to use pure Ayurvedic Kumkumadi saffron oil with rosewater every night before sleeping. "
    "Comment GLOW and I'll send you my exact routine and clean Amazon source!"
)

async def main():
    communicate = edge_tts.Communicate(text, "en-IN-NeerjaExpressiveNeural", rate="+6%", pitch="+2Hz")
    await communicate.save("ananya_day01_audio.mp3")
    print("[SUCCESS] Created ananya_day01_audio.mp3")

if __name__ == "__main__":
    asyncio.run(main())
