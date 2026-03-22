import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="레이아웃 디자인",
    layout="wide"  # 화면을 넓게 사용 (기본값은 "centered")
)

st.title("레이아웃 디자인")

# 학생 데이터 생성
data = {
    "이름": ["김철수", "이영희", "박민수", "정지은", "최동욱", "강서연", "윤태희", "장민지"],
    "나이": [25, 23, 26, 24, 27, 22, 25, 23],
    "학년": ["3학년", "2학년", "4학년", "3학년", "4학년", "1학년", "3학년", "2학년"],
    "수학": [85, 92, 78, 95, 88, 70, 91, 87],
    "영어": [90, 88, 85, 92, 86, 75, 89, 90],
    "과학": [88, 90, 92, 89, 91, 80, 85, 88]
}

df = pd.DataFrame(data)

# ============================================
# 1. 사이드바 (Sidebar) 사용하기
# ============================================
st.sidebar.title("설정 메뉴")
st.sidebar.write("사이드바에 필터링 옵션을 모아둘 수 있습니다.")

# 사이드바에 필터 옵션 배치
st.sidebar.header("데이터 필터")

# 사이드바 - 학년 선택
sidebar_grade = st.sidebar.selectbox(
    "학년 선택",
    options=["전체"] + sorted(df['학년'].unique().tolist())
)

# 사이드바 - 최소 나이
sidebar_min_age = st.sidebar.slider(
    "최소 나이",
    min_value=int(df['나이'].min()),
    max_value=int(df['나이'].max()),
    value=int(df['나이'].min())
)

# 사이드바 - 과목 선택
sidebar_subjects = st.sidebar.multiselect(
    "표시할 과목",
    options=["수학", "영어", "과학"],
    default=["수학", "영어", "과학"]
)

# 사이드바 구분선
st.sidebar.divider()

# 사이드바 - 추가 옵션
st.sidebar.header("추가 옵션")
show_stats = st.sidebar.checkbox("통계 표시", value=True)
show_chart = st.sidebar.checkbox("차트 표시", value=True)

# 필터링 적용
filtered_df = df.copy()

if sidebar_grade != "전체":
    filtered_df = filtered_df[filtered_df['학년'] == sidebar_grade]

filtered_df = filtered_df[filtered_df['나이'] >= sidebar_min_age]

st.sidebar.success(f" {len(filtered_df)}명의 학생이 검색되었습니다.")

# ============================================
# 2. 컬럼(Columns)으로 화면 나누기
# ============================================
st.header("1. 컬럼으로 화면 나누기")
st.write("화면을 여러 개의 열로 나눠서 정보를 정리할 수 있습니다.")

# 3개의 컬럼 생성 (동일한 너비)
col1, col2, col3 = st.columns(3)

# 각 컬럼에 메트릭 카드 배치
with col1:
    st.metric(
        label=" 총 학생 수",
        value=len(filtered_df),
        delta=f"{len(filtered_df) - len(df)} (필터 적용)"
    )

with col2:
    if sidebar_subjects:
        avg_score = filtered_df[sidebar_subjects].mean().mean()
        st.metric(
            label=" 평균 점수",
            value=f"{avg_score:.1f}점",
            delta="2.3점" if avg_score > 85 else "-1.2점"
        )
    else:
        st.metric(label=" 평균 점수", value="N/A")

with col3:
    if sidebar_subjects:
        max_score = filtered_df[sidebar_subjects].max().max()
        st.metric(
            label=" 최고 점수",
            value=f"{max_score}점"
        )
    else:
        st.metric(label=" 최고 점수", value="N/A")

st.divider()

# 2:1 비율로 컬럼 나누기
st.header("2. 비율을 조정한 컬럼 레이아웃")

col_left, col_right = st.columns([2, 1])  # 2:1 비율

with col_left:
    st.subheader(" 필터링된 학생 데이터")
    if sidebar_subjects:
        columns_to_show = ["이름", "나이", "학년"] + sidebar_subjects
        st.dataframe(filtered_df[columns_to_show], use_container_width=True, height=300)
    else:
        st.dataframe(filtered_df[["이름", "나이", "학년"]], use_container_width=True, height=300)

with col_right:
    st.subheader(" 요약 정보")
    if show_stats and sidebar_subjects:
        st.write("**과목별 평균**")
        for subject in sidebar_subjects:
            avg = filtered_df[subject].mean()
            st.write(f"• {subject}: {avg:.1f}점")
    else:
        st.info("사이드바에서 '통계 표시'를 선택하세요.")

st.divider()

# ============================================
# 3. 탭(Tabs)으로 콘텐츠 구분하기
# ============================================
st.header("3. 탭으로 콘텐츠 구분하기")
st.write("탭을 사용하면 많은 정보를 깔끔하게 정리할 수 있습니다.")

# 탭 생성
tab1, tab2, tab3, tab4 = st.tabs([" 데이터", " 차트", " 랭킹", " 정보"])

# 탭 1: 데이터 테이블
with tab1:
    st.subheader("전체 데이터 테이블")
    st.dataframe(filtered_df, use_container_width=True)
    
    # 탭 안에서도 컬럼 사용 가능
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("데이터 요약")
        st.write(f" 학생 수: {len(filtered_df)}명")
        st.write(f" 평균 나이: {filtered_df['나이'].mean():.1f}세")
    with col_b:
        st.write("학년 분포")
        grade_counts = filtered_df['학년'].value_counts()
        st.dataframe(grade_counts.to_frame(name="인원"), use_container_width=True)

# 탭 2: 차트
with tab2:
    st.subheader("성적 시각화")
    
    if show_chart and sidebar_subjects:
        # 과목별 평균 점수 차트
        st.write("과목별 평균 점수")
        avg_by_subject = filtered_df[sidebar_subjects].mean()
        st.bar_chart(avg_by_subject)
        
        # 학생별 점수 추이 (첫 5명만)
        st.write("학생별 성적 비교 (상위 5명)")
        chart_df = filtered_df[["이름"] + sidebar_subjects].head(5).set_index("이름")
        st.line_chart(chart_df)
    else:
        st.info("사이드바에서 '차트 표시'를 선택하고 과목을 선택하세요.")

# 탭 3: 랭킹
with tab3:
    st.subheader("성적 순위")
    
    if sidebar_subjects:
        rank_df = filtered_df.copy()
        rank_df['평균'] = rank_df[sidebar_subjects].mean(axis=1)
        rank_df['총점'] = rank_df[sidebar_subjects].sum(axis=1)
        rank_df = rank_df.sort_values('평균', ascending=False)
        
        # 순위 추가
        rank_df['순위'] = range(1, len(rank_df) + 1)
        
        st.dataframe(
            rank_df[['순위', '이름', '학년'] + sidebar_subjects + ['평균', '총점']],
            use_container_width=True
        )
        
        # 1등 학생 하이라이트
        if len(rank_df) > 0:
            top_student = rank_df.iloc[0]
            st.success(f" 1등: {top_student['이름']} ({top_student['학년']}) - 평균 {top_student['평균']:.1f}점")
    else:
        st.warning("사이드바에서 최소 하나의 과목을 선택하세요.")

# 탭 4: 정보
with tab4:
    st.subheader(" 레이아웃 가이드")
    
    st.markdown("""
    ### 배운 레이아웃 기능들:
    
    1. 사이드바 (Sidebar)
       - `st.sidebar.title()`, `st.sidebar.selectbox()` 등
       - 필터나 설정을 별도 공간에 배치
    
    2. 컬럼 (Columns)
       - `st.columns(3)` - 동일한 너비로 3개 분할
       - `st.columns([2, 1])` - 2:1 비율로 분할
       - `with col1:` 구문으로 각 컬럼에 콘텐츠 추가
    
    3. 탭 (Tabs)
       - `st.tabs(["탭1", "탭2"])` - 여러 탭 생성
       - `with tab1:` 구문으로 각 탭에 콘텐츠 추가
    
    4. 페이지 설정
       - `layout="wide"` - 화면을 넓게 사용
       - `layout="centered"` - 중앙 정렬 (기본값)
    """)

st.divider()

st.info("Tip: 실제 대시보드를 만들 때는 사이드바에 필터를, 메인 영역에는 탭으로 구분된 콘텐츠를 배치하는 것이 일반적입니다!")
