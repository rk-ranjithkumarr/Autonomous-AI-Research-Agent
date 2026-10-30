import os
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from ddgs import DDGS
from openai import OpenAI

load_dotenv()
APP_DIR = Path(__file__).parent
OUTPUT_DIR = APP_DIR / "reports"
OUTPUT_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Autonomous AI Research Agent", page_icon="🔎", layout="wide")
st.title("🔎 Autonomous AI Research Agent")
st.caption("Research planning → web search → source collection → cited report")

with st.sidebar:
    st.header("Settings")
    model = st.text_input("OpenAI model", value=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    max_results = st.slider("Sources to collect", 3, 10, 6)
    st.markdown("**Setup:** add `OPENAI_API_KEY` to `.env` for AI-generated reports.")
    st.markdown("Search results depend on the availability and quality of public web sources.")

topic = st.text_area(
    "Research question",
    placeholder="Example: How are small businesses using AI agents in 2026?",
    height=100,
)
focus = st.text_input("Optional focus or constraints", placeholder="Example: prioritize official sources and practical risks")

def search_web(query, limit):
    results = []
    try:
        with DDGS() as ddgs:
            for item in ddgs.text(query, max_results=limit):
                results.append({
                    "title": item.get("title", "Untitled"),
                    "url": item.get("href", ""),
                    "snippet": item.get("body", ""),
                })
    except Exception as exc:
        st.error(f"Web search failed: {exc}")
    # Deduplicate by URL
    unique, seen = [], set()
    for r in results:
        if r["url"] and r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)
    return unique

def generate_report(topic, focus, sources, model):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None, "OPENAI_API_KEY is not configured."
    client = OpenAI(api_key=api_key)
    source_text = "\n\n".join(
        f"[{i}] {s['title']}\nURL: {s['url']}\nSnippet: {s['snippet']}"
        for i, s in enumerate(sources, start=1)
    )
    prompt = f"""You are a careful research analyst. Produce a useful research brief for this question:
{topic}
Additional focus: {focus or 'None specified'}

Use only the source information supplied below for factual claims. Do not claim to have read full pages when only snippets are available. Cite claims using [1], [2], etc. Clearly label uncertainty, conflicting evidence, and gaps. Do not invent facts or citations.

Structure:
# Executive summary
# Key findings
# Evidence and analysis
# Risks, caveats, and open questions
# Conclusion
# Sources
For Sources, list each source number, title, and URL.

Collected search results:
{source_text}
"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You create evidence-aware research reports with transparent citations."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content, None

if st.button("🚀 Run research", type="primary", disabled=not topic.strip()):
    with st.status("Researching your question...", expanded=True) as status:
        st.write("1/3 Searching the web...")
        queries = [topic.strip()]
        if focus.strip():
            queries.append(f"{topic.strip()} {focus.strip()}")
        collected = []
        seen = set()
        for q in queries:
            for item in search_web(q, max_results):
                if item["url"] not in seen:
                    seen.add(item["url"])
                    collected.append(item)
        collected = collected[:max_results]
        st.write(f"Collected {len(collected)} unique search results.")
        st.write("2/3 Generating a cited report...")
        report, error = generate_report(topic.strip(), focus.strip(), collected, model)
        if error:
            # A usable source digest is still returned when no API key is configured.
            report = (
                f"# Research source digest\n\n**Research question:** {topic.strip()}\n\n"
                "**Note:** An OpenAI API key was not found, so an AI-synthesized report was not generated. "
                "Review these search results and add a key to `.env` to enable synthesis.\n\n"
                "## Search results\n\n" +
                "\n\n".join(f"### [{i}] {s['title']}\n{s['snippet']}\n\nSource: {s['url']}"
                            for i, s in enumerate(collected, 1))
            )
            st.warning(error)
        st.write("3/3 Saving report...")
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = OUTPUT_DIR / f"research_report_{stamp}.md"
        output.write_text(report, encoding="utf-8")
        status.update(label="Research run complete", state="complete", expanded=False)

    left, right = st.columns([2, 1])
    with left:
        st.subheader("Research report")
        st.markdown(report)
        st.download_button("Download Markdown report", report, file_name=output.name, mime="text/markdown")
    with right:
        st.subheader("Collected sources")
        for i, s in enumerate(collected, 1):
            st.markdown(f"**[{i}] [{s['title']}]({s['url']})**")
            st.caption(s["snippet"])
            st.divider()

st.markdown("---")
st.caption("Prototype note: this app searches public web snippets and synthesizes from those snippets. Verify important claims against the original sources.")
