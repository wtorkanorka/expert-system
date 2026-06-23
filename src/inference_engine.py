class InferenceEngine:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def infer(self, answers):
        language_scores = {lang: 0 for lang in self.kb.languages.keys()}
        priorities = {}
        for question in self.kb.questions:
            question_text = question['question']
            user_answer = answers.get(question_text)

            if not user_answer:
                continue  
            if 'attribute' in question:
                for option in question['options']:
                    if option['text'] == user_answer:
                        priorities[question['attribute']] = option['priority']
                        break
                continue 
            for option in question['options']:
                if option['text'] == user_answer:
                    aspect_priority = 1
                    for prev_question in self.kb.questions:
                        if 'attribute' in prev_question and prev_question['attribute'].startswith(question_text.lower().split()[0]):
                            aspect_priority = priorities.get(prev_question['attribute'], 1)
                            break
                    for trait, weight in option.get('weights', {}).items():
                        for lang, lang_traits in self.kb.languages.items():
                            if trait in lang_traits:
                                language_scores[lang] += lang_traits[trait] * weight * aspect_priority
                    break
        max_score = max(language_scores.values())
        if max_score > 0:
            for lang in language_scores:
                language_scores[lang] = (language_scores[lang] / max_score) * 100
        sorted_languages = sorted(language_scores.items(), key=lambda x: x[1], reverse=True)
        top_languages = [lang for lang, score in sorted_languages if score > 0][:3]
        if top_languages:
            detailed_results = []
            for lang in top_languages:
                detailed_results.append({'language': lang, 'score': round(language_scores[lang], 2)})
            return detailed_results
        else:
            return [{'language': 'Python', 'score': 100}, {'language': 'JavaScript', 'score': 80}]