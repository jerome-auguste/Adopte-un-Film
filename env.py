
class BaseEnv:
    available_fields = ['director', 'actor', 'genre', 'title', 'score']
    recommendation_categories = ['Based on similar subjects',
                                 'Based on the same story',
                                 'From the same series',
                                 'In the same genre',
                                 'With the same performer (OST)',
                                 'Similar inspirations']
    recommandation_keys = ['topicLabel',
                           'basedOnLabel', 'seriesLabel']
    recommandation_functions = ['recommendation_topic', 'recommendation_based_on', 'recommendation_part_of_series',
                                'recommendation_genre', 'recommendation_performer', 'recommendation_inspiredby']
    num_fields_to_search = 1


env = BaseEnv
