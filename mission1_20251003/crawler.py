# ============================================================
# 야놀자 리뷰 크롤러
# ============================================================
# 야놀자 숙소 리뷰 페이지에서 리뷰 텍스트, 별점, 날짜를 수집하여 JSON 파일로 저장

import json
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm

# 크롤링 대상 URL (야놀자 강릉 호텔 리뷰 페이지)
# 변경 이력:
# - sort=HOST_CHOICE → 호스트 선택 리뷰만 (모두 5점)
# - sort 없음 → 모든 리뷰 (여전히 대부분 5점)
# - sort=LATEST (최종) → 최신순 정렬 (다양한 별점 기대)
URL = 'https://nol.yanolja.com/reviews/domestic/3013417?sort=LATEST'

# 스크롤 설정 (최종 최적화: 2025-10-04)
SCROLL_COUNT = 20  # 페이지 스크롤 횟수 (적정 수준으로 유지)
SCROLL_PAUSE_TIME = 2  # 각 스크롤 후 대기 시간 (안정적 동적 로딩)


def scroll_page(driver, scroll_count=SCROLL_COUNT, pause_time=SCROLL_PAUSE_TIME):
    """
    페이지를 아래로 스크롤하여 동적 콘텐츠(리뷰)를 로드

    Args:
        driver: Selenium WebDriver 인스턴스
        scroll_count (int): 스크롤을 수행할 횟수
        pause_time (float): 각 스크롤 후 대기 시간 (초)
    """
    print(f"페이지 스크롤 시작 ({scroll_count}회)...")

    for i in range(scroll_count):
        # 페이지 최하단으로 스크롤
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        # 동적 콘텐츠 로딩 대기
        time.sleep(pause_time)

        # 진행 상황 표시
        if (i + 1) % 3 == 0:
            print(f"  스크롤 진행: {i + 1}/{scroll_count}")

    print("스크롤 완료!")


def extract_date(date_text):
    """
    날짜 문자열에서 YYYY.MM.DD 형식의 날짜만 추출

    Args:
        date_text (str): 크롤링한 날짜 필드 텍스트

    Returns:
        str: 추출된 날짜 (YYYY.MM.DD) 또는 빈 문자열

    Examples:
        '2022.09.30' → '2022.09.30'
        '루루*' → ''
        '골져스 파셜오션 더블' → ''
    """
    # 정규표현식으로 YYYY.MM.DD 형식 찾기
    match = re.search(r'\d{4}\.\d{2}\.\d{2}', date_text)

    if match:
        return match.group(0)  # 매칭된 날짜 반환
    else:
        return ''  # 날짜 형식이 없으면 빈 문자열


def extract_stars(review_container):
    """
    리뷰 컨테이너에서 별점 추출 (2025-10-04 실제 HTML 구조 기반)

    Args:
        review_container: BeautifulSoup element (리뷰 컨테이너)

    Returns:
        int: 별점 (0-5)

    Note:
        2025-10-04 디버그 분석 결과 (최종 수정):
        - 별점 위치: css-166s55a (Level 3 컨테이너)
        - 별점 컨테이너: <div class="css-rz7kwu">
        - 별점 SVG: <svg class="css-1mj121y"> (총 5개 - 활성+비활성)
        - 제외 SVG: <svg class="css-165qm45"> (좋아요 버튼)

        ⚠️ 중요: 야놀자는 활성 별(⭐)과 비활성 별(☆)을 모두 css-1mj121y로 표시
        → path 데이터로 구분:
          - 채워진 별: path d="M12.638 2.471..." (활성)
          - 빈 별: path d="M10.693 3.123..." (비활성)

        해결책: path의 첫 숫자가 12인 것만 카운트 (채워진 별)
    """
    # 별점 컨테이너 찾기
    star_container = review_container.find('div', class_='css-rz7kwu')
    if not star_container:
        return 0

    # 모든 별 SVG 찾기 (활성+비활성 포함)
    star_svgs = star_container.find_all('svg', class_='css-1mj121y')
    if not star_svgs:
        return 0

    # 채워진 별만 카운트 (path의 첫 숫자가 12인 것)
    filled_stars = 0
    for svg in star_svgs:
        path = svg.find('path')
        if path:
            d_attr = path.get('d', '')
            # 채워진 별: "M12.638..." 로 시작
            # 빈 별: "M10.693..." 로 시작
            if d_attr.startswith('M12.'):
                filled_stars += 1

    # 검증: 별점은 0-5개 사이여야 함
    if 0 <= filled_stars <= 5:
        return filled_stars

    # 예외 상황: 5개 초과면 전체 SVG 개수 반환 (폴백)
    return min(len(star_svgs), 5)


def parse_reviews(html):
    """
    HTML 소스에서 리뷰 데이터 파싱 (2025-10 기준 실제 구조)

    Args:
        html (str): 페이지의 HTML 소스

    Returns:
        list: 리뷰 딕셔너리 리스트
              각 리뷰: {'review': str, 'stars': int, 'date': str}
    """
    soup = BeautifulSoup(html, 'html.parser')

    # 리뷰 컨테이너 선택 (2025-10 기준 실제 구조)
    # css-166s55a 또는 content-text를 포함한 상위 div
    review_containers = soup.find_all('div', class_='css-166s55a')

    # 대체: content-text 기준으로 상위 컨테이너 찾기
    if not review_containers:
        review_texts = soup.find_all('p', class_='content-text css-vjs6b8')
        review_containers = [p.find_parent('div', class_=re.compile(r'css-')) for p in review_texts]
        review_containers = [c for c in review_containers if c]  # None 제거

    review_list = []
    success_count = 0
    fail_count = 0

    print(f"\n리뷰 파싱 시작 (총 {len(review_containers)}개)...")

    # tqdm으로 진행 상황 표시
    for i in tqdm(range(len(review_containers)), desc="리뷰 파싱"):
        try:
            container = review_containers[i]

            # 1. 리뷰 텍스트 추출
            review_elem = container.find('p', class_='content-text css-vjs6b8')
            if not review_elem:
                # 대체 셀렉터 시도
                review_elem = container.find('p', class_=re.compile(r'content'))

            if not review_elem:
                fail_count += 1
                continue

            review_text = review_elem.text.strip()

            # 2. 별점 추출 (새로운 방법)
            star_cnt = extract_stars(container)

            # 3. 날짜 추출 (구조 기반: 첫 번째 css-6lreu3만 선택)
            date_text = ''
            date_elems = container.find_all('p', class_='css-6lreu3')
            if date_elems:
                # 첫 번째 요소만 날짜 (두 번째는 사용자명)
                date_text = extract_date(date_elems[0].text.strip())

            # 4. 리뷰 딕셔너리 생성
            review_dict = {
                'review': review_text,
                'stars': star_cnt,
                'date': date_text
            }

            review_list.append(review_dict)
            success_count += 1

        except Exception as e:
            # 개별 리뷰 파싱 실패 시 건너뛰기
            fail_count += 1
            print(f"\n  [경고] 리뷰 {i} 파싱 중 오류: {e}")
            continue

    print(f"\n파싱 완료: 성공 {success_count}개, 실패 {fail_count}개")

    # 통계 출력
    if review_list:
        stars_count = {}
        for r in review_list:
            stars_count[r['stars']] = stars_count.get(r['stars'], 0) + 1

        print(f"\n별점 분포:")
        for stars in sorted(stars_count.keys()):
            print(f"  {stars}점: {stars_count[stars]}개")

    return review_list


def save_reviews(review_list, output_path='./res/reviews.json'):
    """
    리뷰 리스트를 JSON 파일로 저장

    Args:
        review_list (list): 리뷰 딕셔너리 리스트
        output_path (str): 저장할 JSON 파일 경로
    """
    # res 디렉토리가 없으면 생성 (에러 방지)
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # JSON 파일 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(review_list, f, indent=4, ensure_ascii=False)

    print(f"\n리뷰 저장 완료: {output_path}")
    print(f"총 {len(review_list)}개의 리뷰가 저장되었습니다.")


def crawl_yanolja_reviews(url=URL):
    """
    야놀자 리뷰 크롤링 메인 함수

    Args:
        url (str): 크롤링할 야놀자 리뷰 페이지 URL

    Returns:
        list: 수집된 리뷰 리스트
    """
    print("=" * 60)
    print("야놀자 리뷰 크롤러 시작")
    print("=" * 60)
    print(f"URL: {url}\n")

    # 1. Selenium WebDriver 초기화
    print("Chrome 브라우저 시작...")
    driver = webdriver.Chrome()

    try:
        # 2. 페이지 로드
        driver.get(url)
        print(f"페이지 로드 완료\n")

        # 초기 로딩 대기 (3초)
        time.sleep(3)

        # 3. 페이지 스크롤 (동적 콘텐츠 로드)
        scroll_page(driver)

        # 4. HTML 소스 가져오기
        html = driver.page_source

        # 5. 리뷰 파싱
        review_list = parse_reviews(html)

        # 6. JSON 파일로 저장
        save_reviews(review_list)

        return review_list

    except Exception as e:
        print(f"\n[오류] 크롤링 중 에러 발생: {e}")
        return []

    finally:
        # 7. 브라우저 종료
        driver.quit()
        print("\n브라우저 종료")
        print("=" * 60)


if __name__ == '__main__':
    # 크롤러 실행
    crawl_yanolja_reviews()
