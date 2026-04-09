import os
import subprocess
import argparse

def run_streamlit():
    os.system("streamlit run dashboard/app.py")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ui", action="store_true")
    args = parser.parse_args()
    
    if args.ui:
        run_streamlit()
    else:
        subprocess.run(["python3", "scraper/amazon_search.py"])
        subprocess.run(["python3", "scraper/generate_reviews.py"])
        subprocess.run(["python3", "analysis/cleaner.py"])
        subprocess.run(["python3", "analysis/sentiment.py"])
        subprocess.run(["python3", "analysis/themes.py"])
        subprocess.run(["python3", "analysis/metrics.py"])

if __name__ == "__main__":
    main()
