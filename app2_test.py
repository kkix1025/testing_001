import re
from collections import Counter
import streamlit as st


def clean_words(text: str) -> list[str]:
    words = re.findall(r"[가-힣a-zA-Z0-9]+", text.lower())
    return words


def split_sentences(text: str) -> list[str]:
    sentences = re.split(r"[.!?\n]+", text)
    return [s.strip() for s in sentences if s.strip()]


def extract_top_words(words: list[str], top_n: int = 10) -> list[tuple[str, int]]:
    stopwords = {
        "은", "는", "이", "가", "을", "를", "에", "의", "도", "와", "과",
        "한", "하다", "그리고", "또한", "the", "is", "are", "a", "an", "of",
        "to", "in", "on", "for"
    }
    filtered = [w for w in words if w not in stopwords and len(w) > 1]
    counter = Counter(filtered)
    return counter.most_common(top_n)


def simple_summary(sentences: list[str], max_sentences: int = 3) -> list[str]:
    return sentences[:max_sentences]


def analyze_sentiment(text: str) -> str:
    positive_words = ["좋다", "행복", "성공", "만족", "추천", "재밌", "훌륭", "잘"]
    negative_words = ["싫다", "불편", "실패", "문제", "어렵", "나쁘", "최악", "불만"]

    pos_score = sum(text.count(word) for word in positive_words)
    neg_score = sum(text.count(word) for word in negative_words)

    if pos_score > neg_score:
        return "긍정"
    if neg_score > pos_score:
        return "부정"
    return "중립"


st.set_page_config(page_title="로컬 텍스트 분석기", page_icon="📝")
st.title("📝 로컬 텍스트 분석기")
st.write("API 없이 텍스트를 분석하는 토이 프로젝트입니다.")

user_input = st.text_area("텍스트를 입력하세요", height=250)

if st.button("분석하기"):
    if not user_input.strip():
        st.warning("텍스트를 먼저 입력하세요.")
    else:
        words = clean_words(user_input)
        sentences = split_sentences(user_input)
        top_words = extract_top_words(words)
        summary = simple_summary(sentences)
        sentiment = analyze_sentiment(user_input)

        st.subheader("기본 통계")
        st.write(f"- 글자 수: {len(user_input)}")
        st.write(f"- 단어 수: {len(words)}")
        st.write(f"- 문장 수: {len(sentences)}")
        st.write(f"- 감정 분류: {sentiment}")

        st.subheader("상위 키워드")
        if top_words:
            for word, count in top_words:
                st.write(f"- {word}: {count}회")
        else:
            st.write("추출된 키워드가 없습니다.")

        st.subheader("간단 요약")
        if summary:
            for idx, sentence in enumerate(summary, start=1):
                st.write(f"{idx}. {sentence}")
        else:
            st.write("요약할 문장이 없습니다.")