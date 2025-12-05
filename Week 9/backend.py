import sqlite3
import time
import random
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- CONFIGURATION ---
DB_FILE = "aries_data.db"
HISTORY_SIZE = 500   # Reduced slightly for cleaner demos
REAL_TIME_SPEED = 2  # Slower live updates (easier to see the chart move)

# --- DATASETS ---
BRANDS = [
    "Apple", "Nike", "Tesla", "Samsung", "Disney", 
    "Google", "Amazon", "Microsoft", "Netflix", "Sony"
]

TEMPLATES_POS = [
    "I absolutely love the new features.", "Best purchase I've made all year.",
    "Customer service was incredibly helpful.", "The quality is unmatched.",
    "Stock price is looking great!", "Finally a product that works.",
    "Highly recommend this to everyone.", "Amazing experience.",
    "The design is beautiful.", "Super fast performance."
]

TEMPLATES_NEG = [
    "Total waste of money.", "It broke after just two days.",
    "Customer service was rude and unhelpful.", "Why is the price so high?",
    "Huge disappointment.", "The battery life is terrible.",
    "Glitchy and unusable.", "I will never buy from them again.",
    "This update ruined everything.", "Scam! Do not buy."
]

TEMPLATES_NEU = [
    "It arrived today.", "Thinking about upgrading.",
    "Does anyone know the release date?", "It's okay, nothing special.",
    "Compared to the previous model, it's similar.", "Just saw the ad.",
    "Waiting for the reviews.", "Standard quality.",
    "Not sure if I should buy it.", "Interesting news."
]

# --- ENGINE ---
analyzer = SentimentIntensityAnalyzer()

def get_random_text(brand):
    """Generates a realistic looking comment."""
    sentiment_type = random.choices(["pos", "neg", "neu"], weights=[40, 30, 30])[0]
    
    if sentiment_type == "pos":
        text = random.choice(TEMPLATES_POS)
    elif sentiment_type == "neg":
        text = random.choice(TEMPLATES_NEG)
    else:
        text = random.choice(TEMPLATES_NEU)
        
    if random.random() > 0.5:
        return f"[{brand}] {text}"
    else:
        return text

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sentiment_data 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  brand TEXT, 
                  text TEXT, 
                  sentiment REAL, 
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()
    print("✅ Database Connection Secure")

def seed_history():
    """Injects fake history that flows PERFECTLY into the present moment."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute("SELECT count(*) FROM sentiment_data")
    count = c.fetchone()[0]
    
    if count == 0:
        print(f"⚡ Seeding {HISTORY_SIZE} historical records sequentially...")
        data_batch = []
        now = datetime.datetime.now()
        
        # KEY FIX: Generate sequential timestamps ending NOW.
        # We simulate that posts came in every ~10 seconds in the past.
        for i in range(HISTORY_SIZE):
            brand = random.choice(BRANDS)
            text = get_random_text(brand)
            score = analyzer.polarity_scores(text)['compound']
            
            # Calculate time: (Total - Current Index) * interval
            # This ensures record 0 is old, and record 999 is roughly 'now'
            time_offset = (HISTORY_SIZE - i) * 10 
            past_time = now - datetime.timedelta(seconds=time_offset)
            
            data_batch.append((brand, text, score, past_time))
            
        c.executemany("INSERT INTO sentiment_data (brand, text, sentiment, timestamp) VALUES (?, ?, ?, ?)", data_batch)
        conn.commit()
        print("✅ History Load Complete.")
    else:
        print(f"ℹ️ Database already has {count} records. Skipping Seed.")
    
    conn.close()

def run_generator():
    init_db()
    seed_history()
    
    print("🚀 Aries Real-Time Generator Running... (Ctrl+C to stop)")
    
    while True:
        brand = random.choice(BRANDS)
        text = get_random_text(brand)
        score = analyzer.polarity_scores(text)['compound']
        current_time = datetime.datetime.now()
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO sentiment_data (brand, text, sentiment, timestamp) VALUES (?, ?, ?, ?)",
                  (brand, text, score, current_time))
        conn.commit()
        conn.close()
        
        print(f"Live Ingest: {brand} | {score:.2f}")
        time.sleep(random.uniform(0.5, REAL_TIME_SPEED))

if __name__ == "__main__":
    run_generator()