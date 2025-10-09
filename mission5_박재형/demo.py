import requests

import gradio as gr


MAPPING_EN2KO = {
    "hangover": "해장",
    "diet": "다이어트"
}
MAPPING_KO2EN = {v: k for k, v in MAPPING_EN2KO.items()}


def get_recommendations(query_ko):
    try:
        query_en = MAPPING_KO2EN[query_ko]
        print(f"Query: {query_en}")
        url = f"http://127.0.0.1:8000/recommend/{query_en}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()[0]
            print(f"Data received: {data}")
            return data
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error in get_recommendations: {e}")
        return None


def fn(query_ko):
    try:
        recs = get_recommendations(query_ko)
        if not recs:
            return "❌ 추천 데이터를 가져올 수 없습니다.", ""

        rec_reason = recs['recommend_reason'] + '\n\n'
        rec_items = ''
        for i, rec in enumerate(recs['recommendations']):
            rec_items += f'음식점 #{i+1}: ' + rec['restaurant'] + '\n'
            rec_items += '메뉴 목록:\n'
            for j, menu in enumerate(rec['menus']):
                rec_items += f'        #{j+1}: ' + menu + '\n'
            rec_items += '\n'

        print(f"Returning: reason={rec_reason[:50]}..., items length={len(rec_items)}")
        return rec_reason, rec_items
    except Exception as e:
        print(f"Error in fn: {e}")
        import traceback
        traceback.print_exc()
        return f"❌ 에러 발생: {str(e)}", ""


def run_demo():
    demo = gr.Interface(
        title='먹어본 박재형의 한 마디 ♾',
        fn=fn,
        inputs=[gr.Radio(['해장', '다이어트'], label='GPT-4 활용 추천 ⓘ', value='다이어트')],
        outputs=[
            gr.Textbox(label='추천 사유', lines=5, interactive=False),
            gr.Textbox(label='추천 아이템', lines=15, interactive=False)
        ]
    )
    demo.launch(share=True, debug=True)


if __name__ == '__main__':
    run_demo()