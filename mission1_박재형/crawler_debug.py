"""
야놀자 리뷰 HTML 구조 디버그 도구
별점 추출 로직을 개선하기 위해 실제 HTML 구조를 분석
"""

import time
from bs4 import BeautifulSoup
from selenium import webdriver

# 크롤링 대상 URL
URL = 'https://nol.yanolja.com/reviews/domestic/3013417?sort=LATEST'

def analyze_review_structure(driver, num_reviews=5):
    """
    첫 N개 리뷰의 HTML 구조를 상세 분석

    Args:
        driver: Selenium WebDriver
        num_reviews: 분석할 리뷰 개수
    """
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 리뷰 텍스트를 포함한 요소 찾기
    review_texts = soup.find_all('p', class_=lambda x: x and 'content-text' in x)

    # 전체 페이지에서 SVG 찾기 (별점이 어디 있는지 확인)
    all_svgs = soup.find_all('svg')
    print(f"\n전체 페이지 SVG 개수: {len(all_svgs)}개")
    print(f"(리뷰 {len(review_texts)}개 × 별 5개 = 예상 {len(review_texts) * 5}개)")

    # SVG 샘플 출력
    if all_svgs:
        print(f"\n첫 번째 SVG 샘플:")
        svg_sample = all_svgs[0]
        print(f"  class: {svg_sample.get('class')}")
        print(f"  부모: {svg_sample.parent.name} class={svg_sample.parent.get('class')}")

    print("=" * 80)
    print(f"🔍 야놀자 리뷰 HTML 구조 분석 (처음 {num_reviews}개)")
    print("=" * 80)
    print(f"\n발견된 리뷰 개수: {len(review_texts)}개")

    debug_output = []
    debug_output.append("=" * 80)
    debug_output.append("야놀자 리뷰 HTML 구조 상세 분석")
    debug_output.append("=" * 80)
    debug_output.append(f"\n분석 URL: {URL}")
    debug_output.append(f"발견된 리뷰: {len(review_texts)}개\n")

    for i, review_elem in enumerate(review_texts[:num_reviews], 1):
        print(f"\n{'=' * 80}")
        print(f"리뷰 #{i}")
        print(f"{'=' * 80}")

        debug_output.append(f"\n\n{'=' * 80}")
        debug_output.append(f"리뷰 #{i}")
        debug_output.append(f"{'=' * 80}")

        # 리뷰 텍스트
        review_text = review_elem.text.strip()
        print(f"\n📝 리뷰 텍스트: {review_text[:100]}...")
        debug_output.append(f"\n📝 리뷰 텍스트: {review_text[:100]}...")

        # 상위 컨테이너 여러 레벨 찾기 (별점은 더 위에 있을 수 있음)
        containers = []
        current = review_elem
        for level in range(5):  # 최대 5단계 상위까지
            parent = current.find_parent('div')
            if parent:
                containers.append((level + 1, parent))
                current = parent
            else:
                break

        print(f"\n📦 상위 컨테이너 계층 ({len(containers)}개):")
        debug_output.append(f"\n📦 상위 컨테이너 계층:")

        for level, cont in containers:
            cont_class = cont.get('class')
            print(f"  Level {level}: {cont_class}")
            debug_output.append(f"  Level {level}: {cont_class}")

        # 가장 넓은 범위 컨테이너 선택 (별점이 포함될 가능성 높음)
        container = containers[-1][1] if containers else review_elem.find_parent('div')

        if not container:
            print("⚠️ 상위 컨테이너를 찾을 수 없습니다")
            debug_output.append("⚠️ 상위 컨테이너 없음")
            continue

        # === 별점 요소 탐색 ===
        print(f"\n⭐ 별점 요소 탐색:")
        debug_output.append(f"\n⭐ 별점 요소 탐색:")

        # 1. SVG 태그 찾기
        svgs = container.find_all('svg')
        print(f"  - SVG 개수: {len(svgs)}개")
        debug_output.append(f"  - SVG 개수: {len(svgs)}개")

        if svgs:
            for j, svg in enumerate(svgs[:10], 1):  # 최대 10개까지만
                svg_class = svg.get('class')
                svg_parent = svg.parent
                svg_parent_class = svg_parent.get('class') if svg_parent else None

                print(f"\n  SVG #{j}:")
                print(f"    - class: {svg_class}")
                print(f"    - 부모 class: {svg_parent_class}")
                print(f"    - 부모 태그: {svg_parent.name if svg_parent else 'None'}")

                debug_output.append(f"\n  SVG #{j}:")
                debug_output.append(f"    class: {svg_class}")
                debug_output.append(f"    부모 class: {svg_parent_class}")
                debug_output.append(f"    부모 태그: {svg_parent.name if svg_parent else 'None'}")

                # SVG 내부 구조
                if svg.find('path'):
                    path_d = svg.find('path').get('d', '')[:50]
                    print(f"    - path d: {path_d}...")
                    debug_output.append(f"    path d: {path_d}...")

        # 2. aria-label 속성 찾기 (별점 정보가 숨겨져 있을 수 있음)
        aria_labels = container.find_all(attrs={'aria-label': True})
        if aria_labels:
            print(f"\n  📌 aria-label 발견: {len(aria_labels)}개")
            debug_output.append(f"\n  📌 aria-label 발견:")
            for label_elem in aria_labels[:5]:
                label_text = label_elem.get('aria-label')
                print(f"    - {label_elem.name}: {label_text}")
                debug_output.append(f"    {label_elem.name}: {label_text}")

        # 3. data 속성 찾기
        data_attrs = [attr for attr in container.attrs if attr.startswith('data-')]
        if data_attrs:
            print(f"\n  🔖 data 속성:")
            debug_output.append(f"\n  🔖 data 속성:")
            for attr in data_attrs:
                print(f"    - {attr}: {container[attr]}")
                debug_output.append(f"    {attr}: {container[attr]}")

        # 4. 특정 패턴 클래스 찾기 (별 관련)
        star_keywords = ['star', 'rating', 'score', 'rz7kwu', '1mj121y']
        for keyword in star_keywords:
            elements = container.find_all(class_=lambda x: x and keyword in str(x).lower())
            if elements:
                print(f"\n  🌟 '{keyword}' 포함 요소: {len(elements)}개")
                debug_output.append(f"\n  🌟 '{keyword}' 포함 요소: {len(elements)}개")
                for elem in elements[:3]:
                    print(f"    - {elem.name} class={elem.get('class')}")
                    debug_output.append(f"    {elem.name} class={elem.get('class')}")

        # 5. 각 레벨별 HTML 구조 저장 (별점 위치 찾기)
        print(f"\n  📄 각 레벨별 HTML 구조:")
        debug_output.append(f"\n  📄 각 레벨별 HTML 구조:")

        for level, cont in containers[:3]:  # 처음 3레벨만
            html_snippet = str(cont)[:800]
            print(f"\n    === Level {level} (처음 300자) ===")
            print(f"    {html_snippet[:300]}...")

            debug_output.append(f"\n    === Level {level} (처음 800자) ===")
            debug_output.append(html_snippet)

    # 파일로 저장
    output_path = './debug_html_structure.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(debug_output))

    print(f"\n\n{'=' * 80}")
    print(f"✅ 분석 완료!")
    print(f"상세 내용이 '{output_path}' 파일에 저장되었습니다.")
    print(f"{'=' * 80}")


def main():
    """디버그 크롤러 메인 함수"""
    print("🔍 야놀자 리뷰 HTML 구조 분석 도구")
    print("=" * 80)
    print(f"URL: {URL}\n")

    # Chrome 브라우저 시작
    print("Chrome 브라우저 시작...")
    driver = webdriver.Chrome()

    try:
        # 페이지 로드
        driver.get(URL)
        print(f"페이지 로드 완료\n")

        # 초기 로딩 대기
        time.sleep(3)

        # 약간 스크롤 (동적 콘텐츠 로드)
        print("페이지 스크롤 (2회)...")
        for i in range(2):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2)

        # HTML 구조 분석
        analyze_review_structure(driver, num_reviews=5)

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # 브라우저 종료
        driver.quit()
        print("\n브라우저 종료")


if __name__ == '__main__':
    main()
